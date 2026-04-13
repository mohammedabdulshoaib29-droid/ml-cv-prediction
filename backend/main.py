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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from routes.dataset_routes import router as dataset_router
from routes.prediction_routes import router as prediction_router
from routes.cv_prediction_routes import router as cv_prediction_router
import os
from pathlib import Path
from dotenv import load_dotenv
import sys
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

# Create datasets directory if it doesn't exist
import os
from pathlib import Path as PathlibPath

BACKEND_DIR = PathlibPath(__file__).parent
DATASETS_DIR = BACKEND_DIR / "datasets"
DATASETS_DIR.mkdir(parents=True, exist_ok=True)

# Startup verification
print("🚀 Initializing ML-CV Prediction API...")
try:
    from models.ann import run_ann
    from models.rf import run_rf
    from models.xgb import run_xgb
    from models.comparison import run_all_models
    print("✅ All ML models imported successfully")
except Exception as e:
    print(f"⚠️  Warning during model import: {e}")
    print("API will attempt to use models, but they may fail")

# Generate sample datasets if they don't exist
def generate_sample_cv_datasets():
    """Generate sample CV analysis datasets for testing"""
    
    # Check if sample datasets already exist
    sample_file = DATASETS_DIR / "sample_cv_train.csv"
    if sample_file.exists():
        print("✅ Sample datasets already exist")
        return
    
    print("📊 Generating sample CV analysis datasets...")
    
    # Generate sample CV training data
    np.random.seed(42)
    n_samples = 100
    
    cv_data = {
        "Potential": np.linspace(-0.5, 1.0, n_samples),
        "OXIDATION": np.random.uniform(0.5, 2, n_samples),
        "Zn/Co_Conc": np.random.uniform(20, 80, n_samples),
        "SCAN_RATE": np.random.uniform(10, 100, n_samples),
        "ZN": np.random.uniform(0.1, 1, n_samples),
        "CO": np.random.uniform(0.1, 1, n_samples),
        "Current": np.random.uniform(0.001, 0.1, n_samples)
    }
    
    train_df = pd.DataFrame(cv_data)
    train_df.to_csv(DATASETS_DIR / "sample_cv_train.csv", index=False)
    print(f"✅ Created sample_cv_train.csv ({n_samples} samples)")
    
    # Generate sample CV test data
    test_data = {
        "Potential": np.linspace(-0.5, 1.0, 50),
        "OXIDATION": np.random.uniform(0.5, 2, 50),
        "Zn/Co_Conc": np.random.uniform(20, 80, 50),
        "SCAN_RATE": np.random.uniform(10, 100, 50),
        "ZN": np.random.uniform(0.1, 1, 50),
        "CO": np.random.uniform(0.1, 1, 50),
        "Current": np.random.uniform(0.001, 0.1, 50)
    }
    
    test_df = pd.DataFrame(test_data)
    test_df.to_csv(DATASETS_DIR / "sample_cv_test.csv", index=False)
    print(f"✅ Created sample_cv_test.csv (50 samples)")

# Generate sample datasets on startup
try:
    generate_sample_cv_datasets()
except Exception as e:
    print(f"⚠️  Warning: Could not generate sample datasets: {e}")

app = FastAPI(
    title="ML-Based CV Behavior Prediction",
    description="Advanced machine learning for CV analysis and behavior forecasting",
    version="1.0.0"
)

# Add compression middleware for faster responses
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add CORS middleware - simplified since frontend is now on same server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(dataset_router, prefix="/api", tags=["datasets"])
app.include_router(prediction_router, prefix="/api", tags=["predictions"])
app.include_router(cv_prediction_router, prefix="/api", tags=["cv-predictions"])

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "ML API is running"}

# Serve static files from React build directory
# Check if frontend build exists
build_dir = Path(__file__).parent.parent / "frontend" / "build"

if build_dir.exists():
    app.mount("/", StaticFiles(directory=str(build_dir), html=True), name="static")
else:
    # Development fallback message
    @app.get("/")
    def root():
        return {
            "message": "ML-Based CV Behavior Prediction API",
            "api_docs": "/docs",
            "note": "Frontend not built. Run: cd frontend && npm install && npm run build"
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
