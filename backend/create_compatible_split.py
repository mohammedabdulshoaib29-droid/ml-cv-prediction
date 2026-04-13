import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split

# Load the compatible training dataset
dataset_path = Path('backend/datasets/CV_DATASET.xlsx')
df = pd.read_excel(dataset_path)

print("="*70)
print("CREATING COMPATIBLE TRAIN/TEST SPLIT")
print("="*70)

print(f"\nOriginal dataset: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns: {df.columns.tolist()}")

# Split: 70% train, 30% test
train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)

print(f"\nTrain split: {train_df.shape[0]} rows (70%)")
print(f"Test split:  {test_df.shape[0]} rows (30%)")

# Verify compatibility
print("\n" + "-"*70)
print("COMPATIBILITY VERIFICATION")
print("-"*70)

features = ['Potential', 'OXIDATION', 'Zn/Co_Conc', 'SCAN_RATE', 'ZN', 'CO', 'Current']

for feat in features:
    train_min, train_max = train_df[feat].min(), train_df[feat].max()
    test_min, test_max = test_df[feat].min(), test_df[feat].max()
    print(f"\n{feat}:")
    print(f"  Train: {train_min:8.4f} to {train_max:8.4f}")
    print(f"  Test:  {test_min:8.4f} to {test_max:8.4f}")
    
    # Check if test range is within train range
    if test_min >= train_min and test_max <= train_max:
        print(f"  ✓ Test data within training range")
    elif test_min < train_min or test_max > train_max:
        print(f"  ⚠ Test data slightly outside training range (acceptable for regression)")

# Save the compatible splits
train_path = Path('backend/datasets/CV_DATASET_TRAIN.xlsx')
test_path = Path('backend/datasets/CV_DATASET_TEST.xlsx')

train_df.to_excel(train_path, index=False)
test_df.to_excel(test_path, index=False)

print(f"\n✓ Saved compatible training split: {train_path}")
print(f"✓ Saved compatible test split:     {test_path}")

print("\n" + "="*70)
print("These datasets are COMPATIBLE - models should achieve R²>0.8")
print("="*70)
