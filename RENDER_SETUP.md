# ML-Based CV Behavior Prediction
## Deployment Configuration for Render

This project is configured for deployment on [Render.com](https://render.com).

### 📁 Project Structure
```
ml-web-app/
├── backend/              # FastAPI backend (Python)
│   ├── main.py
│   ├── requirements-prod.txt
│   ├── routes/
│   ├── models/
│   └── utils/
├── frontend/             # React frontend (Node.js)
│   ├── src/
│   ├── public/
│   └── package.json
├── render.yaml           # Render deployment config
├── Procfile              # Process file for Render
├── .env.example          # Environment variables template
├── DEPLOYMENT_GUIDE.md   # Complete deployment guide
└── deploy.bat/deploy.sh  # Quick deployment scripts
```

### 🚀 Quick Start Deployment

#### Option 1: Automatic (Recommended)
```bash
# Windows
deploy.bat

# Mac/Linux
bash deploy.sh
```

#### Option 2: Manual Steps
1. **Initialize Git** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: ML-Based CV Behavior Prediction"
   ```

2. **Push to GitHub**:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ml-web-app.git
   git push -u origin main
   ```

3. **Deploy on Render**:
   - Visit [render.com](https://render.com)
   - Create Backend Web Service (uses `Procfile`)
   - Create Frontend Static Site
   - Set environment variables (see below)

### 🔐 Environment Variables

**Backend (`ml-cv-prediction-api`) Environment:**
```
CORS_ORIGINS=https://ml-cv-prediction-frontend.onrender.com
PYTHONUNBUFFERED=1
```

**Frontend (`ml-cv-prediction-frontend`) Environment:**
```
REACT_APP_API_URL=https://ml-cv-prediction-api.onrender.com
```

### 📊 Service Information

| Service | Type | Runtime | Build Time |
|---------|------|---------|-----------|
| Backend | Web Service | Python 3.11 | 8-10 min |
| Frontend | Static Site | Node.js 18 | 3-5 min |

### ✅ Verification

After deployment:
1. Check backend health: `https://your-backend.onrender.com/health`
2. Visit frontend: `https://your-frontend.onrender.com`
3. Test prediction flow

### 📚 Documentation
- [Complete Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Project README](README.md)
- [Installation Guide](INSTALLATION_GUIDE.md)

### 🆘 Troubleshooting

**Backend build fails:**
- Verify `pip install -r backend/requirements-prod.txt` works locally
- Check Python version compatibility
- Monitor build logs in Render dashboard

**Frontend can't reach API:**
- Confirm `REACT_APP_API_URL` environment variable is set
- Check backend CORS_ORIGINS includes frontend URL
- Test API endpoint manually

**Timeout errors:**
- Increase timeout: modify `--timeout 120` in Procfile
- Upgrade Render instance type
- Optimize ML model inference

---

**Website Name:** ML-Based CV Behavior Prediction  
**Environment:** Production Ready  
**Last Updated:** April 2026
