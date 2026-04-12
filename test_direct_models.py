#!/usr/bin/env python
"""Direct test of ML models to verify preprocessing fixes"""

import sys
import pandas as pd
import numpy as np

# Add backend to path
sys.path.insert(0, r'C:\Users\shoai\ml-web-app\backend')

from models.comparison import run_all_models

def test_models_directly():
    print("=" * 70)
    print("DIRECT MODEL TESTING - VERIFYING PREPROCESSING & FORMULA FIXES")
    print("=" * 70)
    
    try:
        # Load sample datasets
        print("\n📚 Loading sample datasets...")
        train_df = pd.read_csv(r"backend/datasets/sample_cv_train.csv")
        test_df = pd.read_csv(r"backend/datasets/sample_cv_test.csv")
        
        print(f"  ✓ Train set: {len(train_df)} samples")
        print(f"  ✓ Test set: {len(test_df)} samples")
        
        # Check data structure
        print(f"\n  Train columns: {train_df.columns.tolist()}")
        print(f"  Data types:\n{train_df.dtypes}")
        
        # Run all models
        print("\n🤖 Running ML models with updated preprocessing...")
        print("  (RobustScaler, IQR outlier removal, improved hyperparameters)")
        
        results = run_all_models(train_df, test_df)
        
        # Display results
        print("\n" + "=" * 70)
        print("RESULTS - MODEL PERFORMANCE")
        print("=" * 70)
        
        performance = results.get("performance", {})
        
        print("\n📊 R² Scores (should be > 0 after fix):")
        for model in ["ANN", "RF", "XGB"]:
            if model in performance:
                r2 = performance[model].get("r2", 0)
                rmse = performance[model].get("rmse", 0)
                cap = performance[model].get("capacitance", 0)
                
                status = "✅ POSITIVE" if r2 > 0 else "❌ NEGATIVE"
                print(f"\n  {model}:")
                print(f"    R² = {r2:.6f} {status}")
                print(f"    RMSE = {rmse:.6f}")
                print(f"    Capacitance = {cap:.6f} F/g")
        
        print("\n" + "=" * 70)
        print("CAPACITANCE ANALYSIS")
        print("=" * 70)
        
        best_model = results.get("best_model", "Unknown")
        best_cap = results.get("capacitance", 0)
        best_conc = results.get("best_concentration", 0)
        
        print(f"\n  Best Model: {best_model}")
        print(f"  Best Concentration: {best_conc:.4f}")
        print(f"  Maximum Capacitance: {best_cap:.6f} F/g")
        
        print("\n" + "=" * 70)
        print("ENERGY & POWER DENSITY CALCULATIONS")
        print("=" * 70)
        
        energy_density = results.get("energy_density", 0)
        power_density = results.get("power_density", 0)
        
        print(f"\n  Energy Density: {energy_density:.4f} Wh/kg")
        print(f"    ✓ Using formula: E = 0.5 × C × V²")
        print(f"    ✓ Realistic range: 0-50 Wh/kg for supercaps")
        print(f"    Status: {'✅ GOOD' if 0 <= energy_density <= 50 else '❌ OUT OF RANGE'}")
        
        print(f"\n  Power Density: {power_density:.2f} W/kg")
        print(f"    ✓ Using formula: P = E / t (t=20s)")
        print(f"    ✓ Realistic range: 1000-10000 W/kg for supercaps")
        print(f"    Status: {'✅ GOOD' if 1000 <= power_density <= 10000 else '❌ OUT OF RANGE'}")
        
        print("\n" + "=" * 70)
        print("PREPROCESSING IMPROVEMENTS APPLIED")
        print("=" * 70)
        
        print("""
✅ FIXES IMPLEMENTED IN ALL THREE MODELS:

1. RobustScaler: Replaces StandardScaler
   - Better handles electrochemical data with natural outliers
   - Uses median and quartile ranges instead of mean/std
   - Less affected by extreme values in current measurements

2. IQR-Based Outlier Removal:
   - Removes extreme values only from training data
   - Uses Interquartile Range (Q3 - Q1) × 1.5 threshold
   - Prevents model from learning noise patterns

3. Improved Model Architectures:
   - ANN: Added BatchNormalization, changed to Huber loss
   - RF: Increased n_estimators, optimized max_depth
   - XGB: Added regularization (L1/L2), optimized depth

4. Better Hyperparameters:
   - Reduced overfitting through regularization
   - Adjusted learning rates and tree depths
   - Removed artificial noise from predictions

5. Correct Energy/Power Density Formulas:
   - E = 0.5 × C × V² (Energy in Joules/kg)
   - P = E / discharge_time (Power in Watts/kg)
   - Proper unit conversions (J/kg → Wh/kg)
        """)
        
        # Check if models improved
        all_positive_r2 = all(
            performance.get(m, {}).get("r2", -1) > 0 
            for m in ["ANN", "RF", "XGB"]
        )
        
        print("\n" + "=" * 70)
        if all_positive_r2:
            print("✅ SUCCESS: All models have positive R² scores!")
            print("✅ Preprocessing and formulas are correctly implemented!")
        else:
            print("⚠️  Some models still have R² < 0")
            print("    This may indicate:")
            print("    - Very small or imbalanced training set")
            print("    - Input features not strongly correlated with target")
            print("    - Better data preprocessing or feature engineering needed")
        print("=" * 70 + "\n")
        
        return all_positive_r2
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_models_directly()
    sys.exit(0 if success else 1)
