"""
Model Training Routes
Handles training and evaluation of ML models
"""

from flask import Blueprint, request, jsonify, current_app
import os
import pandas as pd
from werkzeug.utils import secure_filename
import traceback
import json

from models.orchestrator import train_all_models

model_bp = Blueprint('models', __name__)

ALLOWED_EXTENSIONS = {'xlsx', 'csv'}


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _read_uploaded_dataframe(file_storage):
    filename = file_storage.filename or ''
    if not _allowed_file(filename):
        raise ValueError('File must be .xlsx or .csv')

    if filename.lower().endswith('.xlsx'):
        return pd.read_excel(file_storage)
    return pd.read_csv(file_storage)


def _load_training_dataframe(dataset_name):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    train_path = os.path.join(upload_folder, secure_filename(dataset_name))

    if not os.path.exists(train_path):
        raise FileNotFoundError('Training dataset not found')

    if dataset_name.lower().endswith('.xlsx'):
        return pd.read_excel(train_path)
    return pd.read_csv(train_path)


def _extract_predictors():
    predictors = request.form.get('predictors')
    if not predictors:
        return None

    try:
        parsed = json.loads(predictors)
        return parsed if isinstance(parsed, list) else None
    except Exception:
        return None


@model_bp.route('/train', methods=['POST'])
def train():
    """
    Train one or more models using a single stored dataset.
    The dataset is internally split into train/test partitions.
    Optional:
    - dataset_name or train_dataset
    - model_type: all | ann | rf | xgb
    - predictors: optional JSON array of feature names
    - target: ignored unless explicitly valid; pipeline prefers Capacitance
    """
    try:
        dataset_name = request.form.get('dataset_name') or request.form.get('train_dataset')
        if not dataset_name:
            return jsonify({'success': False, 'error': 'Training dataset not specified'}), 400

        train_df = _load_training_dataframe(dataset_name)
        if train_df.empty:
            return jsonify({'success': False, 'error': 'Training dataset is empty'}), 400

        model_type = request.form.get('model_type', 'all')
        predictors = _extract_predictors()
        target = request.form.get('target') or 'Capacitance'

        metadata = {
            'selected_train_dataset': dataset_name,
            'uploaded_test_filename': None,
            'target_column': target,
            'feature_columns': predictors or [],
            'pipeline_mode': 'internal_split_training'
        }

        results = train_all_models(
            train_df=train_df,
            test_df=None,
            predictors=predictors,
            target=target,
            model_type=model_type,
            metadata=metadata
        )

        results['message'] = 'Training completed using internal train/test split'
        if not results.get('success') and results.get('model_errors'):
            results['error'] = 'All model runs failed: ' + '; '.join(
                f"{item.get('model')}: {item.get('error')}"
                for item in results.get('model_errors', [])
                if item.get('error')
            )
        status_code = 200 if results.get('success') else 400
        return jsonify(results), status_code

    except FileNotFoundError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        print(f"Error in train: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@model_bp.route('/predict', methods=['POST'])
def predict():
    """
    Train models using the selected stored dataset and predict on an uploaded dataset.
    Training metrics still come from an internal split of the training dataset.
    Expected form data:
    - dataset_name or train_dataset: Name of stored training dataset
    - test_file: Test dataset file (xlsx or csv)
    - model_type: all | ann | rf | xgb
    - predictors: optional JSON array of feature names
    - target: optional target column name
    """
    try:
        dataset_name = request.form.get('dataset_name') or request.form.get('train_dataset')
        if not dataset_name:
            return jsonify({'success': False, 'error': 'Training dataset not specified'}), 400

        if 'test_file' not in request.files:
            return jsonify({'success': False, 'error': 'Test dataset not provided'}), 400

        test_file = request.files['test_file']
        if test_file.filename == '':
            return jsonify({'success': False, 'error': 'No test file selected'}), 400

        train_df = _load_training_dataframe(dataset_name)
        test_df = _read_uploaded_dataframe(test_file)

        if train_df.empty:
            return jsonify({'success': False, 'error': 'Training dataset is empty'}), 400
        if test_df.empty:
            return jsonify({'success': False, 'error': 'Test dataset is empty'}), 400

        model_type = request.form.get('model_type', 'all')
        predictors = _extract_predictors()
        target = request.form.get('target') or 'Capacitance'

        metadata = {
            'selected_train_dataset': dataset_name,
            'uploaded_test_filename': secure_filename(test_file.filename),
            'target_column': target,
            'feature_columns': predictors or [],
            'pipeline_mode': 'train_split_plus_external_inference'
        }

        results = train_all_models(
            train_df=train_df,
            test_df=test_df,
            predictors=predictors,
            target=target,
            model_type=model_type,
            metadata=metadata
        )

        results['message'] = 'Prediction completed using internally trained models'
        if not results.get('success') and results.get('model_errors'):
            results['error'] = 'All model runs failed: ' + '; '.join(
                f"{item.get('model')}: {item.get('error')}"
                for item in results.get('model_errors', [])
                if item.get('error')
            )
        status_code = 200 if results.get('success') else 400
        return jsonify(results), status_code

    except FileNotFoundError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        print(f"Error in predict: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@model_bp.route('/compare', methods=['POST'])
def compare_models():
    try:
        response, status_code = train()
        return response, status_code
    except Exception as e:
        print(f"Error in compare_models: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
