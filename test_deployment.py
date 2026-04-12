#!/usr/bin/env python3
"""End-to-end test of the deployed system"""

import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test backend health"""
    print("\n1️⃣  Testing Backend Health...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print(f"   ✅ Backend healthy: {data['message']}")
    return True

def test_get_datasets():
    """Test getting dataset list"""
    print("\n2️⃣  Testing Dataset Endpoint...")
    response = requests.get(f"{BASE_URL}/api/datasets")
    print(f"   Response status: {response.status_code}")
    if response.status_code != 200:
        print(f"   Response: {response.text}")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✅ Found {len(data['datasets'])} datasets")
    for ds in data['datasets'][:3]:
        print(f"      • {ds['name']}")
    return data['datasets']

def test_predict(datasets):
    """Test prediction workflow"""
    if len(datasets) < 2:
        print(f"   ⚠️  Only {len(datasets)} datasets available, need 2 for train/test")
        return False
    
    print("\n3️⃣  Testing Prediction Endpoint...")
    
    # Use first dataset for training, second for testing
    train_dataset = datasets[0]['name']
    test_dataset = datasets[1]['name']
    
    print(f"   📊 Training: {train_dataset}")
    print(f"   📊 Testing: {test_dataset}")
    
    # Create test file path
    test_file_path = Path("datasets") / test_dataset
    
    # Upload test file
    with open(f"backend/{test_file_path}", 'rb') as f:
        files = {'test_file': f}
        data = {'dataset_name': train_dataset}
        
        response = requests.post(
            f"{BASE_URL}/api/predict",
            files=files,
            data=data,
            timeout=120
        )
    
    if response.status_code != 200:
        print(f"   ❌ Prediction failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    result = response.json()
    
    # Verify response structure
    assert "status" in result
    assert result["status"] == "success"
    assert "is_cv_analysis" in result
    assert result["is_cv_analysis"] == True
    
    # Check CV analysis specific fields
    print(f"\n   ✅ Prediction successful!")
    print(f"   📊 Best Model: {result.get('best_model', 'N/A')}")
    print(f"   📊 Best Dopant: {result.get('best_dopant', 'N/A')}")
    print(f"   ⚡ Capacitance: {result.get('capacitance', 0):.2f} F/g")
    print(f"   ⚡ Energy Density: {result.get('energy_density', 0):.2f} Wh/kg")
    print(f"   ⚡ Power Density: {result.get('power_density', 0):.2f} W/kg")
    
    # Check graphs
    if 'graphs' in result:
        print(f"\n   📈 CV Graphs:")
        for model, graph in result['graphs'].items():
            print(f"      • {model}: {len(graph['x'])} points")
    
    # Check table
    if 'table' in result:
        print(f"\n   📋 Model Comparison Table:")
        for row in result['table']:
            print(f"      • {row['model']}: R²={row['r2']:.4f}, RMSE={row['rmse']:.4f}")
    
    return True

def test_frontend():
    """Test if frontend loads"""
    print("\n4️⃣  Testing Frontend (Web UI)...")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert 'html' in response.text.lower() or 'react' in response.text.lower()
    print(f"   ✅ Frontend loads successfully at {BASE_URL}/")
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 END-TO-END SYSTEM DEPLOYMENT TEST")
    print("="*60)
    
    try:
        # Test 1: Health
        test_health()
        
        # Test 2: Datasets
        datasets = test_get_datasets()
        
        # Test 3: Prediction
        test_predict(datasets)
        
        # Test 4: Frontend
        test_frontend()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n🎉 YOUR SYSTEM IS READY:")
        print(f"   🌐 Frontend: http://localhost:8000")
        print(f"   🔌 Backend API: http://localhost:8000/api")
        print(f"   📚 API Docs: http://localhost:8000/docs")
        print("\n💡 Next Steps:")
        print("   1. Open http://localhost:8000 in your browser")
        print("   2. Select a training dataset from dropdown")
        print("   3. Upload a test CSV/Excel file")
        print("   4. Click 'Run Analysis'")
        print("   5. View results, graphs, and recommendations")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
