#!/usr/bin/env python
"""Test to find the actual 500 error."""

import sys
import os

# Set up path
sys.path.insert(0, 'backend')

try:
    print("[1] Importing pandas...")
    import pandas as pd
    print("[OK] Pandas imported")
    
    print("[2] Loading test data...")
    train_df = pd.read_csv("backend/datasets/sample_cv_train.csv")
    test_df = pd.read_csv("backend/datasets/sample_cv_test.csv")
    print(f"[OK] Data loaded - train: {train_df.shape}, test: {test_df.shape}")
    
    print("[3] Importing models...")
    from models.comparison import run_all_models
    print("[OK] Models imported")
    
    print("[4] Running models...")
    result = run_all_models(train_df, test_df)
    print("[OK] Models ran successfully")
    print(f"[RESULT] Keys: {result.keys()}")
    
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
