"""
Model Orchestrator - Coordinates training of all models
"""

import pandas as pd
import traceback

from models.ann import run_ann
from models.rf import run_rf
from models.xgb import run_xgb
from models.pipeline_utils import empty_model_result


MODEL_RUNNERS = {
    'ANN': run_ann,
    'RandomForest': run_rf,
    'XGBoost': run_xgb
}

MODEL_TYPE_MAP = {
    'all': ['ANN', 'RandomForest', 'XGBoost'],
    'ann': ['ANN'],
    'rf': ['RandomForest'],
    'randomforest': ['RandomForest'],
    'xgb': ['XGBoost'],
    'xgboost': ['XGBoost']
}


def _default_models_payload():
    return {
        'ANN': empty_model_result('ANN'),
        'RandomForest': empty_model_result('RandomForest'),
        'XGBoost': empty_model_result('XGBoost')
    }


def _build_prediction_table(model_results):
    successful_models = {
        model_name: model_result
        for model_name, model_result in model_results.items()
        if model_result.get('success')
    }

    if not successful_models:
        return []

    max_rows = 0
    for model_result in successful_models.values():
        max_rows = max(
            max_rows,
            len(model_result.get('predictions', {}).get('predicted', [])),
            len(model_result.get('predictions', {}).get('actual', []))
        )

    table = []
    for index in range(max_rows):
        row = {'index': index + 1}
        actual_value = None

        for model_name, model_result in successful_models.items():
            prediction_payload = model_result.get('predictions', {})
            actual_values = prediction_payload.get('actual', [])
            predicted_values = prediction_payload.get('predicted', [])

            if actual_value is None and index < len(actual_values):
                actual_value = float(actual_values[index])

            row[model_name] = float(predicted_values[index]) if index < len(predicted_values) else None

        row['actual'] = actual_value
        table.append(row)

    return table


def _build_comparison(model_results):
    comparison = []
    for model_name, model_result in model_results.items():
        if not model_result.get('success'):
            continue

        metrics = model_result.get('metrics', {})
        comparison.append({
            'model': model_name,
            'r2_score': float(metrics.get('r2_score', 0.0)),
            'rmse': float(metrics.get('rmse', 0.0)),
            'mae': float(metrics.get('mae', 0.0)),
            'predicted_capacitance_mean': float(metrics.get('predicted_capacitance_mean', 0.0)),
            'predicted_capacitance_min': float(metrics.get('predicted_capacitance_min', 0.0)),
            'predicted_capacitance_max': float(metrics.get('predicted_capacitance_max', 0.0))
        })

    comparison.sort(key=lambda item: item['rmse'])
    return comparison


def train_all_models(train_df, test_df, predictors=None, target=None, model_type='all', metadata=None):
    results = {
        'success': True,
        'metadata': metadata or {},
        'models': _default_models_payload(),
        'comparison': [],
        'prediction_table': []
    }

    try:
        selected_models = MODEL_TYPE_MAP.get((model_type or 'all').lower(), ['ANN', 'RandomForest', 'XGBoost'])
        model_errors = []

        for model_name in selected_models:
            model_runner = MODEL_RUNNERS[model_name]
            model_result = model_runner(train_df, test_df, predictors, target)
            results['models'][model_name] = model_result

            if not model_result.get('success') and model_result.get('error'):
                model_errors.append({'model': model_name, 'error': model_result.get('error')})

        for model_result in results['models'].values():
            metadata_payload = model_result.get('metadata', {})
            if metadata_payload.get('feature_columns') and not results['metadata'].get('feature_columns'):
                results['metadata']['feature_columns'] = metadata_payload.get('feature_columns')
            if metadata_payload.get('target_column') and not results['metadata'].get('target_column'):
                results['metadata']['target_column'] = metadata_payload.get('target_column')
            if 'test_has_target' in metadata_payload and 'test_has_target' not in results['metadata']:
                results['metadata']['test_has_target'] = metadata_payload.get('test_has_target')
            if metadata_payload.get('rejected_features') and not results['metadata'].get('rejected_features'):
                results['metadata']['rejected_features'] = metadata_payload.get('rejected_features')

        results['comparison'] = _build_comparison(results['models'])
        results['prediction_table'] = _build_prediction_table(results['models'])
        results['timestamp'] = pd.Timestamp.now().isoformat()

        if not results['comparison']:
            results['success'] = False
            results['error'] = 'All model runs failed'
            results['model_errors'] = model_errors
        elif model_errors:
            results['model_errors'] = model_errors

        return results

    except Exception as e:
        print(f'Error training models: {traceback.format_exc()}')
        return {
            'success': False,
            'metadata': metadata or {},
            'models': results['models'],
            'comparison': [],
            'prediction_table': [],
            'error': str(e)
        }