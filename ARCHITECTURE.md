# 🏗️ ML Web Application - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                                │
│                    (http://localhost:3000)                          │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ HTTP/CORS
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       REACT FRONTEND                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ DatasetSelector  │  │  FileUploader    │  │  ModelComparison │ │
│  │ - Dropdown list  │  │ - Upload train   │  │ - Bar chart      │ │
│  │ - Upload section │  │ - Upload test    │  │ - Line chart     │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
│  ┌──────────────────┐  ┌──────────────────┐                        │
│  │ ResultsDisplay   │  │ Model Selection  │                        │
│  │ - Metrics        │  │ - Single/All     │                        │
│  │ - Predictions    │  │ - Download CSV   │                        │
│  └──────────────────┘  └──────────────────┘                        │
│                                                                     │
│                         API Service Layer                          │
│                    (services/api.js)                               │
│  - axios HTTP client                                              │
│  - Error handling                                                 │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ REST API (JSON)
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                                │
│                  (http://localhost:8000)                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────┐                                      │
│  │ ROUTE LAYER              │                                      │
│  ├──────────────────────────┤                                      │
│  │ GET  /api/datasets       │                                      │
│  │ POST /api/upload-dataset │                                      │
│  │ DELETE /api/datasets/{id}│                                      │
│  │ POST /api/predict        │                                      │
│  │ GET  /api/predict/status │                                      │
│  └──────────────────────────┘                                      │
│           │      │      │                                          │
│           ▼      ▼      ▼                                          │
│  ┌──────────────────────────┐                                      │
│  │ UTILITY LAYER            │                                      │
│  ├──────────────────────────┤                                      │
│  │ preprocessing.py         │                                      │
│  │ - Handle missing values   │                                      │
│  │ - Categorical encoding    │                                      │
│  │ - Feature scaling         │                                      │
│  │ - Target encoding         │                                      │
│  │                          │                                      │
│  │ evaluation.py            │                                      │
│  │ - Calculate metrics       │                                      │
│  │ - Accuracy, RMSE, MAE    │                                      │
│  └──────────────────────────┘                                      │
│           │                                                        │
│           ▼                                                        │
│  ┌──────────────────────────┐                                      │
│  │ MODEL LAYER              │                                      │
│  ├──────────────────────────┤                                      │
│  │ ml_models.py             │                                      │
│  │                          │                                      │
│  │ ┌──────────────────────┐ │                                      │
│  │ │ ANN (TensorFlow)     │ │                                      │
│  │ │ - MLPClassifier      │ │                                      │
│  │ │ - MLPRegressor       │ │                                      │
│  │ └──────────────────────┘ │                                      │
│  │ ┌──────────────────────┐ │                                      │
│  │ │ Random Forest        │ │                                      │
│  │ │ - Classification RF  │ │                                      │
│  │ │ - Regression RF      │ │                                      │
│  │ └──────────────────────┘ │                                      │
│  │ ┌──────────────────────┐ │                                      │
│  │ │ XGBoost              │ │                                      │
│  │ │ - Classification XGB │ │                                      │
│  │ │ - Regression XGB     │ │                                      │
│  │ └──────────────────────┘ │                                      │
│  │                          │                                      │
│  │ Methods:                 │                                      │
│  │ - train(X, y)           │                                      │
│  │ - predict(X)            │                                      │
│  │ - get_feature_importance │                                      │
│  └──────────────────────────┘                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ File I/O
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA STORAGE LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐      ┌──────────────────┐                   │
│  │  datasets/       │      │  Temp Files      │                   │
│  │ (Training Data)  │      │ (Test Data)      │                   │
│  │ - .csv files     │      │ - Uploaded       │                   │
│  │ - .xlsx files    │      │ - Processing     │                   │
│  │                  │      │ - Deleted after  │                   │
│  └──────────────────┘      └──────────────────┘                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Upload Dataset Flow
```
User selects file
       ↓
Frontend: FileInput component
       ↓
axios POST /upload-dataset
       ↓
Backend: dataset_routes.validate_file()
       ↓
Save to datasets/ directory
       ↓
Return filename + size
       ↓
Frontend: Update dataset dropdown
```

### Prediction Flow
```
User clicks "Run Prediction"
       ↓
Frontend: Get selected dataset + uploaded test file
       ↓
axios POST /predict (FormData)
       ↓
Backend: Load and preprocess training data
       ↓
Backend: Load and preprocess test data
       ↓
Backend: Initialize MLModels (MLPClassifier/Regressor, RF, XGB)
       ↓
Backend: models.train(X_train, y_train)
       ↓
Backend: predictions = models.predict(X_test)
       ↓
Backend: metrics = evaluator.evaluate(y_test, predictions)
       ↓
Backend: Return {models, metrics, feature_importance}
       ↓
Frontend: Display results + charts
       ↓
User can download CSV
```

---

## Component Interaction Diagram

```
App.js (Main)
├── State Management
│   ├── selectedDataset
│   ├── testFile
│   ├── results
│   ├── loading
│   ├── error
│   └── modelType
│
└── Components
    ├── DatasetSelector
    │   ├── Props: onDatasetSelect, onUploadSuccess
    │   └── Calls: datasetService.getDatasets()
    │              datasetService.uploadDataset()
    │
    ├── FileUploader (for test data)
    │   ├── Props: onFileSelect, label
    │   └── Returns: file object
    │
    ├── Model Selection Radio Group
    │   └── Props: modelType state
    │
    ├── Predict Button
    │   └── Calls: predictionService.predict()
    │
    ├── ResultsDisplay
    │   ├── Props: results, loading, error
    │   └── Features:
    │       - Shows metrics (accuracy, RMSE, MAE)
    │       - CSV download
    │
    └── ModelComparison
        ├── Props: results
        └── Charts:
            - Bar chart (model comparison)
            - Line chart (predictions)
            - Feature importance boxes
```

---

## API Request/Response Examples

### Get Datasets
```bash
Request:  GET http://localhost:8000/api/datasets
Response: 
{
  "datasets": [
    {
      "name": "BiFeO3_dataset.xlsx",
      "size": 15234,
      "type": ".xlsx"
    },
    {
      "name": "MnO2_dataset.csv",
      "size": 12456,
      "type": ".csv"
    }
  ]
}
```

### Upload Dataset
```bash
Request:  POST http://localhost:8000/api/upload-dataset
Content-Type: multipart/form-data
Body: file=[binary]

Response:
{
  "message": "Dataset uploaded successfully",
  "filename": "Graphene_dataset.xlsx",
  "size": 18234
}
```

### Make Prediction
```bash
Request:  POST http://localhost:8000/api/predict
Content-Type: multipart/form-data
Body: 
  dataset_name=BiFeO3_dataset.xlsx
  test_file=[binary]
  model_type=all

Response:
{
  "task_type": "regression",
  "training_dataset": "BiFeO3_dataset.xlsx",
  "test_samples": 50,
  "models": {
    "ann": {
      "predictions": [10.45, 11.23, 12.10, ...],
      "all_predictions": [...],
      "accuracy": 0.9234,
      "rmse": 0.1234,
      "mae": 0.0987,
      "training_status": "trained"
    },
    "rf": { ... },
    "xgb": { ... }
  },
  "feature_importance": {
    "rf": [["Feature1", 0.35], ["Feature2", 0.28], ...],
    "xgb": [["Feature3", 0.42], ["Feature1", 0.31], ...]
  }
}
```

---

## File Processing Pipeline

```
Input File (.csv, .xlsx)
       ↓
pandas.read_csv() or pd.read_excel()
       ↓
Handle missing values (mean for numeric, mode for categorical)
       ↓
Separate features (X) and target (y)
       ↓
Encode categorical variables (LabelEncoder)
       ↓
Standardize features (StandardScaler)
       ↓
Output: X (normalized), y (encoded)
       ↓
Train/Predict: Pass to ML models
```

---

## Technology Stack Layers

```
┌─────────────────────────────────────────────┐
│      PRESENTATION LAYER (React)             │
│  - User Interface Components                │
│  - Forms, Dropdowns, Charts                 │
│  - CSS Styling                              │
└─────────────────────────────────────────────┘
                   │
┌─────────────────────────────────────────────┐
│    API/COMMUNICATION LAYER (HTTP)           │
│  - Axios HTTP Client                        │
│  - CORS Middleware                          │
│  - Request/Response Handling                │
└─────────────────────────────────────────────┘
                   │
┌─────────────────────────────────────────────┐
│    BUSINESS LOGIC LAYER (FastAPI)           │
│  - API Routes                               │
│  - Data Preprocessing                       │
│  - Model Evaluation                         │
│  - Error Handling                           │
└─────────────────────────────────────────────┘
                   │
┌─────────────────────────────────────────────┐
│    ML LAYER (scikit-learn, TF, XGBoost)     │
│  - Model Training                           │
│  - Prediction                               │
│  - Feature Importance                       │
└─────────────────────────────────────────────┘
                   │
┌─────────────────────────────────────────────┐
│    DATA LAYER (Pandas, File System)         │
│  - Dataset Loading                          │
│  - Data Storage                             │
│  - Temp File Management                     │
└─────────────────────────────────────────────┘
```

---

## Deployment Architecture (Optional)

```
┌─────────────────┐
│   End Users     │
│   (Browsers)    │
└────────┬────────┘
         │
    HTTPS/80
         │
┌────────▼─────────────────────────────┐
│        Web Server (nginx/Apache)     │
│     Serves React static files        │
│  (Load balancer + SSL termination)   │
└────────┬─────────────────────────────┘
         │
    HTTP/8000
         │
┌────────▼──────────────────────────────┐
│   API Server (Gunicorn + FastAPI)     │
│   - Load balanced                     │
│   - Multiple worker processes         │
│   - Environment isolated              │
└────────┬──────────────────────────────┘
         │
┌────────▼──────────────────────────────┐
│   Persistent Storage                  │
│   - Datasets (S3/Cloud Storage)       │
│   - Logs                              │
│   - Optional: Database (Results)      │
└───────────────────────────────────────┘
```

---

## Security Layers

```
Frontend
  ↓
[CORS Check] ← Validates origin
  ↓
FastAPI
  ↓
[Input Validation] ← Check file types, sizes
  ↓
[Error Handling] ← No sensitive data in errors
  ↓
Filesystem
  ↓
[File Sanitization] ← Safe filename handling
  ↓
Data Processing
  ↓
[Temp File Cleanup] ← No leftover data
```

---

## Scalability Considerations

**Current Setup (Single Machine):**
- Good for: Development, Testing, Small teams
- Limitation: Max 1-2 concurrent predictions

**Scalable Setup (Future):**
1. **Horizontal Scaling:**
   - Multiple API server instances
   - Load balancer (nginx/ALB)
   - Shared dataset storage (S3/Cloud)

2. **Background Processing:**
   - Celery + Redis for async jobs
   - Queue heavy predictions
   - Return results via WebSocket

3. **Model Management:**
   - Model versioning
   - A/B testing framework
   - Model registry

4. **Monitoring:**
   - Application monitoring (New Relic, DataDog)
   - Error tracking (Sentry)
   - Performance metrics (Prometheus)

---

## Performance Metrics

| Operation | Typical Time |
|-----------|---|
| Load dataset | 0.5-2 sec |
| Train ANN | 2-5 sec |
| Train RF | 1-3 sec |
| Train XGB | 2-6 sec |
| Make predictions | 0.5-2 sec |
| Total workflow | 5-20 sec |

*Times depend on: Dataset size, Hardware, Model complexity*

---

**Architecture Design Principles:**
- ✅ Separation of concerns (routes, utils, models)
- ✅ Reusable components (React components)
- ✅ Service layer abstraction (api.js)
- ✅ Error handling at each layer
- ✅ Scalable structure
- ✅ Clean code with comments
- ✅ CORS security (configurable)
