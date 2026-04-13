"""
ML Web App - Main Flask Application
Capacitance Prediction with Dataset Management & Model Evaluation
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import traceback
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Create Flask app - disable automatic static serving
app = Flask(__name__, static_folder=None)  # Disable Flask's automatic /static routing
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


# Static file serving for React frontend (root and catch-all routes)


@app.route('/')
def serve_index():
    """Serve the React index.html file"""
    index_path = os.path.join(FRONTEND_BUILD, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_BUILD, 'index.html')
    return jsonify({'message': 'Frontend not built. Run: cd frontend && npm install && npm run build'}), 503


@app.route('/<path:filename>')
def serve_spa_fallback(filename):
    """Serve static files or index.html for SPA routing"""
    # Skip API routes - let blueprints handle them
    if filename.startswith('api/'):
        return jsonify({'error': 'Not found', 'message': f'API endpoint not found: /{filename}'}), 404
    
    # Try to serve the requested file
    full_path = os.path.abspath(os.path.join(FRONTEND_BUILD, filename))
   
    # Security: prevent directory traversal
    if not full_path.startswith(os.path.abspath(FRONTEND_BUILD)):
        return jsonify({'error': 'Forbidden'}), 403
    
    # Serve static files or fall back to index.html for SPA routing
    if os.path.isfile(full_path):
        return send_file(full_path, conditional=True)
    
    # For any non-existent route, serve index.html (SPA routing)
    index_file = os.path.join(FRONTEND_BUILD, 'index.html')
    if os.path.isfile(index_file):
        return send_file(index_file, mimetype='text/html')
    
    return jsonify({'error': 'Frontend not found'}), 503


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
    print("\n=== REGISTERED ROUTES ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule.rule} -> {rule.endpoint}")
    print("=========================\n")
    app.run(debug=False, host='0.0.0.0', port=5000)
