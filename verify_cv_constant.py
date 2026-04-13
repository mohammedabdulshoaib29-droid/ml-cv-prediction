#!/usr/bin/env python
"""
Verification script to test that CV_REQUIRED_COLUMNS is properly defined
and the prediction endpoint can initialize correctly.
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

print("="*70)
print("VERIFICATION: CV_REQUIRED_COLUMNS Definition")
print("="*70)

# Test 1: Import the constant directly
print("\n[Test 1] Importing CV_REQUIRED_COLUMNS...")
try:
    from routes.prediction_routes import CV_REQUIRED_COLUMNS
    print(f"✓ Success! CV_REQUIRED_COLUMNS = {CV_REQUIRED_COLUMNS}")
except NameError as e:
    print(f"✗ FAILED: {e}")
    sys.exit(1)

# Test 2: Import the router
print("\n[Test 2] Importing prediction router...")
try:
    from routes.prediction_routes import router
    print(f"✓ Success! Router imported: {router}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    sys.exit(1)

# Test 3: Import the main app
print("\n[Test 3] Importing FastAPI app...")
try:
    from main import app
    print(f"✓ Success! App imported: {app}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    sys.exit(1)

# Test 4: Verify the constant is accessible in the module scope
print("\n[Test 4] Verifying constant in module scope...")
try:
    from routes import prediction_routes
    assert hasattr(prediction_routes, 'CV_REQUIRED_COLUMNS'), "CV_REQUIRED_COLUMNS not found in module"
    print(f"✓ Success! Constant found in module scope")
except Exception as e:
    print(f"✗ FAILED: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("✓ ALL TESTS PASSED - CV_REQUIRED_COLUMNS is properly defined!")
print("="*70)
