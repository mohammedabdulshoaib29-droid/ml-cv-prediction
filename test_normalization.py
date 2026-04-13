import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from models.comparison import run_all_models
from routes.prediction_routes import normalize_cross_dataset, sample_data_for_fast_training

# Load datasets
train_path = Path('backend/datasets/CV_DATASET.xlsx')
test_path = Path('backend/datasets/60MV_CV.xlsx')

print("Loading datasets...")
train_df = pd.read_excel(train_path)
test_df = pd.read_excel(test_path)

print(f"\nBefore normalization:")
print(f"  Train Current: {train_df['Current'].min():.6f} to {train_df['Current'].max():.6f}")
print(f"  Test Current: {test_df['Current'].min():.6f} to {test_df['Current'].max():.6f}")

# Apply normalization
print("\nApplying cross-dataset normalization...")
train_df_norm, test_df_norm, norm_params = normalize_cross_dataset(train_df, test_df)

print(f"\nAfter normalization:")
print(f"  Train Current: {train_df_norm['Current'].min():.6f} to {train_df_norm['Current'].max():.6f}")
print(f"  Test Current: {test_df_norm['Current'].min():.6f} to {test_df_norm['Current'].max():.6f}")

# Sample data
print("\nSampling data...")
train_sample, test_sample = sample_data_for_fast_training(train_df_norm, test_df_norm, max_train_samples=150)

# Run models
print("\n" + "="*60)
print("Running models with normalized data...")
print("="*60)
results = run_all_models(train_sample, test_sample, norm_params)

# Display results
print("\n" + "="*60)
print("MODEL PERFORMANCE RESULTS")
print("="*60)
if "performance" in results:
    perf = results["performance"]
    print(f"\nANN:  R² = {perf['ANN']['r2']:.4f}, RMSE = {perf['ANN']['rmse']:.6f}")
    print(f"RF:   R² = {perf['RF']['r2']:.4f}, RMSE = {perf['RF']['rmse']:.6f}")
    print(f"XGB:  R² = {perf['XGB']['r2']:.4f}, RMSE = {perf['XGB']['rmse']:.6f}")
    print(f"\nBest Model: {results.get('best_model', 'N/A')}")
    print(f"Capacitance (F/g): {results.get('best_capacitance', 0):.2f}")
