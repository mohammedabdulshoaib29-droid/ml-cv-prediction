import requests
import sys
from pathlib import Path

try:
    # Prepare files
    test_file_path = Path("backend/datasets/sample_cv_test.csv")
    
    with open(test_file_path, 'rb') as f:
        files = {
            'test_file': f,
        }
        data = {
            'dataset_name': 'sample_cv_train.csv',
            'model_type': 'all'
        }
        
        print("Sending prediction request...")
        response = requests.post(
            'http://localhost:8000/api/predict',
            files=files,
            data=data,
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code != 200:
            print("\n❌ ERROR:")
            try:
                error_data = response.json()
                print(error_data)
            except:
                print(response.text)
        else:
            print("\n✅ SUCCESS!")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
