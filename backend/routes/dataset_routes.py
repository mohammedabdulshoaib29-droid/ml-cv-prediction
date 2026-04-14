"""
Dataset Management Routes
Handles uploading, listing, and managing training datasets
"""

from flask import Blueprint, request, jsonify, current_app
import os
import pandas as pd
from werkzeug.utils import secure_filename
import traceback

dataset_bp = Blueprint('datasets', __name__)

ALLOWED_EXTENSIONS = {'xlsx', 'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _read_dataset(filepath):
    if filepath.lower().endswith('.xlsx'):
        return pd.read_excel(filepath)
    return pd.read_csv(filepath)


def _build_dataset_summary(filename, filepath):
    df = _read_dataset(filepath)
    numeric_columns = [column for column in df.columns if pd.api.types.is_numeric_dtype(df[column])]
    target_candidates = ['Current', 'current', 'Capacitance', 'capacitance', 'target', 'Target']
    inferred_target = next((column for column in target_candidates if column in df.columns), df.columns[-1] if len(df.columns) else None)

    return {
        'name': filename,
        'size': os.path.getsize(filepath),
        'rows': int(len(df)),
        'columns': list(df.columns),
        'cols_count': int(len(df.columns)),
        'numeric_columns': numeric_columns,
        'target_column': inferred_target
    }


@dataset_bp.route('/list', methods=['GET'])
def list_datasets():
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        files = []

        if os.path.exists(upload_folder):
            for filename in os.listdir(upload_folder):
                filepath = os.path.join(upload_folder, filename)
                if os.path.isfile(filepath) and allowed_file(filename):
                    try:
                        files.append(_build_dataset_summary(filename, filepath))
                    except Exception:
                        files.append({
                            'name': filename,
                            'size': os.path.getsize(filepath),
                            'rows': 0,
                            'columns': [],
                            'cols_count': 0,
                            'numeric_columns': [],
                            'target_column': None
                        })

        return jsonify({
            'success': True,
            'datasets': sorted(files, key=lambda item: item['name'].lower()),
            'total': len(files)
        }), 200
    except Exception as e:
        print(f"Error listing datasets: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@dataset_bp.route('/upload', methods=['POST'])
def upload_dataset():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Only .xlsx and .csv files allowed'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            df = _read_dataset(filepath)
            if len(df) == 0:
                os.remove(filepath)
                return jsonify({'success': False, 'error': 'Dataset is empty'}), 400

            summary = _build_dataset_summary(filename, filepath)
            return jsonify({
                'success': True,
                'dataset': summary
            }), 201
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'success': False, 'error': f'Invalid file format: {str(e)}'}), 400

    except Exception as e:
        print(f"Error uploading dataset: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@dataset_bp.route('/preview/<dataset_name>', methods=['GET'])
def preview_dataset(dataset_name):
    try:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(dataset_name))

        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'Dataset not found'}), 404

        df = _read_dataset(filepath)

        preview_data = {
            'name': dataset_name,
            'shape': {'rows': int(len(df)), 'columns': int(len(df.columns))},
            'columns': list(df.columns),
            'numeric_columns': [column for column in df.columns if pd.api.types.is_numeric_dtype(df[column])],
            'dtypes': {col: str(df[col].dtype) for col in df.columns},
            'preview': df.head(10).where(pd.notnull(df.head(10)), None).to_dict(orient='records'),
            'statistics': {
                col: {
                    'min': float(df[col].min()) if pd.api.types.is_numeric_dtype(df[col]) and not df[col].dropna().empty else None,
                    'max': float(df[col].max()) if pd.api.types.is_numeric_dtype(df[col]) and not df[col].dropna().empty else None,
                    'mean': float(df[col].mean()) if pd.api.types.is_numeric_dtype(df[col]) and not df[col].dropna().empty else None,
                    'null_count': int(df[col].isnull().sum())
                }
                for col in df.columns
            }
        }

        return jsonify({'success': True, 'data': preview_data}), 200
    except Exception as e:
        print(f"Error previewing dataset: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@dataset_bp.route('/delete/<dataset_name>', methods=['DELETE'])
def delete_dataset(dataset_name):
    try:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(dataset_name))

        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'Dataset not found'}), 404

        os.remove(filepath)
        return jsonify({'success': True, 'message': f'Dataset {dataset_name} deleted'}), 200
    except Exception as e:
        print(f"Error deleting dataset: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500