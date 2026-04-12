import requests

print("Testing Power Density Calculation...")

with open('backend/datasets/sample_cv_test.csv', 'rb') as f:
    files = {'test_file': f}
    data = {'dataset_name': 'sample_cv_train.csv', 'model_type': 'all'}
    resp = requests.post('http://localhost:8000/api/predict', files=files, data=data, timeout=60)
    
    if resp.status_code == 200:
        result = resp.json()
        
        energy = result.get('energy_density', 0)
        power = result.get('power_density', 0)
        capacitance = result.get('capacitance', 0)
        
        print(f"\n✅ SUCCESS - Results:")
        print(f"   Energy Density: {energy:.4f} Wh/kg")
        print(f"   Power Density:  {power:.2f} W/kg")
        print(f"   Capacitance:    {capacitance:.2f} F/g")
        
        # Check if power density is in the correct range
        if 1000 <= power <= 10000:
            print(f"\n✅ CORRECT RANGE: Power density is between 1,000-10,000 W/kg")
        else:
            print(f"\n❌ OUT OF RANGE: Power density {power:.2f} W/kg is outside 1,000-10,000 range")
    else:
        print(f"❌ Failed: {resp.status_code}")
