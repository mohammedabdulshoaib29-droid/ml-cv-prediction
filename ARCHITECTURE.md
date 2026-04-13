# System Architecture & Design

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND (Port 3000)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────┐  ┌──────────────────────┐             │
│  │ DatasetManager     │  │ ModelTrainer         │             │
│  │ - Upload files     │  │ - Upload test data   │             │
│  │ - List datasets    │  │ - Start training     │             │
│  │ - Show preview     │  │ - Display progress   │             │
│  └────────────────────┘  └──────────────────────┘             │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ModelComparison                                            │ │
│  │ - Show best model       - Display metrics                  │ │
│  │ - Compare R² scores     - Feature importance bars          │ │
│  │ - Actual vs Predicted   - Training history                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP/CORS
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FLASK BACKEND (Port 5000)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  API ENDPOINTS                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ /api/datasets/list          - List all datasets            │ │
│  │ /api/datasets/upload        - Upload new dataset           │ │
│  │ /api/datasets/preview/{id}  - Get dataset stats            │ │
│  │ /api/datasets/delete/{id}   - Delete dataset               │ │
│  │                                                             │ │
│  │ /api/models/train           - Train all 3 models           │ │
│  │ /api/models/compare         - Compare models               │ │
│  │                                                             │ │
│  │ /api/health/status          - App health                   │ │
│  │ /api/health/ready           - Readiness check              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  BUSINESS LOGIC                                                │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌──────────────┐        │
│  │ ANN    │  │ Random │  │XGBoost │  │ Orchestrator │        │
│  │Model  │  │ Forest │  │ Model  │  │ - Coordinate │        │
│  │Training│  │Model  │  │Training│  │ - Evaluate   │        │
│  │        │  │Training│  │        │  │ - Compare    │        │
│  └────────┘  └────────┘  └────────┘  └──────────────┘        │
│                                                                 │
│  DATA LAYER                                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ File System Storage                                        │ │
│  │ └─ datasets/                                               │ │
│  │    ├─ training_data.xlsx                                   │ │
│  │    ├─ material_1.csv                                       │ │
│  │    └─ material_2.xlsx                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Upload Dataset Flow
```
User uploads file
    ↓
FileUploader (Frontend)
    ↓
POST /api/datasets/upload
    ↓
Flask receives multipart form
    ↓
Validate file (type, size)
    ↓
Read file (xlsx/csv)
    ↓
Validate data (empty, format)
    ↓
Save to backend/datasets/
    ↓
Return metadata to frontend
    ↓
Update dataset dropdown
```

### Model Training Flow
```
Select training dataset + Upload test data
    ↓
Click "Start Training"
    ↓
POST /api/models/train
    ↓
Load training dataset from disk
    ↓
Load test dataset from upload
    ↓
orchestrator.train_all_models()
    ├─ run_ann(train_df, test_df)
    │  ├─ Data preprocessing
    │  │  ├─ Drop NaNs
    │  │  ├─ Scale features (RobustScaler)
    │  │  ├─ Scale target (StandardScaler)
    │  ├─ Build model (3 dense layers + dropout)
    │  ├─ Train (100 epochs, early stopping)
    │  ├─ Predict on test set
    │  ├─ Evaluate (R², RMSE, MAE)
    │  ├─ Calculate capacitance profile
    │  └─ Return results
    │
    ├─ run_rf(train_df, test_df)
    │  ├─ Data preprocessing (same as above)
    │  ├─ Train Random Forest (200 estimators)
    │  ├─ Get feature importance
    │  ├─ Evaluate metrics
    │  └─ Return results
    │
    └─ run_xgb(train_df, test_df)
       ├─ Data preprocessing
       ├─ Train XGBoost (200 rounds)
       ├─ Get feature importance
       ├─ Evaluate metrics
       └─ Return results
    ↓
Compare R² scores, identify best
    ↓
Format response JSON
    ↓
Return to frontend
    ↓
Display in ModelComparison component
```

---

## Component Architecture

### Backend Components

#### 1. main.py - Flask Application
```python
Flask(__name__)
├─ CORS() - Enable cross-origin requests
├─ Register blueprint: dataset_bp
├─ Register blueprint: model_bp
├─ Register blueprint: health_bp
└─ Error handlers (400, 404, 500)
```

#### 2. dataset_routes.py - Dataset Management
```python
dataset_bp (Blueprint)
├─ @app.route('/list', methods=['GET'])
│  └─ Load all .xlsx/.csv from datasets folder
├─ @app.route('/upload', methods=['POST'])
│  └─ Validate and save uploaded file
├─ @app.route('/preview/<name>', methods=['GET'])
│  └─ Load and analyze dataset
└─ @app.route('/delete/<name>', methods=['DELETE'])
   └─ Remove file from filesystem
```

#### 3. model_routes.py - Model Training
```python
model_bp (Blueprint)
├─ @app.route('/train', methods=['POST'])
│  ├─ Get train_dataset from form
│  ├─ Get test_file from upload
│  ├─ Load both datasets
│  ├─ Call orchestrator.train_all_models()
│  └─ Return formatted results
└─ @app.route('/compare', methods=['POST'])
   └─ Same flow, different response format
```

#### 4. Model Training Modules
```
ann.py
├─ run_ann(train_df, test_df)
│  ├─ Data cleaning & scaling
│  ├─ Build Sequential model
│  │  ├─ Dense(64, relu)
│  │  ├─ Dropout(0.2)
│  │  ├─ Dense(32, relu)
│  │  ├─ Dropout(0.1)
│  │  ├─ Dense(16, relu)
│  │  └─ Dense(1, linear)
│  ├─ Compile with Adam optimizer
│  ├─ Fit with early stopping
│  ├─ Evaluate on test set
│  └─ Calculate capacitance

rf.py
├─ run_rf(train_df, test_df)
│  ├─ Data cleaning
│  ├─ RandomForestRegressor(200 estimators)
│  ├─ Train and predict
│  ├─ Get feature importance
│  └─ Calculate metrics

xgb.py
├─ run_xgb(train_df, test_df)
│  ├─ Data cleaning
│  ├─ XGBRegressor(200 estimators)
│  ├─ Train and predict
│  ├─ Get feature importance
│  └─ Calculate metrics
```

### Frontend Components

#### 1. DatasetManager.js
```javascript
DatasetManager
├─ State: datasets[], selectedDataset, loading, showPreview
├─ Effects: loadDatasets() on mount
├─ Functions:
│  ├─ handleUploadDataset() - POST to /datasets/upload
│  ├─ handleSelectDataset() - Update parent state
│  ├─ handlePreviewDataset() - GET /datasets/preview
│  └─ handleDeleteDataset() - DELETE /datasets/delete
├─ UI:
│  ├─ Upload section with drag-drop
│  ├─ Dataset list with cards
│  ├─ Preview modal
│  └─ Action buttons
```

#### 2. ModelTrainer.js
```javascript
ModelTrainer
├─ Props: selectedDataset
├─ State: testFile, training, results, error
├─ Functions:
│  ├─ handleTestFileChange() - Set test file
│  ├─ handleTrainModels() - POST /models/train
│  └─ Error display
├─ UI:
│  ├─ Test file upload
│  ├─ Loading spinner
│  └─ Training button
└─ Passes results to ModelComparison
```

#### 3. ModelComparison.js
```javascript
ModelComparison
├─ Props: results from training
├─ State: selectedModel
├─ Effects: Set first model on results change
├─ Rendering:
│  ├─ Best model card
│  ├─ Performance charts (R², RMSE)
│  ├─ Model tabs
│  ├─ Selected model details:
│  │  ├─ Metrics grid (R², RMSE, MAE, Capacitance)
│  │  ├─ Sample info
│  │  ├─ Prediction plot
│  │  ├─ Capacitance profile
│  │  ├─ Feature importance bars
│  │  └─ Training history
│  └─ Error display
```

#### 4. PerformanceChart.js
```javascript
PerformanceChart
├─ Props: labels[], data[], title, color, type
├─ Renders:
│  ├─ BarChart (for R², RMSE, MAE)
│  └─ LineChart (optional for trends)
└─ Uses Recharts library
```

#### 5. PredictionPlot.js
```javascript
PredictionPlot
├─ Props: actual[], predicted[], modelName
├─ Renders: ScatterChart of actual vs predicted
└─ Uses Recharts library
```

---

## Data Structures

### Dataset Response
```json
{
  "success": true,
  "datasets": [
    {
      "name": "BiFeO3_dataset.xlsx",
      "size": 524288,
      "rows": 5000,
      "columns": ["Potential", "OXIDATION", ...],
      "cols_count": 7
    }
  ]
}
```

### Model Training Response
```json
{
  "success": true,
  "models": {
    "ANN": {
      "success": true,
      "model": "ANN",
      "metrics": {
        "r2_score": 0.9638,
        "rmse": 0.000334,
        "mae": 0.000250,
        "train_samples": 3500,
        "test_samples": 1500
      },
      "predictions": {
        "actual": [100.5, 102.3, ...],
        "predicted": [101.2, 103.1, ...]
      },
      "best_concentration": 5.2,
      "best_capacitance": 180.5,
      "capacitance_profile": {
        "concentrations": [0, 0.5, 1.0, ...],
        "capacitance_values": [80.0, 95.2, ...]
      }
    },
    "RandomForest": {...},
    "XGBoost": {...}
  },
  "best_model": {
    "name": "XGBoost",
    "r2_score": 0.9919,
    "result": {...}
  }
}
```

---

## Data Processing Pipeline

### Step 1: Data Loading
```python
# Load from Excel or CSV
train_df = pd.read_excel(filepath)  # or pd.read_csv()
test_df = pd.read_excel(test_filepath)
```

### Step 2: Column Selection
```python
required_cols = predictors + [target]
train_df = train_df[required_cols]
test_df = test_df[required_cols]
```

### Step 3: Missing Value Handling
```python
# Numeric columns: median
for col in numeric_cols:
    df[col].fillna(df[col].median(), inplace=True)

# Categorical columns: mode
for col in categorical_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)
```

### Step 4: Feature Scaling
```python
feature_scaler = RobustScaler()
X_train_scaled = feature_scaler.fit_transform(X_train)
X_test_scaled = feature_scaler.transform(X_test)
```

### Step 5: Target Scaling (ANN only)
```python
target_scaler = StandardScaler()
y_train_scaled = target_scaler.fit_transform(y_train.reshape(-1, 1))
```

### Step 6: Model Training & Prediction
```python
model.fit(X_train_scaled, y_train_scaled)
y_pred_scaled = model.predict(X_test_scaled)
y_pred_original = target_scaler.inverse_transform(y_pred_scaled)
```

### Step 7: Evaluation
```python
r2 = r2_score(y_test_original, y_pred_original)
rmse = np.sqrt(mean_squared_error(y_test_original, y_pred_original))
mae = mean_absolute_error(y_test_original, y_pred_original)
```

---

## Error Handling Strategy

### Frontend Error Handling
```javascript
try {
  const response = await axios.get(url)
  if (response.data.success) {
    // Process success
  } else {
    setError(response.data.error)
  }
} catch (err) {
  setError(err.response?.data?.error || err.message)
  console.error('Detailed error:', err)
}
```

### Backend Error Handling
```python
try:
    # Process request
    return jsonify({'success': True, ...}), 200
except ValueError as e:
    print(f"Validation error: {traceback.format_exc()}")
    return jsonify({'success': False, 'error': str(e)}), 400
except Exception as e:
    print(f"Server error: {traceback.format_exc()}")
    return jsonify({'success': False, 'error': str(e)}), 500
```

---

## Performance Optimizations

### Frontend
1. **Code Splitting**: Lazy load components
2. **Optimization**: CSS optimization, minimal JS
3. **Caching**: React component memoization
4. **Bundle Size**: ~47 kB (optimized)

### Backend
1. **Parallel Processing**: Multi-threaded model training
2. **Efficient Scaling**: RobustScaler (O(n) complexity)
3. **Early Stopping**: ANN stops when validation loss plateaus
4. **Memory Management**: Explicit garbage collection

### Database
1. **File System**: Simple, fast for file storage
2. **Caching**: No redundant file reads

---

## Scalability Considerations

### Current Capacities
- Max dataset size: 50MB
- Concurrent uploads: Limited by server memory
- Model training: Sequential (one per machine)
- Users: Single machine deployment

### Future Scaling Options
1. **Database**: Move to PostgreSQL for metadata
2. **Distributed Training**: Parallel model training
3. **Caching**: Redis for model results
4. **Load Balancing**: Nginx proxy
5. **Containerization**: Docker for easy deployment
6. **Cloud**: Deploy to AWS, GCP, Azure

---

## Security Architecture

### Input Validation
```
File Upload → Validate type → Validate size → Scan content
```

### CORS Policy
```
Allow: http://localhost:3000 (development)
Can be restricted in production
```

### File Safety
```
- Filename sanitization with secure_filename()
- Size limits (50MB max)
- No path traversal attacks
```

### Error Messages
```
Generic messages shown to user
Detailed traces logged server-side only
```

---

## Monitoring & Debugging

### Logging Points
1. **Model Training**: Print progress
2. **Data Processing**: Log preprocessing steps
3. **API Calls**: Log request/response
4. **Errors**: Full traceback to console

### Frontend Debugging
1. **Browser DevTools**: Console, Network, React Components
2. **Axios Interceptors**: Log all HTTP requests/responses
3. **State Logging**: Redux DevTools (if added later)

### Backend Debugging
1. **Flask Debug Mode**: Auto-reload, debugger
2. **Print Statements**: Strategic logging
3. **Traceback**: Full error traces

---

## Deployment Considerations

### Development
- Local: Flask development server, hot reload
- Ports: 5000 (backend), 3000 (frontend)

### Production
- Framework: Gunicorn/uWSGI for Flask
- Frontend: npm build → static files
- Server: Nginx reverse proxy
- Environment: Docker container recommended

---

## Testing Strategy (Future)

```
Unit Tests
├─ Data preprocessing functions
├─ Model training logic
├─ API endpoint responses
└─ React component rendering

Integration Tests
├─ Full dataset upload flow
├─ Model training end-to-end
├─ API interactions
└─ Frontend/Backend communication

E2E Tests (Selenium)
├─ Complete user workflows
├─ Model training success
└─ Results display
```

---

This architecture provides a solid foundation for a scalable, maintainable ML web application!
