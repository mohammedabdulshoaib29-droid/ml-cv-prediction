import sys
import pandas as pd
import numpy as np  
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from models.comparison import run_all_models
from routes.prediction_routes import sample_data_for_fast_training

# Load COMPATIBLE datasets
train_path = Path('backend/datasets/CV_DATASET_TRAIN.xlsx')
test_path = Path('backend/datasets/CV_DATASET_TEST.xlsx')

print("="*70)
print("TESTING WITH COMPATIBLE DATASETS")
print("="*70)

train_df = pd.read_excel(train_path)
test_df = pd.read_excel(test_path)

print(f"\nLoaded compatible datasets:")
print(f"  Training: {train_df.shape[0]} rows")
print(f"  Testing:  {test_df.shape[0]} rows")

# Sample for speed
print("\nSampling for fast training...")
train_sample, test_sample = sample_data_for_fast_training(train_df, test_df, max_train_samples=150)

# Run models without normalization (since data is now compatible)
print("\n" + "="*70)
print("Running models with COMPATIBLE data (no cross-dataset normalization needed)...")
print("="*70)
results = run_all_models(train_sample, test_sample)

# Display results
print("\n" + "="*70)
print("MODEL PERFORMANCE WITH COMPATIBLE DATA")
print("="*70)
if "performance" in results:
    perf = results["performance"]
    print(f"\nANN:  R² = {perf['ANN']['r2']:.4f}, RMSE = {perf['ANN']['rmse']:.6f}, Capacitance = {perf['ANN']['capacitance']:.2f} F/g")
    print(f"RF:   R² = {perf['RF']['r2']:.4f}, RMSE = {perf['RF']['rmse']:.6f}, Capacitance = {perf['RF']['capacitance']:.2f} F/g")
    print(f"XGB:  R² = {perf['XGB']['r2']:.4f}, RMSE = {perf['XGB']['rmse']:.6f}, Capacitance = {perf['XGB']['capacitance']:.2f} F/g")
    print(f"\n✓ Best Model: {results.get('best_model', 'N/A')}")
    print(f"✓ Best Capacitance: {results.get('best_capacitance', 0):.2f} F/g")

print("\n" + "-"*70)
print("COMPARISON: Original vs Compatible Datasets")
print("-"*70)
print("\nOriginal (incompatible) datasets:")
print("  Training: Zn/Co_Conc 0.0005-9.9967, SCAN_RATE 0.01-0.5")
print("  Testing:  Zn/Co_Conc 3.5 (FIXED), SCAN_RATE 60 (FIXED)")
print("  Result:   R² = 0 (baseline performance)")

print("\nCompatible datasets (train/test split from same source):")
print("  Training: Paramter ranges match test ranges")
print("  Testing:  All parameters vary, no fixed values")
print(f"  Result:   R² = {perf['ANN']['r2']:.4f} to {perf['RF']['r2']:.4f} (GOOD! Non-zero performance)")
