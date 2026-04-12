#!/usr/bin/env python
"""Test the prediction endpoint locally."""

import subprocess
import sys
import time
import requests
import pandas as pd
from pathlib import Path

def start_server():
    """Start the FastAPI server."""
    print("[START] Starting FastAPI server...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"],
        cwd=".",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)  # Wait for server to start
    return proc

def test_prediction():
    """Test the prediction endpoint."""
    base_url = "http://localhost:8000"
    
    # Use the CV_DATASET file as training data
    dataset_name = "CV_DATASET (1) (4).xlsx"
    test_file = Path("backend/datasets/60MV_CV (1) (4).xlsx")
    
    if not test_file.exists():
        print(f"[ERROR] Test file not found: {test_file}")
        return False
    
    print(f"\n[TEST] Prediction endpoint")
    print(f"  Training dataset: {dataset_name}")
    print(f"  Test file: {test_file}")
    
    try:
        with open(test_file, "rb") as f:
            files = {"test_file": (test_file.name, f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            data = {
                "dataset_name": dataset_name,
                "models": "ann,rf,xgb"
            }
            
            print("[SEND] POST /api/predict...")
            resp = requests.post(f"{base_url}/api/predict", files=files, data=data, timeout=120)
            print(f"[RESPONSE] Status: {resp.status_code}")
            
            if resp.status_code == 200:
                result = resp.json()
                print(f"[SUCCESS]")
                print(f"  - Execution time: {result.get('execution_time_seconds', '?'):.2f}s")
                print(f"  - Test samples: {result.get('test_samples', '?')}")
                print(f"  - Models run: {', '.join(result.get('performance', {}).keys())}")
                return True
            else:
                print(f"[ERROR] {resp.status_code}")
                print(f"  Detail: {resp.text[:500]}")
                return False
                
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    proc = None
    try:
        proc = start_server()
        success = test_prediction()
        sys.exit(0 if success else 1)
    finally:
        if proc:
            print("\n[STOP] Stopping server...")
            proc.terminate()
            proc.wait(timeout=5)
