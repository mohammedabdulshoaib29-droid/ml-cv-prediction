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
from sklearn.model_selection import train_test_split
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


def calculate_capacitance(df):
    required_columns = {'Potential', 'Current', 'SCAN_RATE'}
    if not required_columns.issubset(df.columns):
        return np.nan

    voltages = pd.to_numeric(df['Potential'], errors='coerce').dropna().to_numpy(dtype=float)
    currents = pd.to_numeric(df['Current'], errors='coerce').dropna().to_numpy(dtype=float)
    scan_rate_series = pd.to_numeric(df['SCAN_RATE'], errors='coerce').dropna()

    if len(voltages) == 0 or len(currents) == 0 or scan_rate_series.empty:
        return np.nan

    usable_length = min(len(voltages), len(currents))
    voltages = voltages[:usable_length]
    currents = currents[:usable_length]

    delta_v = float(np.max(voltages) - np.min(voltages)) if usable_length else 0.0
    mass = 0.002
    scan_rate = float(scan_rate_series.mean()) if not scan_rate_series.empty else 0.0
    v = scan_rate / 1000 if scan_rate != 0 else 1e-6
    area = float(np.trapezoid(np.abs(currents), voltages)) if usable_length > 1 else 0.0

    return area / (2 * mass * delta_v * v) if delta_v != 0 else 0.0


def validate_data(df):
    print('Shape:', df.shape)
    print('Missing values:\n', df.isnull().sum())
    for col in df.columns:
        if df[col].nunique(dropna=True) < 2:
            print(f'⚠️ Column {col} has low variance')


def clean_dataset(df):
    cleaned = df.copy()
    cleaned = cleaned.dropna().reset_index(drop=True)

    if 'Current' in cleaned.columns and not cleaned.empty:
        current_series = pd.to_numeric(cleaned['Current'], errors='coerce')
        current_mean = current_series.mean()
        cleaned = cleaned.loc[current_series != current_mean].copy()

    cleaned = cleaned.dropna().reset_index(drop=True)
    return cleaned


def ensure_capacitance_target(df):
    enriched = df.copy()

    if 'Capacitance' not in enriched.columns and {'Potential', 'Current', 'SCAN_RATE'}.issubset(enriched.columns):
        capacitance_value = calculate_capacitance(enriched)
        enriched['Capacitance'] = capacitance_value

    return enriched


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
            'test_has_target': False,
            'split_mode': 'unknown'
        }
    }


def infer_target_column(train_df, requested_target=None):
    if requested_target and requested_target in train_df.columns:
        return requested_target

    capacitance_is_usable = False
    if 'Capacitance' in train_df.columns:
        capacitance_series = pd.to_numeric(train_df['Capacitance'], errors='coerce').dropna()
        capacitance_is_usable = capacitance_series.nunique() > 1

    if capacitance_is_usable:
        return 'Capacitance'

    for column in TARGET_CANDIDATES:
        if column in train_df.columns:
            series = pd.to_numeric(train_df[column], errors='coerce').dropna()
            if series.nunique() > 1:
                return column

    if 'Capacitance' in train_df.columns:
        return 'Capacitance'

    numeric_columns = [column for column in train_df.columns if pd.api.types.is_numeric_dtype(train_df[column])]
    if numeric_columns:
        return numeric_columns[-1]

    if len(train_df.columns) > 0:
        return train_df.columns[-1]

    raise ValueError('Could not infer target column because the training dataset has no columns')


def resolve_feature_columns(train_df, inference_df, target_column, predictors=None):
    missing_inference = []

    if predictors:
        missing_train = [column for column in predictors if column not in train_df.columns]
        if missing_train:
            raise ValueError(f'Predictor columns not found in training dataset: {missing_train}')

        feature_candidates = [column for column in predictors if column in train_df.columns]
        if inference_df is not None:
            missing_inference = [column for column in feature_candidates if column not in inference_df.columns]
    else:
        excluded = {target_column}
        preferred_exclusions = {'Current', 'Capacitance'}
        excluded.update(column for column in preferred_exclusions if column in train_df.columns and column != target_column)
        feature_candidates = [column for column in train_df.columns if column not in excluded]

        if inference_df is not None:
            missing_inference = [column for column in feature_candidates if column not in inference_df.columns]

    numeric_features = []
    rejected_features = []
    for column in feature_candidates:
        if column == target_column:
            continue

        train_is_numeric = pd.api.types.is_numeric_dtype(train_df[column])
        inference_is_numeric = True

        if inference_df is not None and column in inference_df.columns:
            inference_is_numeric = pd.api.types.is_numeric_dtype(inference_df[column])

        if train_is_numeric and inference_is_numeric:
            numeric_features.append(column)
        else:
            rejected_features.append(column)

    if not numeric_features:
        raise ValueError('No numeric feature columns available for model training')

    return numeric_features, rejected_features, missing_inference


def prepare_datasets(train_df, test_df=None, predictors=None, target=None, scale_features=False, split_mode='internal'):
    train_data = ensure_capacitance_target(clean_dataset(deepcopy(train_df)))
    validate_data(train_data)

    if len(train_data) < 5:
        raise ValueError('Training dataset must contain at least 5 valid rows after cleaning')

    target_column = target or 'Capacitance'
    target_column = infer_target_column(train_data, target_column)

    if target_column not in train_data.columns:
        raise ValueError(f'Target column "{target_column}" not found in training dataset')

    if split_mode == 'internal' or test_df is None:
        inference_df = None
    else:
        inference_df = ensure_capacitance_target(clean_dataset(deepcopy(test_df)))
        validate_data(inference_df)

    feature_columns, rejected_features, missing_inference_features = resolve_feature_columns(
        train_data,
        inference_df,
        target_column,
        predictors
    )

    dataset_for_split = train_data[feature_columns + [target_column]].copy()
    dataset_for_split = dataset_for_split.apply(pd.to_numeric, errors='coerce').dropna().reset_index(drop=True)

    if len(dataset_for_split) < 5:
        raise ValueError('Training dataset must contain at least 5 usable numeric rows after preprocessing')

    x = dataset_for_split[feature_columns]
    y = dataset_for_split[target_column]

    print('Target stats:')
    print(y.describe())
    print('X sample:', x.head())
    print('y sample:', y.head())
    print('y unique:', y.nunique())

    if y.nunique() < 2:
        raise ValueError('Target variable has low variance; cannot train reliable models')

    x_train_df, x_eval_df, y_train_series, y_eval_series = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
    )

    imputer = SimpleImputer(strategy='median')
    x_train = imputer.fit_transform(x_train_df)
    x_eval = imputer.transform(x_eval_df)

    scaler = None
    if scale_features:
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_eval = scaler.transform(x_eval)

    inference_x = None
    if inference_df is not None and len(inference_df) > 0:
        inference_features = inference_df.copy()

        for column in feature_columns:
            if column not in inference_features.columns:
                inference_features[column] = np.nan

        inference_features = inference_features[feature_columns].apply(pd.to_numeric, errors='coerce')
        inference_features = inference_features.fillna(inference_features.median(numeric_only=True))

        for index, column in enumerate(feature_columns):
            if inference_features[column].isna().all():
                inference_features[column] = x_train_df[column].median()

        inference_x = imputer.transform(inference_features)
        if scale_features and scaler is not None:
            inference_x = scaler.transform(inference_x)

    return {
        'x_train': x_train,
        'x_test': x_eval,
        'x_inference': inference_x,
        'y_train': y_train_series.to_numpy(dtype=float),
        'y_test': y_eval_series.to_numpy(dtype=float),
        'feature_columns': feature_columns,
        'target_column': target_column,
        'test_has_target': True,
        'rejected_features': rejected_features,
        'missing_inference_features': missing_inference_features,
        'train_samples': int(len(y_train_series)),
        'test_samples': int(len(y_eval_series)),
        'inference_samples': int(len(inference_df)) if inference_df is not None else 0,
        'split_mode': 'internal' if inference_df is None else 'train_plus_inference'
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


def finalize_model_result(model_name, prepared, predictions, inference_predictions=None):
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

    result = {
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
            'rejected_features': prepared['rejected_features'],
            'split_mode': prepared.get('split_mode', 'internal')
        }
    }

    if inference_predictions is not None:
        result['inference'] = {
            'predicted': [float(value) for value in sanitize_predictions(inference_predictions)]
        }

    return result
