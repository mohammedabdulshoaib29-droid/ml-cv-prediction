import requests
import json

# Test 1: Health check
print('Testing health endpoint...')
try:
    resp = requests.get('http://localhost:8000/health', timeout=5)
    print(f'✅ Health: {resp.json()}')
except Exception as e:
    print(f'❌ Health check failed: {e}')

# Test 2: Get datasets
print('\nTesting datasets endpoint...')
try:
    resp = requests.get('http://localhost:8000/api/datasets', timeout=5)
    if resp.status_code == 200:
        datasets = resp.json().get('datasets', [])
        print(f'✅ Datasets available: {len(datasets)} datasets')
    else:
        print(f'❌ Failed: {resp.status_code}')
except Exception as e:
    print(f'❌ Datasets failed: {e}')

# Test 3: Make a prediction
print('\nTesting prediction endpoint...')
try:
    with open('backend/datasets/sample_cv_test.csv', 'rb') as f:
        files = {'test_file': f}
        data = {'dataset_name': 'sample_cv_train.csv', 'model_type': 'all'}
        resp = requests.post('http://localhost:8000/api/predict', files=files, data=data, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            print(f'✅ Prediction successful!')
            print(f'   - Best Model: {result.get("best_model")}')
            print(f'   - Capacitance: {result.get("capacitance"):.2f} F/g')
            print(f'   - Energy Density: {result.get("energy_density"):.4f} Wh/kg')
        else:
            print(f'❌ Failed: {resp.status_code}')
            print(f'   Error: {resp.text[:200]}')
except Exception as e:
    print(f'❌ Prediction failed: {e}')

print('\n✅ All tests completed!')
