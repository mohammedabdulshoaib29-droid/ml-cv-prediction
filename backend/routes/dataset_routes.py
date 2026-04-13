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


@dataset_bp.route('/list', methods=['GET'])
def list_datasets():
    """List all available training datasets"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        files = []
        
        if os.path.exists(upload_folder):
            for filename in os.listdir(upload_folder):
                filepath = os.path.join(upload_folder, filename)
                if os.path.isfile(filepath) and allowed_file(filename):
                    # Get file size and basic info
                    size = os.path.getsize(filepath)
                    try:
                        if filename.endswith('.xlsx'):
                            df = pd.read_excel(filepath)
                        else:
                            df = pd.read_csv(filepath)
                        rows = len(df)
                        cols = len(df.columns)
                        columns = list(df.columns)
                    except Exception as e:
                        rows, cols, columns = 0, 0, []
                    
                    files.append({
                        'name': filename,
                        'size': size,
                        'rows': rows,
                        'columns': columns,
                        'cols_count': cols
                    })
        
        return jsonify({
            'success': True,
            'datasets': files,
            'total': len(files)
        }), 200
    except Exception as e:
        print(f"Error listing datasets: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@dataset_bp.route('/upload', methods=['POST'])
def upload_dataset():
    """Upload a new training dataset"""
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
        
        # Save file
        file.save(filepath)
        
        # Validate file
        try:
            if filename.endswith('.xlsx'):
                df = pd.read_excel(filepath)
            else:
                df = pd.read_csv(filepath)
            
            if len(df) == 0:
                os.remove(filepath)
                return jsonify({'success': False, 'error': 'Dataset is empty'}), 400
            
            return jsonify({
                'success': True,
                'filename': filename,
                'rows': len(df),
                'columns': list(df.columns),
                'size': os.path.getsize(filepath)
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
    """Get preview of dataset (first 5 rows and statistics)"""
    try:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(dataset_name))
        
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'Dataset not found'}), 404
        
        # Load dataset
        if dataset_name.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            df = pd.read_csv(filepath)
        
        # Get preview
        preview_data = {
            'name': dataset_name,
            'shape': {'rows': len(df), 'columns': len(df.columns)},
            'columns': list(df.columns),
            'dtypes': {col: str(df[col].dtype) for col in df.columns},
            'preview': df.head(5).to_dict(orient='records'),
            'statistics': {
                col: {
                    'min': float(df[col].min()) if pd.api.types.is_numeric_dtype(df[col]) else None,
                    'max': float(df[col].max()) if pd.api.types.is_numeric_dtype(df[col]) else None,
                    'mean': float(df[col].mean()) if pd.api.types.is_numeric_dtype(df[col]) else None,
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
    """Delete a training dataset"""
    try:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(dataset_name))
        
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'Dataset not found'}), 404
        
        os.remove(filepath)
        return jsonify({'success': True, 'message': f'Dataset {dataset_name} deleted'}), 200
    except Exception as e:
        print(f"Error deleting dataset: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500
from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
import os

router = APIRouter()

# Get datasets directory - works in both local and Render
BACKEND_DIR = Path(__file__).parent.parent
DATASETS_DIR = BACKEND_DIR / "datasets"

# Ensure datasets directory exists
DATASETS_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.csv'}

@router.get("/datasets")
async def get_datasets():
    """Get list of all available datasets"""
    try:
        if not DATASETS_DIR.exists():
            DATASETS_DIR.mkdir(parents=True, exist_ok=True)
            return {"datasets": []}
        
        datasets = []
        for file in DATASETS_DIR.iterdir():
            if file.suffix in ALLOWED_EXTENSIONS:
                datasets.append({
                    "name": file.name,
                    "size": file.stat().st_size,
                    "type": file.suffix
                })
        
        return {"datasets": sorted(datasets, key=lambda x: x['name'])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading datasets: {str(e)}")

@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """Upload and save a new dataset"""
    try:
        # Validate file type
        file_ext = Path(file.filename).suffix
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Create datasets directory if it doesn't exist
        DATASETS_DIR.mkdir(exist_ok=True)
        
        # Save file
        file_path = DATASETS_DIR / file.filename
        
        # Handle duplicate filenames
        if file_path.exists():
            # Append timestamp or version number
            import time
            name, ext = Path(file.filename).stem, file_ext
            file_path = DATASETS_DIR / f"{name}_{int(time.time())}{ext}"
        
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        return {
            "message": "Dataset uploaded successfully",
            "filename": file_path.name,
            "size": len(content)
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.delete("/datasets/{dataset_name}")
async def delete_dataset(dataset_name: str):
    """Delete a dataset"""
    try:
        file_path = DATASETS_DIR / dataset_name
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        file_path.unlink()
        
        return {"message": f"Dataset {dataset_name} deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting dataset: {str(e)}")
