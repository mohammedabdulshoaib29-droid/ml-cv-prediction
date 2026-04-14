#!/usr/bin/env python
"""Test the predict endpoint"""

import sys
sys.path.insert(0, 'backend')

from backend.main import app
import json

# Create test client
client = app.test_client()

print("\n=== Testing /api/models/predict endpoint ===\n")

# Test 1: POST request with no files (should fail with 400)
print("Test 1: POST with no test file")
response = client.post('/api/models/predict',
    data={
        'dataset_name': 'test.xlsx',
        'model_type': 'all'
    }
)
print(f'Status: {response.status_code}')
print(f'Response: {response.get_json()}')
print()

# Test 2: Try with GET (should fail with 405 if not allowed)
print("Test 2: GET request (should be 405)")
response = client.get('/api/models/predict')
print(f'Status: {response.status_code}')
print(f'Response: {response.get_json()}')
print()

print("=== End of tests ===\n")
