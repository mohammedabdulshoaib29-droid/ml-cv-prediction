# 🚀 UNIFIED WEBSITE DEPLOYMENT GUIDE
## ML-Based CV Behavior Prediction

### What Changed ✅
Your frontend and backend are now **integrated into a single unified website**. Users access everything from one URL:

**Before:**
- Frontend: `https://ml-cv-prediction-frontend.onrender.com`
- Backend API: `https://ml-cv-prediction-api.onrender.com`
- ❌ Separate services required

**Now:**
- Website: `https://ml-cv-prediction.onrender.com`
- API: `https://ml-cv-prediction.onrender.com/api`
- ✅ Single unified service!

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────┐
│    SINGLE UNIFIED WEBSITE ON RENDER          │
│  ml-cv-prediction.onrender.com               │
├──────────────────────────────────────────────┤
│                                              │
│  ┌─────────────────────────────────────┐    │
│  │  FastAPI Backend Server (Port 8000) │    │
│  ├─────────────────────────────────────┤    │
│  │                                     │    │
│  │  ┌─────────────────────────────┐   │    │
│  │  │  React Frontend (Built)     │   │    │
│  │  │  Served as Static Files     │   │    │
│  │  └─────────────────────────────┘   │    │
│  │                                     │    │
│  │  /               → React App        │    │
│  │  /api/*          → API Endpoints    │    │
│  │  /docs           → API Docs         │    │
│  │  /health         → Health Check     │    │
│  │                                     │    │
│  └─────────────────────────────────────┘    │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 📋 Quick Deployment (3 Steps)

### Step 1: Prepare Repository
```bash
cd c:\Users\shoai\ml-web-app
git init
git add .
git commit -m "Unified website: ML-Based CV Behavior Prediction"
```

### Step 2: Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/ml-cv-prediction.git
git push -u origin main
```

### Step 3: Deploy on Render
1. Go to [render.com](https://render.com)
2. Click **New +** → **Web Service**
3. Select your repository
4. Configure:
   - **Name**: `ml-cv-prediction`
   - **Environment**: Python 3
   - **Region**: Closest to users
   - **Build Command**: 
     ```
     cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements-prod.txt
     ```
   - **Start Command**:
     ```
     cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT main:app --timeout 120
     ```
   - **Instance Type**: Standard

5. Click **Create Web Service**
6. ⏳ Wait 10-15 minutes for deployment

---

## ✅ Test Your Website

### After Deployment
1. **Open Website**: `https://ml-cv-prediction.onrender.com`
2. **Check Health**: `https://ml-cv-prediction.onrender.com/health`
3. **View API Docs**: `https://ml-cv-prediction.onrender.com/docs`

### Test Flow
1. Upload a CSV dataset from the web interface
2. Make a prediction
3. See results displayed in real-time

---

## 🔄 Local Development

### Run Locally (Full Integration)
```bash
# Terminal 1: Start frontend in development mode using proxy
cd frontend
npm install
npm start  
# Creates development server on http://localhost:3000

# Terminal 2: Start backend with frontend proxy to /api
cd backend
pip install -r requirements.txt
python main.py
# Runs on http://localhost:8000
```

**How it works:**
- Frontend dev server (port 3000) proxies `/api/*` requests to backend (port 8000)
- Frontend code changes auto-reload
- Backend changes require manual restart

### Or Run with Production Build
```bash
# Build frontend
cd frontend && npm install && npm run build

# Run backend (serves built frontend)
cd backend
pip install -r requirements.txt
python main.py
```

---

## 📊 Build Timeline

| Step | Time | Notes |
|------|------|-------|
| Frontend Build | 2-3 min | npm install + React build |
| Backend Dependencies | 8-10 min | TensorFlow compilation |
| Server Start | 1 min | Gunicorn startup |
| **Total** | **12-15 min** | First deployment |

---

## 🎯 How It Works Together

### Request Flow
```
User Browser
    ↓
[GET /] → FastAPI serves React app
    ↓
[Browser runs React]
    ↓
[User uploads dataset]
    ↓
[GET /api/datasets] → FastAPI handles API request
    ↓
[Response returned to React]
    ↓
[React displays results]
```

---

## 🔐 No Environment Variables Needed!

Since frontend and backend are unified:
- ❌ No CORS_ORIGINS needed
- ❌ No REACT_APP_API_URL needed
- ✅ Everything just works!

---

## 📁 File Structure

After deployment, Render will:
1. Build React frontend → `frontend/build/`
2. Install Python dependencies
3. Copy everything into single container
4. Start FastAPI server
5. FastAPI serves:
   - React build as static files at `/`
   - API endpoints at `/api/*`
   - API docs at `/docs`

---

## 💻 Your Website URL

```
https://ml-cv-prediction.onrender.com
```

**Endpoints:**
- `/` - React web interface
- `/api/datasets` - List datasets
- `/api/upload-dataset` - Upload new dataset
- `/api/predict` - Make predictions
- `/api/delete-datasets/{name}` - Delete dataset
- `/docs` - Interactive API documentation
- `/health` - Health check

---

## 🚀 What's Better Now?

✨ **Single URL** - Users only need one URL
✨ **No CORS issues** - Frontend and backend on same domain
✨ **Simpler setup** - One service instead of two
✨ **Faster communication** - Same server, no network overhead
✨ **Production ready** - Works like real-world applications
✨ **Easier to maintain** - Single deployment unit

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Page shows API message | Frontend not built; build succeeded but frontend build took longer |
| API not responding | Check backend logs in Render dashboard |
| Blank page | Clear browser cache (Ctrl+Shift+Del), refresh |
| Static files not serving | Ensure `frontend/build` directory exists locally |

---

## 📚 Files Modified

1. **backend/main.py** - Added static file serving from React build
2. **frontend/src/services/api.js** - Changed to relative API paths (`/api`)
3. **Procfile** - Single service that builds frontend then runs backend
4. **render.yaml** - Single service configuration
5. **.env.example** - Simplified environment variables

---

## 🎉 Real-World Application

Your ML-Based CV Behavior Prediction now works like real production applications:
- Single domain
- Frontend served by backend
- No separate build/deployment steps
- Traditional web architecture
- Professional deployment ready

---

**Website:** ML-Based CV Behavior Prediction  
**URL:** `https://ml-cv-prediction.onrender.com`  
**Status:** ✅ Production Ready  
**Type:** Single Unified Service
