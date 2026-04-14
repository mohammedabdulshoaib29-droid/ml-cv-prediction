"""
Model Training Routes
Handles training and evaluation of ML models
"""

from flask import Blueprint, request, jsonify, current_app
import os
import pandas as pd
from werkzeug.utils import secure_filename
import traceback
from models.orchestrator import train_all_models
import threading
import json

model_bp = Blueprint('models', __name__)

# Store training jobs status
training_jobs = {}


@model_bp.route('/train', methods=['POST'])
def train_models():
    """
    Train all models using specified training and testing datasets
    
    Expected JSON:
    {
        "train_dataset": "BiFeO3_dataset.xlsx",
        "test_file": <binary file>,
        "predictors": ["col1", "col2", ...],  # Optional
        "target": "column_name"  # Optional
    }
    """
    try:
        # Get training dataset
        train_dataset = request.form.get('train_dataset')
        if not train_dataset:
            return jsonify({'success': False, 'error': 'Training dataset not specified'}), 400
        
        # Load training dataset
        upload_folder = current_app.config['UPLOAD_FOLDER']
        train_path = os.path.join(upload_folder, secure_filename(train_dataset))
        
        if not os.path.exists(train_path):
            return jsonify({'success': False, 'error': 'Training dataset not found'}), 404
        
        try:
            if train_dataset.endswith('.xlsx'):
                train_df = pd.read_excel(train_path)
            else:
                train_df = pd.read_csv(train_path)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to load training dataset: {str(e)}'
            }), 400
        
        # Get test dataset from upload
        if 'test_file' not in request.files:
            return jsonify({'success': False, 'error': 'Test dataset not provided'}), 400
        
        test_file = request.files['test_file']
        if test_file.filename == '':
            return jsonify({'success': False, 'error': 'No test file selected'}), 400
        
        try:
            if test_file.filename.endswith('.xlsx'):
                test_df = pd.read_excel(test_file)
            elif test_file.filename.endswith('.csv'):
                test_df = pd.read_csv(test_file)
            else:
                return jsonify({
                    'success': False,
                    'error': 'Test file must be .xlsx or .csv'
                }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to load test dataset: {str(e)}'
            }), 400
        
        # Get optional parameters
        predictors = request.form.get('predictors')
        if predictors:
            try:
                predictors = json.loads(predictors)
            except:
                predictors = None
        
        target = request.form.get('target', 'Current')
        
        # Train models
        results = train_all_models(train_df, test_df, predictors, target)
        
        return jsonify(results), 200 if results.get('success') else 400
    
    except Exception as e:
        print(f"Error in train_models: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@model_bp.route('/compare', methods=['POST'])
def compare_models():
    """
    Get comparison metrics for all models
    
    Expected JSON:
    {
        "train_dataset": "dataset.xlsx",
        "test_file": <binary>,
        "target": "Current"
    }
    """
    try:
        # Load datasets and train models
        train_dataset = request.form.get('train_dataset')
        upload_folder = current_app.config['UPLOAD_FOLDER']
        train_path = os.path.join(upload_folder, secure_filename(train_dataset))
        
        if not os.path.exists(train_path):
            return jsonify({'success': False, 'error': 'Training dataset not found'}), 404
        
        # Load training dataset
        if train_dataset.endswith('.xlsx'):
            train_df = pd.read_excel(train_path)
        else:
            train_df = pd.read_csv(train_path)
        
        # Load test dataset
        test_file = request.files.get('test_file')
        if not test_file:
            return jsonify({'success': False, 'error': 'Test dataset not provided'}), 400
        
        if test_file.filename.endswith('.xlsx'):
            test_df = pd.read_excel(test_file)
        else:
            test_df = pd.read_csv(test_file)
        
        # Train all models
        results = train_all_models(train_df, test_df)
        
        # Extract comparison data
        comparison = {
            'success': True,
            'models_comparison': {}
        }
        
        for model_name, model_result in results['models'].items():
            if model_result.get('success'):
                comparison['models_comparison'][model_name] = {
                    'r2_score': model_result['metrics']['r2_score'],
                    'rmse': model_result['metrics']['rmse'],
                    'mae': model_result['metrics']['mae'],
                    'best_capacitance': model_result.get('best_capacitance', 0)
                }
        
        comparison['best_model'] = results.get('best_model', {})
        
        return jsonify(comparison), 200
    
    except Exception as e:
        print(f"Error in compare_models: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@model_bp.route('/predict', methods=['POST'])
def predict():
    """
    Run predictions using trained models
    
    Expected form data:
    - dataset_name: Name of training dataset
    - test_file: Test dataset file (xlsx or csv)
    - model_type: Type of model to use ('all', 'ann', 'rf', 'xgb')
    """
    try:
        # Get training dataset name
        dataset_name = request.form.get('dataset_name')
        if not dataset_name:
            return jsonify({'success': False, 'error': 'Dataset name not specified'}), 400
        
        # Load training dataset
        upload_folder = current_app.config['UPLOAD_FOLDER']
        train_path = os.path.join(upload_folder, secure_filename(dataset_name))
        
        if not os.path.exists(train_path):
            return jsonify({'success': False, 'error': 'Training dataset not found'}), 404
        
        try:
            if dataset_name.endswith('.xlsx'):
                train_df = pd.read_excel(train_path)
            else:
                train_df = pd.read_csv(train_path)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to load training dataset: {str(e)}'
            }), 400
        
        # Get test dataset from upload
        if 'test_file' not in request.files:
            return jsonify({'success': False, 'error': 'Test dataset not provided'}), 400
        
        test_file = request.files['test_file']
        if test_file.filename == '':
            return jsonify({'success': False, 'error': 'No test file selected'}), 400
        
        try:
            if test_file.filename.endswith('.xlsx'):
                test_df = pd.read_excel(test_file)
            elif test_file.filename.endswith('.csv'):
                test_df = pd.read_csv(test_file)
            else:
                return jsonify({
                    'success': False,
                    'error': 'Test file must be .xlsx or .csv'
                }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to load test dataset: {str(e)}'
            }), 400
        
        # Get model type (default: all)
        model_type = request.form.get('model_type', 'all')
        
        # Train models
        results = train_all_models(train_df, test_df, model_type=model_type)
        
        return jsonify(results), 200 if results.get('success') else 400
    
    except Exception as e:
        print(f"Error in predict: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500
