# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate sample datasets (optional)
cd datasets
python generate_sample_datasets.py
cd ..

# Start server
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ Backend ready at `http://localhost:8000`

---

### Step 2: Frontend Setup (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Expected output:**
```
Compiled successfully!
Local:            http://localhost:3000
```

✅ Frontend ready at `http://localhost:3000`

---

### Step 3: Test the Application

1. **Open browser** → `http://localhost:3000`

2. **Upload a dataset:**
   - Click "Upload New Training Dataset"
   - Navigate to `backend/datasets/` 
   - Select a dataset (if generated using step 1)
   - Click "Upload Dataset"

3. **Select training dataset:**
   - Choose from dropdown in "Select Training Dataset"

4. **Upload test file:**
   - Click file upload area in "Upload Test Dataset"
   - Select a test dataset

5. **Run prediction:**
   - Choose model type (All/ANN/RF/XGBoost)
   - Click "Run Prediction" button

6. **View results:**
   - See accuracy, RMSE, MAE metrics
   - View prediction comparison charts
   - Download results as CSV

---

## 📊 Generate Sample Data Quickly

```bash
cd backend/datasets
python generate_sample_datasets.py
cd ..
```

This creates 3 sample datasets:
- BiFeO3_dataset.csv/xlsx
- MnO2_dataset.csv/xlsx
- Graphene_dataset.csv/xlsx

---

## 🔗 API Documentation

When backend is running, visit: `http://localhost:8000/docs`

This shows all available endpoints with interactive testing!

---

## ✅ Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Sample datasets generated
- [ ] Can upload dataset via UI
- [ ] Can select training dataset from dropdown
- [ ] Can upload test data
- [ ] Predictions generate successfully
- [ ] Charts display correctly

---

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| "Port already in use" | Change port in `main.py` or close other apps |
| CORS errors | Ensure backend is running and CORS enabled |
| Dependencies missing | Run `pip install -r requirements.txt` |
| npm install fails | Delete `node_modules` and `package-lock.json`, retry |
| No datasets appear | Run `python generate_sample_datasets.py` |

---

## 📈 Next Steps

1. **Test with your own data** - Replace sample datasets
2. **Modify models** - Adjust hyperparameters in `models/ml_models.py`
3. **Deploy** - See README.md for production deployment
4. **Customize UI** - Modify React components in `frontend/src`

---

## 📞 Support

- Backend docs: `http://localhost:8000/docs`
- Frontend console: Open DevTools (F12) → Console tab
- Check logs in terminal windows for errors

Happy machine learning! 🎉
