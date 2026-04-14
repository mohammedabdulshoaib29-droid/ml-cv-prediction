"""
Shared backend ML pipeline utilities.
"""

import base64
import io
from copy import deepcopy

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler


TARGET_CANDIDATES = [
    'Capacitance',
    'capacitance',
    'Current',
    'current',
    'target',
    'Target',
    'y',
    'Y',
    'label',
    'Label'
]


def empty_model_result(model_name, error=None):
    return {
        'success': False,
        'model': model_name,
        'error': error,
        'metrics': {
            'r2_score': 0.0,
            'rmse': 0.0,
            'mae': 0.0,
            'predicted_capacitance_mean': 0.0,
            'predicted_capacitance_min': 0.0,
            'predicted_capacitance_max': 0.0,
            'train_samples': 0,
            'test_samples': 0
        },
        'plots': {
            'actual_vs_predicted': [],
            'error_distribution': [],
            'capacitance_series': [],
            'images': {
                'actual_vs_predicted': None,
                'error_distribution': None
            }
        },
        'predictions': {
            'actual': [],
            'predicted': [],
            'errors': []
        },
        'metadata': {
            'feature_columns': [],
            'target_column': None,
            'test_has_target': False
        }
    }


def infer_target_column(train_df, requested_target=None):
    if requested_target and requested_target in train_df.columns:
        return requested_target

    for column in TARGET_CANDIDATES:
        if column in train_df.columns:
            return column

    numeric_columns = [column for column in train_df.columns if pd.api.types.is_numeric_dtype(train_df[column])]
    if numeric_columns:
        return numeric_columns[-1]

    if len(train_df.columns) > 0:
        return train_df.columns[-1]

    raise ValueError('Could not infer target column because the training dataset has no columns')


def resolve_feature_columns(train_df, test_df, target_column, predictors=None):
    if predictors:
        missing_train = [column for column in predictors if column not in train_df.columns]
        missing_test = [column for column in predictors if column not in test_df.columns]
        if missing_train:
            raise ValueError(f'Predictor columns not found in training dataset: {missing_train}')
        if missing_test:
            raise ValueError(f'Predictor columns not found in test dataset: {missing_test}')
        feature_candidates = list(predictors)
    else:
        shared_columns = [column for column in train_df.columns if column in test_df.columns and column != target_column]
        feature_candidates = shared_columns

    numeric_features = []
    rejected_features = []
    for column in feature_candidates:
        if column == target_column:
            continue
        if pd.api.types.is_numeric_dtype(train_df[column]) and pd.api.types.is_numeric_dtype(test_df[column]):
            numeric_features.append(column)
        else:
            rejected_features.append(column)

    if not numeric_features:
        raise ValueError('No shared numeric feature columns available for training and testing')

    return numeric_features, rejected_features


def prepare_datasets(train_df, test_df, predictors=None, target=None, scale_features=False):
    train_data = deepcopy(train_df)
    test_data = deepcopy(test_df)

    target_column = infer_target_column(train_data, target)
    if target_column not in train_data.columns:
        raise ValueError(f'Target column "{target_column}" not found in training dataset')

    feature_columns, rejected_features = resolve_feature_columns(train_data, test_data, target_column, predictors)
    if target_column in feature_columns:
        feature_columns.remove(target_column)

    train_features = train_data[feature_columns].apply(pd.to_numeric, errors='coerce')
    test_features = test_data[feature_columns].apply(pd.to_numeric, errors='coerce')

    train_target = pd.to_numeric(train_data[target_column], errors='coerce')
    valid_train_mask = train_target.notna()
    if int(valid_train_mask.sum()) < 5:
        raise ValueError('Training dataset must contain at least 5 valid target rows after cleaning')

    train_features = train_features.loc[valid_train_mask]
    train_target = train_target.loc[valid_train_mask]

    imputer = SimpleImputer(strategy='median')
    x_train = imputer.fit_transform(train_features)
    x_test = imputer.transform(test_features)

    scaler = None
    if scale_features:
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)

    y_test = None
    test_has_target = False
    if target_column in test_data.columns:
        y_test_series = pd.to_numeric(test_data[target_column], errors='coerce')
        if int(y_test_series.notna().sum()) > 0:
            y_test = y_test_series.to_numpy(dtype=float)
            test_has_target = True

    return {
        'x_train': x_train,
        'x_test': x_test,
        'y_train': train_target.to_numpy(dtype=float),
        'y_test': y_test,
        'feature_columns': feature_columns,
        'target_column': target_column,
        'test_has_target': test_has_target,
        'rejected_features': rejected_features,
        'train_samples': int(len(train_target)),
        'test_samples': int(len(test_data))
    }


def sanitize_predictions(predictions):
    values = np.asarray(predictions, dtype=float)
    values = np.nan_to_num(values, nan=0.0, posinf=0.0, neginf=0.0)
    return values


def build_metrics(y_true, y_pred, train_samples, test_samples):
    y_pred = sanitize_predictions(y_pred)

    metrics = {
        'r2_score': 0.0,
        'rmse': 0.0,
        'mae': 0.0,
        'predicted_capacitance_mean': float(np.mean(y_pred)) if len(y_pred) else 0.0,
        'predicted_capacitance_min': float(np.min(y_pred)) if len(y_pred) else 0.0,
        'predicted_capacitance_max': float(np.max(y_pred)) if len(y_pred) else 0.0,
        'train_samples': int(train_samples),
        'test_samples': int(test_samples)
    }

    aligned_true, aligned_pred = align_truth_and_predictions(y_true, y_pred)
    if aligned_true is not None and len(aligned_true) > 1:
        metrics['r2_score'] = float(r2_score(aligned_true, aligned_pred))
        metrics['rmse'] = float(np.sqrt(mean_squared_error(aligned_true, aligned_pred)))
        metrics['mae'] = float(mean_absolute_error(aligned_true, aligned_pred))

    return metrics


def align_truth_and_predictions(y_true, y_pred):
    if y_true is None:
        return None, sanitize_predictions(y_pred)

    truth = pd.Series(y_true).apply(pd.to_numeric, errors='coerce')
    pred = pd.Series(sanitize_predictions(y_pred))
    total = min(len(truth), len(pred))
    truth = truth.iloc[:total]
    pred = pred.iloc[:total]
    valid_mask = truth.notna()
    truth = truth.loc[valid_mask]
    pred = pred.loc[valid_mask]
    return truth.to_numpy(dtype=float), pred.to_numpy(dtype=float)


def _figure_to_base64():
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()
    return encoded


def build_plots(model_name, y_true, y_pred):
    y_pred = sanitize_predictions(y_pred)
    aligned_true, aligned_pred = align_truth_and_predictions(y_true, y_pred)

    plots = {
        'actual_vs_predicted': [],
        'error_distribution': [],
        'capacitance_series': [],
        'images': {
            'actual_vs_predicted': None,
            'error_distribution': None
        }
    }

    for index, prediction in enumerate(y_pred, start=1):
        item = {'index': index, 'predicted': float(prediction)}
        if aligned_true is not None and index <= len(aligned_true):
            item['actual'] = float(aligned_true[index - 1])
            item['error'] = float(prediction - aligned_true[index - 1])
        plots['capacitance_series'].append(item)

    if aligned_true is not None and len(aligned_true):
        for actual, predicted in zip(aligned_true, aligned_pred):
            plots['actual_vs_predicted'].append({
                'actual': float(actual),
                'predicted': float(predicted)
            })

        errors = aligned_pred - aligned_true
        for error in errors:
            plots['error_distribution'].append({'error': float(error)})

        plt.figure(figsize=(6, 4))
        plt.scatter(aligned_true, aligned_pred, alpha=0.75, color='#2f80ed')
        min_val = float(min(np.min(aligned_true), np.min(aligned_pred)))
        max_val = float(max(np.max(aligned_true), np.max(aligned_pred)))
        plt.plot([min_val, max_val], [min_val, max_val], linestyle='--', color='#eb5757')
        plt.title(f'{model_name} Actual vs Predicted')
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plots['images']['actual_vs_predicted'] = _figure_to_base64()

        plt.figure(figsize=(6, 4))
        bins = min(20, max(5, len(errors) // 2)) if len(errors) else 5
        plt.hist(errors, bins=bins, color='#27ae60', alpha=0.8, edgecolor='white')
        plt.title(f'{model_name} Error Distribution')
        plt.xlabel('Prediction Error')
        plt.ylabel('Frequency')
        plots['images']['error_distribution'] = _figure_to_base64()

    return plots


def finalize_model_result(model_name, prepared, predictions):
    y_pred = sanitize_predictions(predictions)
    aligned_true, aligned_pred = align_truth_and_predictions(prepared['y_test'], y_pred)
    metrics = build_metrics(
        aligned_true,
        aligned_pred,
        prepared['train_samples'],
        prepared['test_samples']
    )
    plots = build_plots(model_name, aligned_true, aligned_pred)

    errors = []
    actual_list = []
    if aligned_true is not None:
        actual_list = [float(value) for value in aligned_true]
        errors = [float(pred - actual) for actual, pred in zip(aligned_true, aligned_pred)]

    return {
        'success': True,
        'model': model_name,
        'error': None,
        'metrics': metrics,
        'plots': plots,
        'predictions': {
            'actual': actual_list,
            'predicted': [float(value) for value in aligned_pred],
            'errors': errors
        },
        'metadata': {
            'feature_columns': prepared['feature_columns'],
            'target_column': prepared['target_column'],
            'test_has_target': prepared['test_has_target'],
            'rejected_features': prepared['rejected_features']
        }
    }