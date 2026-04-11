# ML Web Application - Full Stack Setup Guide

## 📋 Project Overview

A complete full-stack machine learning web application that allows users to:
- Upload and manage training datasets
- Select a training dataset from dropdown
- Upload test datasets
- Train multiple ML models (ANN, RF, XGBoost)
- View predictions and performance metrics
- Visualize model comparisons

## 📁 Project Structure

```
ml-web-app/
├── backend/
│   ├── main.py                          # FastAPI server
│   ├── requirements.txt                 # Python dependencies
│   ├── models/
│   │   └── ml_models.py                 # ML model implementations
│   ├── routes/
│   │   ├── dataset_routes.py            # Dataset API endpoints
│   │   └── prediction_routes.py         # Prediction API endpoints
│   ├── utils/
│   │   ├── preprocessing.py             # Data preprocessing
│   │   └── evaluation.py                # Model evaluation metrics
│   └── datasets/                        # Stored training datasets (auto-created)
│
└── frontend/
    ├── package.json                     # Node.js dependencies
    ├── public/
    │   └── index.html                   # Main HTML file
    └── src/
        ├── App.js                       # Main App component
        ├── App.css                      # App styling
        ├── index.js                     # React entry point
        ├── index.css                    # Global styles
        ├── services/
        │   └── api.js                   # API service (axios)
        ├── components/
        │   ├── DatasetSelector.js       # Dataset selection component
        │   ├── FileUploader.js          # File upload component
        │   ├── ResultsDisplay.js        # Results display component
        │   └── ModelComparison.js       # Visualization component (Recharts)
        └── styles/
            ├── DatasetSelector.css
            ├── FileUploader.css
            ├── ResultsDisplay.css
            └── ModelComparison.css
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run FastAPI server:**
   ```bash
   python main.py
   ```
   
   Or with uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Server will be available at: `http://localhost:8000`
   API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

   Frontend will open at: `http://localhost:3000`

## 📊 API Endpoints

### Dataset Management

**GET /api/datasets**
- Returns list of available training datasets
- Response: `{ "datasets": [{ "name": "...", "size": ..., "type": "..." }] }`

**POST /api/upload-dataset**
- Upload a new training dataset
- Body: FormData with `file` field
- Response: `{ "message": "...", "filename": "...", "size": ... }`

**DELETE /api/datasets/{dataset_name}**
- Delete a dataset
- Response: `{ "message": "..." }`

### Predictions

**POST /api/predict**
- Train models and make predictions
- Body: FormData with:
  - `dataset_name`: Name of training dataset
  - `test_file`: Test dataset file
  - `model_type`: "all", "ann", "rf", or "xgb" (default: "all")
- Response:
  ```json
  {
    "task_type": "classification|regression",
    "training_dataset": "...",
    "test_samples": 100,
    "models": {
      "ann": {
        "predictions": [...],
        "all_predictions": [...],
        "accuracy": 0.95,
        "rmse": 0.12,
        "mae": 0.08,
        "training_status": "trained"
      },
      "rf": { ... },
      "xgb": { ... }
    },
    "feature_importance": {
      "rf": [...],
      "xgb": [...]
    }
  }
  ```

**GET /api/predict/status**
- Check if prediction service is ready
- Response: `{ "status": "ready" }`

## 📈 Features

### Core Features
✅ Dataset Management (upload, select, delete)
✅ Multiple ML Models (ANN, RF, XGBoost)
✅ Data Preprocessing (missing values, encoding, scaling)
✅ Model Evaluation (accuracy, RMSE, MAE, R² score)
✅ Responsive UI with real-time feedback

### Visualization
✅ Model Comparison Chart (Bar chart with accuracy, RMSE, MAE)
✅ Predictions Visualization (Line chart comparing predictions)
✅ Feature Importance Display (RF & XGBoost)

### User Experience
✅ Loading spinners during processing
✅ Error handling and user-friendly messages
✅ Download predictions as CSV
✅ Model selection (single or all)
✅ Clean, responsive UI (works on desktop & tablet)

### Bonus Features Implemented
✅ Single model OR all models selection
✅ Feature importance visualization
✅ Download predictions as CSV
✅ Automatic data preprocessing
✅ CORS support for cross-origin requests

## 📝 Example Dataset Format

Your datasets should have the following format:

### CSV Example (BiFeO3_dataset.csv)
```
feature1,feature2,feature3,feature4,target
1.2,3.4,5.6,7.8,10.5
2.1,3.9,5.2,7.1,11.2
3.5,4.2,6.1,8.3,12.1
...
```

### Excel Example (BiFeO3_dataset.xlsx)
| feature1 | feature2 | feature3 | feature4 | target |
|----------|----------|----------|----------|--------|
| 1.2      | 3.4      | 5.6      | 7.8      | 10.5   |
| 2.1      | 3.9      | 5.2      | 7.1      | 11.2   |
| 3.5      | 4.2      | 6.1      | 8.3      | 12.1   |

### Important Notes:
- First row should contain headers
- Target column can be named anything (last column is assumed as target if not found)
- Supports both numerical and categorical features
- Handles missing values automatically
- Both training and test data should follow the same structure

## 🔧 Configuration

### Backend Configuration

In `main.py`, you can modify:
- Host and port in `uvicorn.run()`
- CORS origins in the middleware
- API prefix path

In `models/ml_models.py`, you can adjust:
- ANN architecture (hidden_layer_sizes)
- Random Forest parameters (n_estimators)
- XGBoost parameters (n_estimators, learning_rate)

### Frontend Configuration

In `frontend/src/services/api.js`, modify:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

Change the port if your backend runs on a different port.

## 🧪 Testing the Application

1. **Prepare sample datasets:**
   - Create a CSV file with training data
   - Create a CSV file with test data

2. **Upload training dataset:**
   - Click "Upload New Training Dataset"
   - Select your CSV/Excel file
   - Click "Upload Dataset"

3. **Run prediction:**
   - Select the uploaded dataset from dropdown
   - Upload test dataset
   - Choose model type (all or specific)
   - Click "Run Prediction"

4. **View results:**
   - See accuracy metrics for each model
   - View sample predictions
   - Compare models in visualization charts
   - Download results as CSV

## 🐛 Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError"**
- Solution: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Error: "CORS error" in frontend**
- Solution: Check if backend is running and CORS is enabled in `main.py`

**Error: "Port already in use"**
- Solution: Change port: `uvicorn main:app --port 8001`

### Frontend Issues

**Error: "Cannot GET /api/datasets"**
- Check if backend is running on `http://localhost:8000`
- Verify API_BASE_URL in `frontend/src/services/api.js`

**Error: "npm start fails"**
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again

## 📦 Deployment

### Backend (Production)

1. Install production server:
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 main:app
   ```

3. Use environment variables for sensitive data (update `main.py` as needed)

### Frontend (Production)

1. Build production bundle:
   ```bash
   npm run build
   ```

2. Serve with a static server (e.g., nginx, or use Flask to serve)

3. Update API_BASE_URL to your production backend URL

## 📚 Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- Scikit-learn - ML preprocessing and Random Forest
- TensorFlow/Keras - Neural Network implementation
- XGBoost - Gradient boosting
- Pandas & NumPy - Data manipulation
- Uvicorn - ASGI server

**Frontend:**
- React 18 - UI library
- Axios - HTTP client
- Recharts - Data visualization
- React Spinners - Loading indicators
- CSS3 - Styling

## 📄 License

This project is open source and available for educational purposes.

## ✨ Enhancement Ideas

1. Add user authentication and profiles
2. Implement model caching to speed up predictions
3. Add cross-validation and hyperparameter tuning
4. Support for image datasets (CNN models)
5. Real-time dataset statistics dashboard
6. Model comparison metrics (precision, recall, F1)
7. Batch prediction on multiple test files
8. API key authentication
9. Database for storing results
10. Docker containerization for easy deployment

## 🤝 Support

For issues or questions, refer to the component-specific documentation or create an issue in your project repository.
