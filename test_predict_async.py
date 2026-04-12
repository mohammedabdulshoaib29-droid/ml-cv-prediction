#!/usr/bin/env python
"""Test the /api/predict endpoint directly without HTTP."""

import sys
import asyncio
from pathlib import Path

# Set up path
sys.path.insert(0, 'backend')

async def test_predict():
    try:
        print("[1] Importing prediction route...")
        from routes.prediction_routes import predict
        print("[OK] Prediction route imported")
        
        print("[2] Creating mock test file...")
        # Use existing test file
        from fastapi import UploadFile
        
        test_file_path = Path("backend/datasets/sample_cv_test.csv")
        
        class MockUploadFile:
            def __init__(self, path):
                self.filename = path.name
                self.path = path
            
            async def read(self):
                return self.path.read_bytes()
        
        test_file = MockUploadFile(test_file_path)
        print(f"[OK] Mock file created: {test_file.filename}")
        
        print("[3] Calling predict endpoint...")
        result = await predict(
            dataset_name="sample_cv_train.csv",
            test_file=test_file,
            model_type="all"
        )
        print("[OK] Predict succeeded!")
        print(f"[RESULT] Status: {result.get('status')}")
        print(f"[RESULT] Models: {result.get('performance', {}).keys()}")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_predict())
    sys.exit(0 if success else 1)
