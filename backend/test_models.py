#!/usr/bin/env python3
"""Quick test script to verify all models work with actual CV data"""

import sys
import os

# Fix for Windows console encoding
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')
    
import pandas as pd
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from models.comparison import run_all_models

def main():
    """Test the complete workflow with actual CV data"""
    
    # Load actual CV datasets
    datasets_dir = Path(__file__).parent / "datasets"
    
    # Find first two CV datasets
    cv_files = sorted([f for f in datasets_dir.glob("*.xlsx") if f.is_file()])
    
    if len(cv_files) < 2:
        print("❌ Need at least 2 CV datasets for train/test split")
        return False
    
    # Load datasets
    print(f"📊 Loading Training Data: {cv_files[0].name}")
    train_df = pd.read_excel(cv_files[0])
    
    print(f"📊 Loading Test Data: {cv_files[1].name}")
    test_df = pd.read_excel(cv_files[1])
    
    print(f"\n✅ Train shape: {train_df.shape}")
    print(f"✅ Test shape: {test_df.shape}")
    
    # Check columns
    required_cols = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO", "Current"]
    train_cols_present = all(col in train_df.columns for col in required_cols)
    test_cols_present = all(col in test_df.columns for col in required_cols)
    
    if not train_cols_present:
        print(f"❌ Missing columns in training data. Have: {train_df.columns.tolist()}")
        return False
    
    if not test_cols_present:
        print(f"❌ Missing columns in test data. Have: {test_df.columns.tolist()}")
        return False
    
    print(f"\n✅ All required columns present")
    
    # Run all models
    print("\n" + "="*60)
    print("🚀 RUNNING ALL MODELS (ANN, RF, XGB)")
    print("="*60)
    
    try:
        results = run_all_models(train_df, test_df)
        
        print("\n" + "="*60)
        print("✅ SUCCESS! All models completed")
        print("="*60)
        
        # Display results
        print(f"\n📊 BEST MODEL: {results['best_model']}")
        print(f"📊 BEST DOPANT: {results['best_dopant']}")
        print(f"📊 BEST CONCENTRATION: {results['best_concentration']:.2f} mol")
        print(f"\n⚡ CAPACITANCE: {results['capacitance']:.2f} F/g")
        print(f"⚡ ENERGY DENSITY: {results['energy_density']:.2f} Wh/kg")
        print(f"⚡ POWER DENSITY: {results['power_density']:.2f} W/kg")
        
        print(f"\n📈 MODEL PERFORMANCE:")
        for model, perf in results['performance'].items():
            print(f"  {model}:")
            print(f"    R² = {perf['r2']:.4f}")
            print(f"    RMSE = {perf['rmse']:.4f}")
            print(f"    Capacitance = {perf['capacitance']:.2f} F/g")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"  • {rec}")
        
        print(f"\n📊 CV GRAPHS:")
        for model, graph in results['graphs'].items():
            print(f"  {model}: {len(graph['x'])} concentration points")
        
        print(f"\n✅ TEST PASSED! System is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
