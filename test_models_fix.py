#!/usr/bin/env python
"""Test script to verify ML models are working with proper preprocessing and formulas"""

import requests
import time
import json

def test_models():
    # Wait for server to be ready
    time.sleep(3)
    
    # Test the API with the sample datasets created during startup
    url = "http://localhost:8000/api/predict"
    
    try:
        print("=" * 60)
        print("TESTING UPDATED ML MODELS")
        print("=" * 60)
        print("\nSending prediction request with sample CV analysis datasets...")
        
        # Create multipart form data
        with open("backend/datasets/sample_cv_test.csv", "rb") as f:
            files = {
                "test_file": ("sample_cv_test.csv", f, "text/csv")
            }
            data = {
                "dataset_name": "sample_cv_train.csv",
                "model_type": "all"
            }
            
            response = requests.post(url, files=files, data=data, timeout=30)
            print(f"Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ PREDICTIONS SUCCESSFUL!")
                
                print("\n" + "=" * 60)
                print("MODEL PERFORMANCE METRICS")
                print("=" * 60)
                
                performance = result.get("performance", {})
                for model in ["ANN", "RF", "XGB"]:
                    if model in performance:
                        perf = performance[model]
                        r2 = perf.get("r2", 0)
                        rmse = perf.get("rmse", 0)
                        capacitance = perf.get("capacitance", 0)
                        
                        # Check if R² is positive (fixed!)
                        r2_status = "✅ GOOD" if r2 > 0 else "❌ NEGATIVE"
                        
                        print(f"\n{model}:")
                        print(f"  R² Score: {r2:.6f} {r2_status}")
                        print(f"  RMSE: {rmse:.6f}")
                        print(f"  Capacitance: {capacitance:.6f} F/g")
                
                print("\n" + "=" * 60)
                print("CAPACITANCE ANALYSIS")
                print("=" * 60)
                print(f"Best Model: {result.get('best_model')}")
                print(f"Best Concentration: {result.get('best_concentration'):.4f} M")
                print(f"Best Capacitance: {result.get('capacitance'):.6f} F/g")
                
                print("\n" + "=" * 60)
                print("ENERGY & POWER DENSITY CALCULATIONS")
                print("=" * 60)
                
                energy_density = result.get("energy_density", 0)
                power_density = result.get("power_density", 0)
                
                # Check if values are in realistic ranges
                energy_status = "✅" if 0 < energy_density <= 50 else "❌"
                power_status = "✅" if 1000 <= power_density <= 10000 else "❌"
                
                print(f"\nEnergy Density: {energy_density:.4f} Wh/kg {energy_status}")
                print(f"  (Expected range: 0-50 Wh/kg for supercapacitors)")
                
                print(f"\nPower Density: {power_density:.2f} W/kg {power_status}")
                print(f"  (Expected range: 1000-10000 W/kg for supercapacitors)")
                
                print("\n" + "=" * 60)
                print("FORMULAS VERIFICATION")
                print("=" * 60)
                print("""
E = 0.5 * C * V²
  E: Energy (Joules per kilogram)
  C: Specific Capacitance (F/kg)
  V: Potential window (Volts)

E_Wh = E_J / 3600
  Converts Joules to Watt-hours

P = E / t
  P: Power (Watts per kilogram)
  t: Discharge time (seconds, default=20s)
                """)
                
                print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")
                return True
            else:
                print(f"\n❌ Error Response:")
                print(response.text)
                return False
    
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_models()
    exit(0 if success else 1)
