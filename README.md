# ML Web App - Capacitance Prediction System

A complete machine learning web application for predicting material-specific capacitance using multiple regression models with full dataset management and model evaluation.

## Features

### ✨ Core Features
- **Multi-Model Training**: ANN, Random Forest, XGBoost
- **Dataset Management**: Upload, store, and switch between multiple datasets
- **Train/Test Separation**: Strict separation for proper model evaluation
- **Model Comparison**: Side-by-side performance metrics
- **Interactive Visualizations**: Charts and graphs for insights
- **Detailed Results**: R², RMSE, MAE, and feature importance

### 🎯 ML Capabilities
- Artificial Neural Network with dropout regularization
- Random Forest with 200 estimators
- XGBoost with optimized parameters
- Automatic data preprocessing (scaling, cleaning)
- Capacitance profile calculation
- Feature importance analysis

### 🎨 UI Features
- Dataset dropdown selector
- Drag-and-drop file upload
- Real-time model training status
- Comparative model dashboard
- Performance metrics cards
- Interactive prediction plots
- Feature importance bars

## Tech Stack

### Backend
- **Framework**: Flask with CORS support
- **ML Libraries**: TensorFlow, scikit-learn, XGBoost
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn

### Frontend
- **Framework**: React
- **Charting**: Recharts
- **Styling**: CSS3
- **HTTP**: Axios

## System Architecture

```
ml-web-app/
├── backend/
│   ├── main.py              # Flask app entry point
│   ├── requirements.txt     # Python dependencies
│   ├── models/
│   │   ├── ann.py          # ANN model
│   │   ├── rf.py           # Random Forest model
│   │   ├── xgb.py          # XGBoost model
│   │   └── orchestrator.py # Model coordinator
│   ├── routes/
│   │   ├── dataset_routes.py   # Dataset management
│   │   ├── model_routes.py     # Model training
│   │   └── health_routes.py    # Health checks
│   └── datasets/           # Training data storage
│
└── frontend/
    ├── package.json
    ├── src/
    │   ├── App.js          # Main app component
    │   ├── components/
    │   │   ├── DatasetManager.js    # Dataset UI
    │   │   ├── ModelTrainer.js      # Training UI
    │   │   ├── ModelComparison.js   # Results display
    │   │   ├── PerformanceChart.js  # Visualizations
    │   │   └── PredictionPlot.js    # Prediction graphs
    │   └── styles/
    │       ├── DatasetManager.css
    │       ├── ModelTrainer.css
    │       └── ModelComparison.css
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn
- Git

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
cp .env.example .env
```

5. **Run Flask server**
```bash
python main.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create .env file (if not exists)**
```
REACT_APP_API_URL=http://localhost:5000/api
```

4. **Start React development server**
```bash
npm start
```

The frontend will open at `http://localhost:3000`

## Usage Guide

### 1. Upload Training Dataset
1. Click "Click to upload or drag file" in Dataset Management
2. Select your .xlsx or .csv file
3. File is validated and stored in `backend/datasets/`

### 2. Select Training Dataset
1. Choose from dropdown of stored datasets
2. View dataset preview for columns and statistics
3. Selected dataset is highlighted

### 3. Upload Test Dataset
1. In Model Training section, upload test data
2. Ensure same columns as training data

### 4. Train Models
1. Click "Start Training" button
2. All 3 models train in sequence
3. Training progress is displayed
4. Results show automatically

### 5. View Results
1. Best model highlighted at top
2. Click tabs to compare individual models
3. View R², RMSE, MAE metrics
4. Check actual vs predicted plots
5. Analyze feature importance (RF & XGBoost)

## API Documentation

### Dataset Endpoints

**List all datasets**
```
GET /api/datasets/list
```

**Upload dataset**
```
POST /api/datasets/upload
Content-Type: multipart/form-data
Body: { file: <binary> }
```

**Preview dataset**
```
GET /api/datasets/preview/<dataset_name>
```

**Delete dataset**
```
DELETE /api/datasets/delete/<dataset_name>
```

### Model Endpoints

**Train all models**
```
POST /api/models/train
Content-Type: multipart/form-data
Body: {
  train_dataset: <name>,
  test_file: <binary>,
  target: <column_name>
}
Response: {
  success: true,
  models: {
    ANN: {...},
    RandomForest: {...},
    XGBoost: {...}
  },
  best_model: {...}
}
```

**Compare models**
```
POST /api/models/compare
(Same body as /train)
Response: {
  models_comparison: {...},
  best_model: {...}
}
```

### Health Endpoints

**Check status**
```
GET /api/health/status
```

**Readiness check**
```
GET /api/health/ready
```

## Data Format Requirements

### Input CSV/Excel Format
```
| Feature1 | Feature2 | Feature3 | Target |
|----------|----------|----------|--------|
| 10.5     | 5.2      | 1.0      | 150.5  |
| 12.3     | 6.1      | 1.5      | 175.2  |
```

### Required Columns (Default)
- `Potential`: Voltage range
- `OXIDATION`: Oxidation state
- `Zn/Co_Conc`: Element concentration
- `SCAN_RATE`: Scan rate of experiment
- `ZN`, `CO`: Element flags
- `Current`: Target variable (predictions)

**Note**: Customize column names in model functions if needed

## Model Performance

### Expected Metrics
- **R² Score**: 0.8-0.99 (higher is better)
- **RMSE**: Depends on target scale
- **MAE**: Mean absolute error

### Training Time
- Approximate time: 1-5 minutes (depends on dataset size)
- All 3 models trained sequentially
- ANN: ~120-180s
- Random Forest:~60-90s
- XGBoost: ~45-75s

## Troubleshooting

### Common Issues

**"Connection refused" error**
- Ensure backend is running on port 5000
- Check `REACT_APP_API_URL` in frontend `.env`

**"No module named..." errors**
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version is 3.8+

**Training fails with empty data**
- Ensure test/train datasets have same columns
- Check for missing values in critical columns
- Validate data format (.xlsx or .csv)

**Low R² or constant predictions**
- Verify train/test data compatibility
- Check target variable range
- Ensure features have sufficient variation

## Data Preprocessing Pipeline

The system automatically handles:
1. **Missing Value Imputation**: Median for numeric, mode for categorical
2. **Feature Scaling**: RobustScaler (resistant to outliers)
3. **Target Normalization**: StandardScaler (for proper evaluation)
4. **Data Validation**: Checks for constant targets, empty datasets
5. **Train/Test Separation**: Strict separation to prevent leakage

## Performance Optimization

- **Parallel Processing**: Multi-threaded model training
- **Lazy Loading**: React components load on demand
- **Bundle Optimization**: Minimal CSS/JS overhead
- **Efficient Scaling**: RobustScaler for outlier handling

## Security Considerations

- Input validation on all file uploads
- File size limits (50MB max)
- CORS protection
- Safe file naming (sanitization)
- No sensitive data in logs

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions:
1. Check troubleshooting section above
2. Review error messages in browser console `/api/models/train`
3. Check backend logs for detailed error traces
4. Verify data format matches requirements

## Roadmap

- [ ] Real-time model training progress updates
- [ ] Batch prediction capability
- [ ] Model serialization and loading
- [ ] Cross-validation support
- [ ] Hyperparameter tuning UI
- [ ] Data visualization enhancements
- [ ] Export results to PDF/Excel
- [ ] User authentication

## Acknowledgments

- Built with React, Flask, and ML libraries
- Inspired by modern ML workflows
- Uses best practices for data science applications
