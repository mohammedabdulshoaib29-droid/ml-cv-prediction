import requests
import json

print("Testing prediction API with updated frontend...")

with open('backend/datasets/sample_cv_test.csv', 'rb') as f:
    files = {'test_file': f}
    data = {'dataset_name': 'sample_cv_train.csv', 'model_type': 'all'}
    resp = requests.post('http://localhost:8000/api/predict', files=files, data=data, timeout=60)
    
    if resp.status_code == 200:
        result = resp.json()
        print('\n✅ API Response Received')
        has_graphs = 'graphs' in result
        has_performance = 'performance' in result
        has_recommendations = 'recommendations' in result
        has_table = 'table' in result
        print(f'   Has graphs: {has_graphs}')
        print(f'   Has performance: {has_performance}')
        print(f'   Has recommendations: {has_recommendations}')
        print(f'   Has table: {has_table}')
        
        if has_graphs:
            print(f'\n✅ CV Curves Available:')
            for model in result['graphs']:
                points = len(result['graphs'][model]['x'])
                print(f'   - {model}: {points} concentration points')
        
        if has_performance:
            print(f'\n✅ Model Performance:')
            for model, perf in result['performance'].items():
                print(f'   - {model}: R²={perf["r2"]:.4f}, RMSE={perf["rmse"]:.4f}, Cap={perf["capacitance"]:.2f}')
        
        if has_recommendations:
            print(f'\n✅ Recommendations:')
            for rec in result['recommendations']:
                print(f'   • {rec}')
        
        print(f'\n✅ All components ready for frontend!')
    else:
        print(f'❌ Failed: {resp.status_code}')
        print(resp.text)
