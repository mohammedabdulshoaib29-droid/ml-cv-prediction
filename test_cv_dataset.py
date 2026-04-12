#!/usr/bin/env python3
"""Test models with CV_DATASET to debug the regression"""

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
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from models.comparison import run_all_models

def test_cv_dataset():
    """Test with the new CV_DATASET"""
    
    print("\n=== Testing with CV_DATASET ===\n")
    
    # Try to load CV_DATASET
    datasets = list(Path("backend/datasets").glob("CV_DATASET*.xlsx"))
    
    if not datasets:
        print("ERROR: No CV_DATASET files found!")
        return False
    
    dataset_file = datasets[0]
    print("[TEST] Loading: {}".format(dataset_file))
    
    try:
        # Load as single dataset
        df = pd.read_excel(dataset_file)
        print("[TEST] Dataset shape: {}".format(df.shape))
        print("[TEST] Columns: {}".format(df.columns.tolist()))
        print("[TEST] Dtypes:\n{}".format(df.dtypes))
        print("[TEST] Data range:")
        print(df.describe())
        
        # Split into train/test
        split_idx = int(len(df) * 0.8)
        train_df = df.iloc[:split_idx].reset_index(drop=True)
        test_df = df.iloc[split_idx:].reset_index(drop=True)
        
        print("\n[TEST] Train shape: {}".format(train_df.shape))
        print("[TEST] Test shape: {}".format(test_df.shape))
        
        # Run models
        print("\n[TEST] Running models...")
        results = run_all_models(train_df, test_df)
        
        print("\n=== RESULTS ===")
        print("Best Model: {}".format(results['best_model']))
        print("Best R²: {:.6f}".format(results['best_r2']))
        print("Capacitance: {:.2f} F/g".format(results['capacitance']))
        
        return True
        
    except Exception as e:
        print("\nERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cv_dataset()
    sys.exit(0 if success else 1)
