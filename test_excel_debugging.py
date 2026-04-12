#!/usr/bin/env python
"""Test script to diagnose Excel file column structure and data loading."""

import pandas as pd
from pathlib import Path

# Test file paths - adjust these to your actual file paths
test_files = [
    "backend/datasets/sample_cv_train.csv",
    "backend/datasets/CV_DATASET (1) (4).xlsx",
    "backend/datasets/60MV_CV (1) (4).xlsx",
]

print("=" * 80)
print("EXCEL FILE DIAGNOSTIC TEST")
print("=" * 80)

for file_path in test_files:
    p = Path(file_path)
    if not p.exists():
        print(f"\n[SKIP] File not found: {file_path}")
        continue
    
    print(f"\n[FILE] {file_path}")
    print(f"[SIZE] {p.stat().st_size / 1024:.2f} KB")
    
    # Try loading
    try:
        if str(file_path).endswith('.csv'):
            df = pd.read_csv(file_path)
            print(f"[FORMAT] CSV")
        else:
            # Get all sheets
            xl = pd.ExcelFile(file_path)
            print(f"[SHEETS] {xl.sheet_names}")
            df = pd.read_excel(file_path, sheet_name=0)
            print(f"[FORMAT] Excel (Sheet: {xl.sheet_names[0]})")
        
        print(f"[SHAPE] {len(df)} rows x {len(df.columns)} columns")
        print(f"[COLUMNS] {list(df.columns)}")
        
        # Show column details
        for i, col in enumerate(df.columns):
            print(f"  [{i}] '{col}' ({df[col].dtype}) - samples: {df[col].head(2).tolist()}")
        
        # Check for required columns
        required = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO", "Current"]
        missing = set(required) - set(df.columns)
        if missing:
            print(f"[MISSING] {missing}")
            # Try case-insensitive
            available_lower = {col.lower(): col for col in df.columns}
            found = {req: available_lower.get(req.lower()) for req in required}
            found = {k: v for k, v in found.items() if v is not None}
            if found:
                print(f"[CASE_INSENSITIVE_MATCH] {found}")
        else:
            print(f"[STATUS] All required columns present!")
            
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("If you have actual Excel files to test, update test_files above")
print("=" * 80)
