# ✅ ML Web Application - Setup Checklist

Complete this checklist to get your ML Web Application running.

---

## 📋 PRE-SETUP VERIFICATION

- [ ] Python 3.8+ installed: `python --version`
- [ ] Node.js 14+ installed: `node --version`
- [ ] npm installed: `npm --version`
- [ ] Project folder: `c:\Users\shoai\ml-web-app`
- [ ] All files created successfully

---

## 🔧 BACKEND SETUP

### Step 1: Install Python Dependencies
- [ ] Navigate to backend folder: `cd backend`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment: `venv\Scripts\activate` (Windows)
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Verify installation: `pip list` (check for fastapi, tensorflow, xgboost)

### Step 2: Generate Sample Datasets (Optional)
- [ ] Navigate to datasets folder: `cd datasets`
- [ ] Run generator: `python generate_sample_datasets.py`
- [ ] Verify files created: Check for .csv and .xlsx files
- [ ] Return to backend folder: `cd ..`

### Step 3: Start Backend Server
- [ ] Run server: `python main.py`
- [ ] Verify running: Check for "Uvicorn running on http://0.0.0.0:8000"
- [ ] Keep this terminal open

### Step 4: Verify Backend Works
- [ ] Open browser: `http://localhost:8000/health`
- [ ] Should see: `{"status":"healthy","message":"ML API is running"}`
- [ ] API docs: `http://localhost:8000/docs`
- [ ] Check endpoints are listed

---

## 🎨 FRONTEND SETUP

### Step 1: Install Node Packages
- [ ] Open new terminal
- [ ] Navigate to frontend: `cd frontend`
- [ ] Install dependencies: `npm install`
- [ ] Wait for installation (may take 2-5 minutes)
- [ ] Verify: Check for `node_modules` folder

### Step 2: Start Frontend Dev Server
- [ ] Run: `npm start`
- [ ] Browser should open automatically to `http://localhost:3000`
- [ ] Verify: See "ML Web Application" header
- [ ] Keep this terminal open

---

## 🧪 FUNCTIONALITY TESTING

### Test 1: Dataset Upload
- [ ] Click "Upload New Training Dataset"
- [ ] Select a CSV or Excel file
- [ ] Click "Upload Dataset" button
- [ ] Verify: Success message appears
- [ ] Verify: Dataset appears in dropdown

### Test 2: Dataset Selection
- [ ] Click "Select Training Dataset" dropdown
- [ ] Verify: Uploaded dataset visible
- [ ] Select it

### Test 3: Test File Upload
- [ ] Click "Upload Test Dataset" file area
- [ ] Select a test CSV/Excel file
- [ ] Verify: Filename shown with option to remove

### Test 4: Model Selection
- [ ] Check radio buttons for model selection
- [ ] Options should be: All, ANN, RF, XGBoost

### Test 5: Run Prediction
- [ ] Have training dataset selected
- [ ] Have test file uploaded
- [ ] Click "Run Prediction" button
- [ ] Verify: Loading spinner appears
- [ ] Wait for processing (5-20 seconds)
- [ ] Verify: Results appear below

### Test 6: Results Display
- [ ] Check accuracy, RMSE, MAE displayed
- [ ] Verify: Bar chart showing model comparison
- [ ] Verify: Line chart showing predictions
- [ ] Check feature importance (if available)

### Test 7: Download CSV
- [ ] Click "Download Predictions as CSV" button
- [ ] Verify: File downloaded (check Downloads folder)
- [ ] Open file: Verify data format

---

## 🐛 TROUBLESHOOTING CHECKLIST

### Backend Won't Start

- [ ] Check Python version: `python --version` (need 3.8+)
- [ ] Virtual environment activated? Look for `(venv)` in terminal
- [ ] All dependencies installed? `pip list | grep fastapi`
- [ ] Port 8000 available? Try: `netstat -ano | findstr :8000`
- [ ] Clear Python cache: `py -m compileall -b .` then delete `__pycache__`
- [ ] Reinstall dependencies: Delete venv, create new one, reinstall

### Frontend Won't Start

- [ ] Check Node version: `node --version` (need 14+)
- [ ] npm installed: `npm --version`
- [ ] Deleted node_modules? Try: `npm ci`
- [ ] Clear npm cache: `npm cache clean --force`
- [ ] Port 3000 available? Check: `netstat -ano | findstr :3000`
- [ ] Delete node_modules and package-lock.json, reinstall

### Can't Upload Dataset

- [ ] Backend running? Check terminal
- [ ] File format correct? Use .csv or .xlsx
- [ ] File not too large? Try smaller file first
- [ ] Check browser console: F12 → Console tab
- [ ] Check backend terminal for errors

### API Connection Errors

- [ ] Backend running on 8000?
- [ ] Frontend API URL correct? Check `frontend/src/services/api.js`
- [ ] CORS enabled? Check `backend/main.py`
- [ ] Both servers running? Check both terminals
- [ ] Try different port: Change in both places

### Predictions Not Working

- [ ] Training dataset selected? Check dropdown
- [ ] Test file uploaded? Check file uploader
- [ ] Sufficient data? Need at least 20 samples
- [ ] Target column in data? Last column assumed as target
- [ ] Check error message in UI
- [ ] Check backend terminal for stack trace

### Slow Performance

- [ ] Dataset too large? Try smaller sample
- [ ] Computer specs sufficient? Check RAM/CPU
- [ ] Other programs using resources? Close unnecessary apps
- [ ] Try simpler model: Select single model instead of all
- [ ] Hardware limitation: Consider upgrading RAM

---

## 📊 VERIFICATION TESTING

After everything works, verify these features:

### Data Management
- [ ] Can upload multiple datasets
- [ ] Datasets listed in dropdown
- [ ] Can delete datasets
- [ ] Can upload CSV and Excel formats

### Model Training
- [ ] ANN trains successfully
- [ ] Random Forest trains successfully
- [ ] XGBoost trains successfully
- [ ] Can train individual models or all

### Predictions & Results
- [ ] Predictions generated for each model
- [ ] Accuracy metrics displayed
- [ ] RMSE and MAE calculated
- [ ] Results layout responsive

### Visualizations
- [ ] Bar chart displays model comparison
- [ ] Line chart shows prediction trends
- [ ] Feature importance shows top features
- [ ] Charts responsive on different screen sizes

### User Experience
- [ ] Loading spinner visible during processing
- [ ] Error messages clear and helpful
- [ ] CSV download works correctly
- [ ] Buttons disabled appropriately
- [ ] Responsive on tablet (developer tools)

---

## 📁 FILE LOCATION VERIFICATION

Verify these key files exist:

### Backend
- [ ] `backend/main.py` - Main server
- [ ] `backend/requirements.txt` - Dependencies
- [ ] `backend/models/ml_models.py` - ML models
- [ ] `backend/routes/dataset_routes.py` - Dataset endpoints
- [ ] `backend/routes/prediction_routes.py` - Prediction endpoints
- [ ] `backend/utils/preprocessing.py` - Data preprocessing
- [ ] `backend/utils/evaluation.py` - Evaluation metrics
- [ ] `backend/datasets/` - Dataset directory

### Frontend
- [ ] `frontend/package.json` - React dependencies
- [ ] `frontend/public/index.html` - HTML entry
- [ ] `frontend/src/App.js` - Main component
- [ ] `frontend/src/index.js` - React entry
- [ ] `frontend/src/services/api.js` - API service
- [ ] `frontend/src/components/DatasetSelector.js`
- [ ] `frontend/src/components/FileUploader.js`
- [ ] `frontend/src/components/ResultsDisplay.js`
- [ ] `frontend/src/components/ModelComparison.js`

### Documentation
- [ ] `README.md` - Main documentation
- [ ] `QUICK_START.md` - Quick setup guide
- [ ] `INSTALLATION_GUIDE.md` - Troubleshooting
- [ ] `ARCHITECTURE.md` - Architecture overview
- [ ] `PROJECT_SUMMARY.md` - Project info

---

## 🎯 SUCCESS INDICATORS

You're successful when you see:

✅ **Backend**
- "Uvicorn running on http://0.0.0.0:8000"
- Swagger UI at http://localhost:8000/docs

✅ **Frontend**
- "Compiled successfully!"
- App loads at http://localhost:3000
- "ML Web Application" title visible

✅ **Integration**
- Dataset dropdown works
- File uploads complete
- Predictions execute
- Results display with charts

✅ **Features Work**
- Can switch between models
- Charts render correctly
- CSV download functions
- Error messages appear properly

---

## 🚀 NEXT STEPS (After Verification)

- [ ] Read ARCHITECTURE.md for deep dive
- [ ] Try with your own datasets
- [ ] Modify model hyperparameters
- [ ] Add custom features
- [ ] Consider deployment options
- [ ] Set up version control (git)
- [ ] Create backup of working version

---

## 📞 NEED HELP?

1. **Check documentation:**
   - README.md - Full guide
   - QUICK_START.md - Fast setup
   - INSTALLATION_GUIDE.md - Troubleshooting
   - ARCHITECTURE.md - System design

2. **Check error messages:**
   - Browser console: F12
   - Backend terminal: Check logs
   - Frontend terminal: Check compiler output

3. **Verify prerequisites:**
   - Python 3.8+? 
   - Node 14+?
   - Port 8000 free?
   - Port 3000 free?

4. **Try basic tests:**
   - Backend health: `http://localhost:8000/health`
   - API docs: `http://localhost:8000/docs`
   - Frontend loads: `http://localhost:3000`

---

## 💾 CHECKPOINT SUMMARY

| Checkpoint | Status | Time |
|-----------|--------|------|
| Python/Node installed | [ ] | 0 min |
| Backend dependencies | [ ] | 3-5 min |
| Sample datasets generated | [ ] | 1 min |
| Backend starts | [ ] | 30 sec |
| Frontend dependencies | [ ] | 2-5 min |
| Frontend starts | [ ] | 1 min |
| Upload test | [ ] | 1 min |
| Prediction test | [ ] | 2 min |
| Results display | [ ] | instant |
| **TOTAL TIME** | | **15-20 min** |

---

**Status Tracking:**
```
[ ] 25% - Prerequisites verified
[ ] 50% - Backend running
[ ] 75% - Frontend running
[ ] 100% - Full system working

🎉 Application Ready!
```

---

**Last Updated:** 2024
**Project Status:** ✅ Complete & Ready to Use
