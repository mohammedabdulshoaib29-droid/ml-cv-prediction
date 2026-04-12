#!/usr/bin/env python
"""Test the /api/predict endpoint with real Excel files."""

import sys
import asyncio
from pathlib import Path

# Set up path
sys.path.insert(0, 'backend')

async def test_predict_with_excel():
    try:
        print("[1] Importing prediction route...")
        from routes.prediction_routes import predict
        print("[OK] Prediction route imported")
        
        print("[2] Creating mock test file with Excel...")
        
        class MockUploadFile:
            def __init__(self, path):
                self.filename = path.name
                self.path = path
            
            async def read(self):
                return self.path.read_bytes()
        
        # Test with actual Excel file
        test_file_path = Path("backend/datasets/60MV_CV (1) (4).xlsx")
        test_file = MockUploadFile(test_file_path)
        print(f"[OK] Mock file created: {test_file.filename} ({test_file_path.stat().st_size / 1024:.1f} KB)")
        
        print("[3] Calling predict endpoint with Excel file...")
        result = await predict(
            dataset_name="CV_DATASET (1) (4).xlsx",
            test_file=test_file,
            model_type="all"
        )
        print("[OK] Predict succeeded with Excel file!")
        print(f"[RESULT] Status: {result.get('status')}")
        print(f"[RESULT] Test samples: {result.get('test_samples')}")
        print(f"[RESULT] Execution time: {result.get('execution_time_seconds'):.2f}s")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_predict_with_excel())
    sys.exit(0 if success else 1)
