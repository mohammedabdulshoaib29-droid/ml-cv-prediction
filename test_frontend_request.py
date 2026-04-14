#!/usr/bin/env python
"""Test the predict endpoint exactly as the frontend sends the request"""

import sys
sys.path.insert(0, 'backend')

from main import app
from io import BytesIO
import pandas as pd

print("\n=== SIMULATING FRONTEND REQUEST ===\n")

client = app.test_client()

# Create a test CSV file in memory (simulating file upload)
test_data = {
    'Potential': [1.0, 1.1, 1.2],
    'Current': [0.5, 0.6, 0.7],
    'OXIDATION': [10, 11, 12],
    'Zn/Co_Conc': [5.0, 5.1, 5.2],
    'SCAN_RATE': [0.05, 0.05, 0.05],
    'ZN': [1, 1, 1],
    'CO': [0, 0, 0]
}

test_df = pd.DataFrame(test_data)
test_bytes = BytesIO()
test_df.to_csv(test_bytes, index=False)
test_bytes.seek(0)

# Simulate the frontend request
print("POST to /api/models/predict with:")
print("  - dataset_name: CV_DATASET.xlsx")
print("  - model_type: all")
print("  - test_file: <CSV data>\n")

response = client.post(
    '/api/models/predict',
    data={
        'dataset_name': 'CV_DATASET.xlsx',
        'model_type': 'all',
        'test_file': (test_bytes, 'test.csv')
    }
)

print(f"Status: {response.status_code}")
try:
    resp_json = response.get_json()
    print(f"Response:")
    for key, value in resp_json.items():
        if isinstance(value, dict) and len(str(value)) > 50:
            print(f"  {key}: <large dict>")
        else:
            print(f"  {key}: {value}")
except Exception as e:
    print(f"Response: {response.data}")

print("\n=== END TEST ===\n")
