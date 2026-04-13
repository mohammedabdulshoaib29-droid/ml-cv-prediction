import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

# Load datasets
train_path = Path('backend/datasets/CV_DATASET.xlsx')
test_path = Path('backend/datasets/60MV_CV.xlsx')

train_df = pd.read_excel(train_path)
test_df = pd.read_excel(test_path)

print("="*70)
print("DETAILED DATA ANALYSIS - ROOT CAUSE OF R²=0")
print("="*70)

print("\n1. CURRENT (TARGET VARIABLE) DISTRIBUTION")
print("-" * 70)
train_current = train_df['Current']
test_current = test_df['Current']

print(f"\nTRAINING Current:")
print(f"  Min:        {train_current.min():.6f}")
print(f"  Max:        {train_current.max():.6f}")
print(f"  Mean:       {train_current.mean():.6f}")
print(f"  Median:     {train_current.median():.6f}")
print(f"  Std:        {train_current.std():.6f}")
print(f"  Variance:   {train_current.var():.10f}")
print(f"  Skewness:   {stats.skew(train_current):.4f}")
print(f"  Kurtosis:   {stats.kurtosis(train_current):.4f}")

print(f"\nTEST Current:")
print(f"  Min:        {test_current.min():.6f}")
print(f"  Max:        {test_current.max():.6f}")
print(f"  Mean:       {test_current.mean():.6f}")
print(f"  Median:     {test_current.median():.6f}")
print(f"  Std:        {test_current.std():.6f}")
print(f"  Variance:   {test_current.var():.10f}")
print(f"  Skewness:   {stats.skew(test_current):.4f}")
print(f"  Kurtosis:   {stats.kurtosis(test_current):.4f}")

print("\n2. POTENTIAL (FEATURE) DISTRIBUTION")
print("-" * 70)
train_potential = train_df['Potential']
test_potential = test_df['Potential']

print(f"\nTRAINING Potential:")
print(f"  Min:        {train_potential.min():.6f}")
print(f"  Max:        {train_potential.max():.6f}")
print(f"  Mean:       {train_potential.mean():.6f}")
print(f"  Std:        {train_potential.std():.6f}")

print(f"\nTEST Potential:")
print(f"  Min:        {test_potential.min():.6f}")
print(f"  Max:        {test_potential.max():.6f}")
print(f"  Mean:       {test_potential.mean():.6f}")
print(f"  Std:        {test_potential.std():.6f}")

print("\n3. OTHER FEATURES")
print("-" * 70)
features = ['OXIDATION', 'Zn/Co_Conc', 'SCAN_RATE', 'ZN', 'CO']
for feat in features:
    if feat in train_df.columns and feat in test_df.columns:
        print(f"\n{feat}:")
        print(f"  Train range: {train_df[feat].min():.4f} to {train_df[feat].max():.4f} (mean={train_df[feat].mean():.4f})")
        print(f"  Test range:  {test_df[feat].min():.4f} to {test_df[feat].max():.4f} (mean={test_df[feat].mean():.4f})")

print("\n4. CORRELATION ANALYSIS")
print("-" * 70)
train_corr = train_df[['Potential'] + features + ['Current']].corr()['Current'].sort_values(ascending=False)
test_corr = test_df[['Potential'] + features + ['Current']].corr()['Current'].sort_values(ascending=False)

print("\nTRAINING - Correlation with Current:")
for feat, corr in train_corr.items():
    print(f"  {feat:15s}: {corr:7.4f}")

print("\nTEST - Correlation with Current:")
for feat, corr in test_corr.items():
    print(f"  {feat:15s}: {corr:7.4f}")

print("\n5. KEY FINDINGS")
print("-" * 70)
print(f"✗ Training Current is ONLY POSITIVE (0.00004 to 0.0055)")
print(f"✗ Test Current includes NEGATIVE VALUES (-0.015 to 0.013)")
print(f"✗ Training ranges: Mean={train_current.mean():.6f}, Std={train_current.std():.6f}")
print(f"✗ Test ranges: Mean={test_current.mean():.6f}, Std={test_current.std():.6f}")
print(f"✓ Potential ranges similar: Train {train_potential.min():.2f}-{train_potential.max():.2f}, Test {test_potential.min():.2f}-{test_potential.max():.2f}")
print(f"\n⚠️  CONCLUSION: These appear to be from DIFFERENT EXPERIMENTS or MEASUREMENT CONDITIONS.")
print(f"    The test data is NOT a proper validation set for the training data!")
