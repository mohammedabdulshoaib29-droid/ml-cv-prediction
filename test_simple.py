#!/usr/bin/env python
"""Direct test of ML models - simplified for Render"""

import sys
import pandas as pd
import numpy as np
import time

# Add backend to path
sys.path.insert(0, r'C:\Users\shoai\ml-web-app\backend')

from models.comparison import run_all_models

def test_models_directly():
    print("=" * 70)
    print("MODEL TESTING")
    print("=" * 70)
    
    try:
        # Load sample datasets
        print("\nLoading datasets...")
        train_df = pd.read_csv(r"backend/datasets/sample_cv_train.csv")
        test_df = pd.read_csv(r"backend/datasets/sample_cv_test.csv")
        
        print(f"Train set: {len(train_df)} samples")
        print(f"Test set: {len(test_df)} samples")
        
        # Run all models
        print("\nRunning models...")
        start_time = time.time()
        results = run_all_models(train_df, test_df)
        elapsed = time.time() - start_time
        
        print(f"\nExecution time: {elapsed:.2f} seconds")
        
        # Display results
        print("\n" + "=" * 70)
        print("MODEL PERFORMANCE")
        print("=" * 70)
        
        performance = results.get("performance", {})
        
        for model in ["ANN", "RF", "XGB"]:
            if model in performance:
                r2 = performance[model].get("r2", 0)
                rmse = performance[model].get("rmse", 0)
                print(f"\n{model}:")
                print(f"  R2: {r2:.6f}")
                print(f"  RMSE: {rmse:.6f}")
        
        print("\n" + "=" * 70)
        print("ENERGY & POWER DENSITY")
        print("=" * 70)
        
        energy = results.get("energy_density", 0)
        power = results.get("power_density", 0)
        
        print(f"Energy Density: {energy:.4f} Wh/kg")
        print(f"Power Density: {power:.2f} W/kg")
        
        print("\nSUCCESS: Models executed without errors!")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_models_directly()
    sys.exit(0 if success else 1)
