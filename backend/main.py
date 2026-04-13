"""
ML Web App - Main Flask Application
Capacitance Prediction with Dataset Management & Model Evaluation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'datasets')
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Import routes
from routes.dataset_routes import dataset_bp
from routes.model_routes import model_bp
from routes.health_routes import health_bp

# Register blueprints
app.register_blueprint(dataset_bp, url_prefix='/api/datasets')
app.register_blueprint(model_bp, url_prefix='/api/models')
app.register_blueprint(health_bp, url_prefix='/api/health')


@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad request', 'message': str(e)}), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found', 'message': str(e)}), 404


@app.errorhandler(500)
def internal_error(e):
    print(f"Server error: {traceback.format_exc()}")
    return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
