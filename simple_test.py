#!/usr/bin/env python
import sys
sys.path.insert(0, 'backend')

from main import app
from io import BytesIO
import pandas as pd

client = app.test_client()

# Create test data
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

# Make the request
response = client.post(
    '/api/models/predict',
    data={
        'dataset_name': 'CV_DATASET.xlsx',
        'model_type': 'all',
        'test_file': (test_bytes, 'test.csv')
    }
)

print(f"Status: {response.status_code}")
resp = response.get_json()
if resp.get('success'):
    print("SUCCESS! Prediction completed")
    print(f"Models trained: {list(resp.get('models', {}).keys())}")
else:
    print(f"ERROR: {resp.get('error','Unknown error')}")
