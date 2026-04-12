#!/usr/bin/env python
"""Direct test of column validation logic."""

import pandas as pd
from pathlib import Path

# Directly define the functions
def normalize_columns(df):
    """Normalize column names: strip whitespace, standardize format"""
    df.columns = [col.strip() for col in df.columns]
    return df

def get_column_mapping(available_cols, required_cols):
    """
    Try to match required columns with available columns.
    """
    available_set = set(available_cols)
    
    # First try exact match
    if all(col in available_set for col in required_cols):
        return {col: col for col in required_cols}
    
    # Try case-insensitive match
    available_lower = {col.lower(): col for col in available_cols}
    required_lower = {col.lower(): col for col in required_cols}
    
    if all(col_lower in available_lower for col_lower in required_lower):
        return {req: available_lower[req.lower()] for req in required_cols}
    
    return None

# Define required columns
CV_REQUIRED_COLUMNS = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO", "Current"]

# Test with actual files
test_files = [
    ("backend/datasets/sample_cv_train.csv", "sample_cv_train"),
    ("backend/datasets/CV_DATASET (1) (4).xlsx", "CV_DATASET"),
    ("backend/datasets/60MV_CV (1) (4).xlsx", "60MV_CV"),
]

print("=" * 80)
print("COLUMN VALIDATION TEST")
print("=" * 80)

for file_path, name in test_files:
    p = Path(file_path)
    if not p.exists():
        print(f"\n[SKIP] {name}: File not found")
        continue
    
    print(f"\n[TEST] {name}")
    
    try:
        # Load file
        if str(file_path).endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path, sheet_name=0)
        
        print(f"  Original columns: {list(df.columns)}")
        
        # Normalize
        df = normalize_columns(df)
        print(f"  After normalize: {list(df.columns)}")
        
        # Check
        train_cols = set(df.columns)
        required_cols = set(CV_REQUIRED_COLUMNS)
        missing = required_cols - train_cols
        
        if missing:
            print(f"  Missing columns: {missing}")
            
            # Try mapping
            mapping = get_column_mapping(df.columns, CV_REQUIRED_COLUMNS)
            if mapping:
                print(f"  Found mapping: {mapping}")
                df_mapped = df.rename(columns=mapping)
                print(f"  After remap: {list(df_mapped.columns)}")
                print(f"  [SUCCESS] All columns present after mapping!")
            else:
                print(f"  [FAIL] No mapping possible")
        else:
            print(f"  [SUCCESS] All required columns present!")
            
    except Exception as e:
        print(f"  [ERROR] {e}")

print("\n" + "=" * 80)
