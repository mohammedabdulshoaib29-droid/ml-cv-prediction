# Quick Start Guide

## Starting the Application

### Step 1: Start Backend (Terminal 1)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
 * WARNING: This is a development server. Do not use it in production deployment.
```

### Step 2: Start Frontend (Terminal 2)
```bash
cd frontend
npm install  # Only first time
npm start
```

**Expected Output:**
```
Compiled successfully!
You can now view ml-web-app in the browser.

Local:            http://localhost:3000
```

### Step 3: Access Application
Open browser to `http://localhost:3000`

---

## Using the Application

### 1. Create Training Data (Optional)

**Sample CSV format:**
```csv
Potential,OXIDATION,Zn/Co_Conc,SCAN_RATE,ZN,CO,Current
-0.5,1,0.5,0.1,1,0,100.5
-0.4,1,0.5,0.1,1,0,102.3
...
```

### 2. Upload Training Dataset
1. Click "Click to upload or drag file" in left panel
2. Select your .csv or .xlsx file
3. Dataset appears in dropdown

### 3. Upload Test Dataset  
1. Click "Click to upload test dataset" button
2. Select separate test data file
3. Same columns as training data required

### 4. Train Models
1. Ensure training dataset is selected
2. Test dataset is uploaded
3. Click "Start Training"
4. Wait for completion (1-5 min)

### 5. View Results
1. **Overview**: Best model highlighted
2. **Comparison**: Side-by-side metrics
3. **Details**: Click tabs for individual models
4. **Graphs**: Actual vs Predicted plots
5. **Analysis**: Feature importance bars

---

## Default Data Format

### Required Columns (Electrochemistry)
- `Potential`: Voltage (float) -1.0 to 1.0
- `OXIDATION`: Oxidation state (int) 0-1
- `Zn/Co_Conc`: Concentration (float) 0-10
- `SCAN_RATE`: Scan rate (float) 0.01-100
- `ZN`: Zinc flag (0/1)
- `CO`: Cobalt flag (0/1)
- `Current`: Target - Current response (float)

### Customize Columns
Edit in `backend/models/*.py`:
```python
predictors = ["col1", "col2", "col3", ...]
target = "target_col"
```

---

## Expected Results

### Model Performance
| Model | R² Score | RMSE | MAE |
|-------|----------|------|-----|
| ANN | 0.95+ | 0.001-0.01 | 0.001-0.008 |
| Random Forest | 0.92+ | 0.002-0.015 | 0.002-0.01 |
| XGBoost | 0.94+ | 0.002-0.012 | 0.001-0.009 |

### Training Time
- **Total**: 2-5 minutes
- **ANN**: ~120s
- **RF**: ~90s  
- **XGBoost**: ~60s

---

## Troubleshooting

### Backend won't start
```bash
# Kill existing process on port 5000
lsof -i :5000  # Find process
kill -9 <PID>  # Kill process

# Or change port in main.py:
app.run(port=5001)
```

### Frontend connection error
Check `frontend/.env`:
```
REACT_APP_API_URL=http://localhost:5000/api
```

### TensorFlow not installing (Windows)
```bash
# Try pre-built wheel
pip install tensorflow==2.13.0
```

### Dataset upload fails
- Check file size < 50MB
- Verify CSV/XLSX format
- Ensure no empty rows/columns

### Low R² scores
1. Check data quality
2. Ensure target has variation
3. Verify feature scaling worked
4. Check train/test overlap

---

## File Structure

```
ml-web-app/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── ann.py
│   │   ├── rf.py
│   │   ├── xgb.py
│   │   └── orchestrator.py
│   ├── routes/
│   │   ├── dataset_routes.py
│   │   ├── model_routes.py
│   │   └── health_routes.py
│   └── datasets/  ← Uploaded files stored here
│
└── frontend/
    ├── package.json
    ├── .env
    └── src/
        ├── components/
        │   ├── DatasetManager.js
        │   ├── ModelTrainer.js
        │   └── ModelComparison.js
        └── styles/
            ├── DatasetManager.css
            ├── ModelTrainer.css
            └── ModelComparison.css
```

---

## API Quick Reference

### List datasets
```bash
curl http://localhost:5000/api/datasets/list
```

### Train models
```bash
curl -X POST http://localhost:5000/api/models/train \
  -F "train_dataset=data.xlsx" \
  -F "test_file=@test.xlsx"
```

### Health check
```bash
curl http://localhost:5000/api/health/status
```

---

## Next Steps

1. **Prepare Data**: Format your dataset matching requirements
2. **Upload Training Data**: Use dataset manager
3. **Run Experiments**: Train models with different datasets
4. **Analyze Results**: Compare model performance
5. **Fine-tune**: Adjust hyperparameters in model files
6. **Deploy**: Use Render, Heroku, or Docker

---

## Support

Need help?

1. **Backend Error**: Check terminal output
2. **Frontend Error**: Open DevTools (F12) → Console
3. **Data Error**: Validate CSV/XLSX format
4. **Model Error**: Check data shape and types

See `README.md` for full documentation!
