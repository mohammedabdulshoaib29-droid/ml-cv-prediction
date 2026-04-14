#!/usr/bin/env python
"""Test model training with new CV dataset"""

import sys
sys.path.insert(0, 'backend')
from main import app

client = app.test_client()
response = client.post('/api/models/train', data={'dataset_name': 'CV_DATASET.xlsx', 'model_type': 'all'})

print(f'Status: {response.status_code}')
result = response.get_json()

if result.get('success'):
    print('\n✅ Training succeeded!')
    best = result.get('best_model', {})
    print(f'Best Model: {best.get("name")}')
    print(f'Capacitance: {best.get("capacitance")}')
    
    print('\nModel Results:')
    for model_name, model_result in result.get('models', {}).items():
        metrics = model_result.get('metrics', {})
        status = 'Success' if model_result.get('success') else 'Failed'
        print(f'  {model_name}: {status}')
        if model_result.get('success'):
            print(f'    R² = {metrics.get("r2_score")}')
            print(f'    RMSE = {metrics.get("rmse")}')
        else:
            print(f'    Error: {model_result.get("error")}')
else:
    print(f'\n❌ Training failed: {result.get("error")}')
