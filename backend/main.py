"""
ML Web App - Main Flask Application
Complete multi-page BiFe2O3 ML prediction backend with dataset, training,
prediction, dashboard, and analytics support.
"""

from pathlib import Path
import os
import traceback

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

# Flask setup
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_BUILD = BASE_DIR.parent / 'frontend' / 'build'
UPLOAD_FOLDER = BASE_DIR / 'datasets'
TEST_UPLOAD_FOLDER = UPLOAD_FOLDER / 'test_uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}

app = Flask(__name__, static_folder=None)
CORS(app)
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['TEST_UPLOAD_FOLDER'] = str(TEST_UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
TEST_UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

LATEST_STATE = {
    'selected_dataset': None,
    'latest_test_file': None,
    'latest_results': None,
    'training_status': 'idle',
    'prediction_status': 'idle',
}

# Import routes after app setup
from routes.dataset_routes import dataset_bp, _build_dataset_summary, _read_dataset, allowed_file
from routes.health_routes import health_bp
from routes.model_routes import model_bp, train as run_model_pipeline

# Register blueprints
app.register_blueprint(dataset_bp, url_prefix='/api/datasets')
app.register_blueprint(model_bp, url_prefix='/api/models')
app.register_blueprint(health_bp, url_prefix='/api/health')


def _datasets_payload():
    datasets = []

    if UPLOAD_FOLDER.exists():
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = UPLOAD_FOLDER / filename
            if filepath.is_file() and allowed_file(filename):
                try:
                    datasets.append(_build_dataset_summary(filename, str(filepath)))
                except Exception:
                    datasets.append({
                        'name': filename,
                        'size': filepath.stat().st_size,
                        'rows': 0,
                        'columns': [],
                        'cols_count': 0,
                        'numeric_columns': [],
                        'target_column': None,
                    })

    datasets.sort(key=lambda item: item['name'].lower())
    return datasets


def _results_payload():
    return {
        'success': True,
        'message': 'Latest application state loaded',
        'datasets': _datasets_payload(),
        'selected_dataset': LATEST_STATE.get('selected_dataset'),
        'latest_test_file': LATEST_STATE.get('latest_test_file'),
        'training_status': LATEST_STATE.get('training_status', 'idle'),
        'prediction_status': LATEST_STATE.get('prediction_status', 'idle'),
        'results': LATEST_STATE.get('latest_results'),
        **(LATEST_STATE.get('latest_results') or {}),
    }


def _save_uploaded_test_file(file_storage):
    filename = secure_filename(file_storage.filename or '')
    if not filename:
        raise ValueError('No test file selected')
    if not allowed_file(filename):
        raise ValueError('Only .xlsx and .csv files allowed')

    target_path = TEST_UPLOAD_FOLDER / filename
    file_storage.save(target_path)
    _read_dataset(str(target_path))
    return filename, target_path


@app.route('/ping')
def ping():
    return jsonify({'status': 'pong', 'service': 'flask'}), 200


@app.route('/upload-train', methods=['POST'])
def upload_train():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Only .xlsx and .csv files allowed'}), 400

        filename = secure_filename(file.filename)
        filepath = UPLOAD_FOLDER / filename
        file.save(filepath)

        try:
            _read_dataset(str(filepath))
            summary = _build_dataset_summary(filename, str(filepath))
            LATEST_STATE['selected_dataset'] = filename
            return jsonify({
                'success': True,
                'message': 'Training dataset uploaded successfully',
                'dataset': summary,
                'selected_dataset': filename,
                'datasets': _datasets_payload(),
            }), 201
        except Exception as exc:
            if filepath.exists():
                filepath.unlink()
            return jsonify({'success': False, 'error': f'Invalid file format: {str(exc)}'}), 400
    except Exception as exc:
        print(f'Error in upload_train: {traceback.format_exc()}')
        return jsonify({'success': False, 'error': str(exc)}), 500


@app.route('/upload-test', methods=['POST'])
def upload_test():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        filename, filepath = _save_uploaded_test_file(request.files['file'])
        preview_df = _read_dataset(str(filepath))

        selected_dataset = request.form.get('dataset_name') or LATEST_STATE.get('selected_dataset')
        if selected_dataset:
            LATEST_STATE['selected_dataset'] = selected_dataset
        LATEST_STATE['latest_test_file'] = filename

        return jsonify({
            'success': True,
            'message': 'Test dataset uploaded successfully',
            'selected_dataset': LATEST_STATE.get('selected_dataset'),
            'test_file': {
                'name': filename,
                'rows': int(len(preview_df)),
                'columns': list(preview_df.columns),
            },
        }), 201
    except Exception as exc:
        print(f'Error in upload_test: {traceback.format_exc()}')
        return jsonify({'success': False, 'error': str(exc)}), 500


@app.route('/train', methods=['POST'])
def train_alias():
    try:
        dataset_name = request.form.get('dataset_name') or request.form.get('train_dataset')
        if dataset_name:
            LATEST_STATE['selected_dataset'] = dataset_name

        LATEST_STATE['training_status'] = 'running'
        response, status_code = run_model_pipeline()
        payload = response.get_json()

        if payload.get('success'):
            payload.setdefault('message', 'Training completed successfully')
            LATEST_STATE['latest_results'] = payload
            LATEST_STATE['training_status'] = 'completed'
            LATEST_STATE['selected_dataset'] = payload.get('metadata', {}).get('selected_train_dataset') or dataset_name
        else:
            LATEST_STATE['training_status'] = 'failed'

        payload['selected_dataset'] = LATEST_STATE.get('selected_dataset')
        payload['training_status'] = LATEST_STATE.get('training_status')
        payload['prediction_status'] = LATEST_STATE.get('prediction_status')
        return jsonify(payload), status_code
    except Exception as exc:
        LATEST_STATE['training_status'] = 'failed'
        print(f'Error in train_alias: {traceback.format_exc()}')
        return jsonify({'success': False, 'error': str(exc), 'training_status': 'failed'}), 500


@app.route('/predict', methods=['POST'])
def predict_alias():
    try:
        dataset_name = request.form.get('dataset_name') or request.form.get('train_dataset')
        if dataset_name:
            LATEST_STATE['selected_dataset'] = dataset_name

        if 'test_file' in request.files and request.files['test_file'].filename:
            LATEST_STATE['latest_test_file'] = secure_filename(request.files['test_file'].filename)

        LATEST_STATE['prediction_status'] = 'running'
        response, status_code = run_model_pipeline()
        payload = response.get_json()

        if payload.get('success'):
            payload.setdefault('message', 'Prediction completed successfully')
            LATEST_STATE['latest_results'] = payload
            LATEST_STATE['prediction_status'] = 'completed'
            LATEST_STATE['selected_dataset'] = payload.get('metadata', {}).get('selected_train_dataset') or dataset_name
        else:
            LATEST_STATE['prediction_status'] = 'failed'

        payload['selected_dataset'] = LATEST_STATE.get('selected_dataset')
        payload['latest_test_file'] = LATEST_STATE.get('latest_test_file')
        payload['training_status'] = LATEST_STATE.get('training_status')
        payload['prediction_status'] = LATEST_STATE.get('prediction_status')
        return jsonify(payload), status_code
    except Exception as exc:
        LATEST_STATE['prediction_status'] = 'failed'
        print(f'Error in predict_alias: {traceback.format_exc()}')
        return jsonify({'success': False, 'error': str(exc), 'prediction_status': 'failed'}), 500


@app.route('/results', methods=['GET'])
def get_results():
    return jsonify(_results_payload()), 200


@app.route('/')
def serve_index():
    index_path = FRONTEND_BUILD / 'index.html'
    if index_path.exists():
        return send_file(index_path)
    return jsonify({'message': 'Frontend not built. Run: cd frontend && npm install && npm run build'}), 503


@app.route('/<path:filename>')
def serve_spa_fallback(filename):
    if filename.startswith('api/'):
        return jsonify({'error': 'Not found', 'message': f'API endpoint not found: /{filename}'}), 404

    full_path = (FRONTEND_BUILD / filename).resolve()

    if not str(full_path).startswith(str(FRONTEND_BUILD.resolve())):
      return jsonify({'error': 'Forbidden'}), 403

    if full_path.is_file():
        return send_file(full_path, conditional=True)

    index_file = FRONTEND_BUILD / 'index.html'
    if index_file.is_file():
        return send_file(index_file, mimetype='text/html')

    return jsonify({'error': 'Frontend not found'}), 503


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': str(error)}), 404


@app.errorhandler(500)
def internal_error(error):
    print(f'Server error: {traceback.format_exc()}')
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500


if __name__ == '__main__':
    print('\n=== REGISTERED ROUTES ===')
    for rule in app.url_map.iter_rules():
        print(f'{rule.rule} -> {rule.endpoint}')
    print('=========================\n')
    app.run(debug=False, host='0.0.0.0', port=5000)
