# ML-Based CV Behavior Prediction - Render Deployment Guide

## Project Overview
This is a machine learning application for predicting CV-related behavior patterns using advanced ML models (XGBoost, TensorFlow).

## Deployment Architecture

### Backend (FastAPI)
- **Service Name**: ml-cv-prediction-api
- **Runtime**: Python 3.11
- **Port**: 8000 (on Render infrastructure)
- **Key Dependencies**: FastAPI, Uvicorn, Gunicorn, TensorFlow, scikit-learn, XGBoost, pandas

### Frontend (React)
- **Service Name**: ml-cv-prediction-frontend
- **Runtime**: Node.js 18
- **Build Output**: Static files in `frontend/build`
- **Key Dependencies**: React 18, Axios, Recharts

## Pre-Deployment Checklist

### 1. Local Testing
```bash
# Test backend
cd backend
pip install -r requirements.txt
python main.py

# Test frontend
cd frontend
npm install
npm start
```

### 2. Environment Variables
Create a `.env` file in the project root (see `.env.example`):
- `CORS_ORIGINS`: Your Render frontend URL
- `ENVIRONMENT`: Set to "production"

### 3. Git Repository
Ensure your project is pushed to GitHub/GitLab:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Deployment Steps on Render

### Step 1: Create Backend Service
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: ml-cv-prediction-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements-prod.txt`
   - **Start Command**: `cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT main:app --timeout 120`
   - **Instance Type**: Standard (minimum recommended for ML models)

### Step 2: Set Backend Environment Variables
In Render dashboard for backend service:
```
CORS_ORIGINS=https://ml-cv-prediction-frontend.onrender.com
PYTHONUNBUFFERED=1
```

### Step 3: Create Frontend Service
1. Click "New +" → "Static Site"
2. Connect your GitHub repository (same repo)
3. Configure:
   - **Name**: ml-cv-prediction-frontend
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`

### Step 4: Set Frontend Environment Variables
In Render dashboard for frontend service:
```
REACT_APP_API_URL=https://ml-cv-prediction-api.onrender.com
```

### Step 5: Update CORS in Backend
1. Redeploy backend service to apply new environment variable
2. Update `backend/main.py` if needed to read from environment:

```python
import os
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Expected Build Times
- **Backend**: 5-10 minutes (TensorFlow takes time to build)
- **Frontend**: 3-5 minutes

## Monitoring & Logs
- Backend logs: Available in Render dashboard
- Frontend build logs: Check Render deployment logs
- Health check: `https://ml-cv-prediction-api.onrender.com/health`

## Troubleshooting

### Backend fails to build
- Check Python dependencies: `pip install -r backend/requirements-prod.txt` locally
- TensorFlow requires significant build time; monitor build logs

### Frontend API connection issues
- Verify `REACT_APP_API_URL` environment variable is set correctly
- Check CORS settings in backend match frontend URL
- Test health endpoint manually

### Port issues
- Render assigns ports dynamically; don't hardcode port 8000
- Use `$PORT` environment variable

## Custom Domain Setup
1. In Render dashboard, go to "Settings" → "Custom Domain"
2. Add your domain
3. Update DNS records as instructed
4. Wait for SSL certificate generation (5-10 minutes)

## Performance Notes
- ML model inference may take 5-30 seconds depending on data size
- Recommended Render instance: Standard or higher
- Consider upgrading if timeout issues occur (increase `--timeout` in Procfile)

## Security Recommendations
- Create `.env.production` file (don't commit to Git)
- Use Render environment variables for sensitive data
- Enable HTTPS (automatic on Render)
- Regularly update dependencies for security patches

## Rollback Strategy
- Render automatically maintains deployment history
- Use Render dashboard to revert to previous deployment if needed
