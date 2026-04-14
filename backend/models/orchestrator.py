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


def _safe_float(value, default=None):
    try:
        if value in (None, ''):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _clean_metric(value):
    return _safe_float(value, None)


def _infer_dopant(metadata, train_df=None, test_df=None):
    metadata = metadata or {}
    direct_candidates = [
        metadata.get('best_dopant'),
        metadata.get('dopant'),
        metadata.get('recommended_dopant'),
    ]
    for candidate in direct_candidates:
        if candidate not in (None, ''):
            return candidate

    dataset_candidates = []
    if train_df is not None:
        dataset_candidates.append(train_df)
    if test_df is not None:
        dataset_candidates.append(test_df)

    dopant_columns = ['Dopant', 'dopant', 'Best Dopant', 'best_dopant']
    for dataset in dataset_candidates:
        for column in dopant_columns:
            if column in dataset.columns:
                series = dataset[column].dropna()
                if not series.empty:
                    first_value = series.iloc[0]
                    if first_value not in (None, ''):
                        return str(first_value)

    return 'Zn-Co'


def _extract_series_points(model_result):
    series = model_result.get('plots', {}).get('capacitance_series', []) or []
    normalized_series = []

    for index, point in enumerate(series, start=1):
        concentration = _safe_float(
            point.get('concentration', point.get('index', index)),
            index,
        )
        predicted = _safe_float(point.get('predicted'))
        actual = _safe_float(point.get('actual'))
        error = _safe_float(point.get('error'))

        item = {
            'index': int(_safe_float(point.get('index'), index) or index),
            'concentration': concentration,
            'predicted': predicted,
        }
        if actual is not None:
            item['actual'] = actual
        if error is not None:
            item['error'] = error
        normalized_series.append(item)

    if normalized_series:
        return normalized_series

    predicted_values = model_result.get('predictions', {}).get('predicted', []) or []
    return [
        {
            'index': index + 1,
            'concentration': float(index + 1),
            'predicted': _safe_float(predicted),
        }
        for index, predicted in enumerate(predicted_values)
    ]


def _best_concentration_from_model(model_result):
    series = _extract_series_points(model_result)
    if not series:
        return None

    valid_series = [
        item for item in series
        if _safe_float(item.get('predicted', item.get('actual')), None) is not None
    ]
    if not valid_series:
        return None

    best_point = max(
        valid_series,
        key=lambda item: _safe_float(item.get('predicted', item.get('actual')), float('-inf'))
    )
    return _safe_float(
        best_point.get('concentration', best_point.get('index')),
        _safe_float(best_point.get('index')),
    )


def _best_capacitance_from_model(model_result):
    metrics = model_result.get('metrics', {})
    preferred = metrics.get('predicted_capacitance_max')
    cleaned_preferred = _clean_metric(preferred)
    if cleaned_preferred is not None:
        return cleaned_preferred

    series = _extract_series_points(model_result)
    valid_values = [
        _safe_float(item.get('predicted', item.get('actual')), None)
        for item in series
    ]
    valid_values = [value for value in valid_values if value is not None]
    if not valid_values:
        return None

    return max(valid_values)


def _build_comparison(model_results):
    comparison = []
    for model_name, model_result in model_results.items():
        if not model_result.get('success'):
            continue

        metrics = model_result.get('metrics', {})
        comparison.append({
            'model': model_name,
            'r2_score': _clean_metric(metrics.get('r2_score')),
            'rmse': _clean_metric(metrics.get('rmse')),
            'mae': _clean_metric(metrics.get('mae')),
            'predicted_capacitance_mean': _clean_metric(metrics.get('predicted_capacitance_mean')),
            'predicted_capacitance_min': _clean_metric(metrics.get('predicted_capacitance_min')),
            'predicted_capacitance_max': _clean_metric(metrics.get('predicted_capacitance_max')),
            'capacitance': _best_capacitance_from_model(model_result),
            'best_concentration': _best_concentration_from_model(model_result),
        })

    comparison.sort(key=lambda item: item['rmse'] if item['rmse'] is not None else float('inf'))
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

        successful_models = {
            name: result
            for name, result in results['models'].items()
            if result.get('success')
        }

        performance = {}
        graphs = {}
        table = []

        for model_name, model_result in results['models'].items():
            metrics = model_result.get('metrics', {})
            best_capacitance = _best_capacitance_from_model(model_result)
            best_concentration = _best_concentration_from_model(model_result)

            performance[model_name] = {
                'status': 'Success' if model_result.get('success') else 'Failed',
                'r2': _clean_metric(metrics.get('r2_score')) if model_result.get('success') else None,
                'rmse': _clean_metric(metrics.get('rmse')) if model_result.get('success') else None,
                'capacitance': best_capacitance if model_result.get('success') else None,
                'best_concentration': best_concentration if model_result.get('success') else None,
                'error': model_result.get('error'),
            }

            graphs[model_name] = _extract_series_points(model_result)

            table.append({
                'model': model_name,
                'status': performance[model_name]['status'],
                'r2_score': performance[model_name]['r2'],
                'rmse': performance[model_name]['rmse'],
                'capacitance': performance[model_name]['capacitance'],
                'best_concentration': performance[model_name]['best_concentration'],
            })

        if successful_models:
            ranked_models = [
                (name, _best_capacitance_from_model(model_result))
                for name, model_result in successful_models.items()
            ]
            ranked_models = [
                (name, capacitance_value)
                for name, capacitance_value in ranked_models
                if capacitance_value is not None
            ]

            if ranked_models:
                best_model_name = max(ranked_models, key=lambda item: item[1])[0]
            else:
                best_model_name = next(iter(successful_models))

            best_model_result = successful_models[best_model_name]
            best_capacitance = _best_capacitance_from_model(best_model_result)
            best_concentration = _best_concentration_from_model(best_model_result)
            best_dopant = _infer_dopant(results.get('metadata'), train_df, test_df)

            best_model = {
                'name': best_model_name,
                'capacitance': best_capacitance,
                'best_concentration': best_concentration,
                'dopant': best_dopant,
            }
            results['best_model'] = best_model
            results['capacitance'] = best_capacitance
            results['best_concentration'] = best_concentration
            results['best_dopant'] = best_dopant
        else:
            results['best_model'] = None
            results['capacitance'] = None
            results['best_concentration'] = None
            results['best_dopant'] = None

        results['performance'] = performance
        results['graphs'] = graphs
        results['table'] = table

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