# ⚡ QUICK REFERENCE - UNIFIED WEBSITE

## 🎯 What You Need to Know

Your ML-Based CV Behavior Prediction app is now **ONE unified website** (like real-world apps).

---

## 🚀 Deploy in 3 Steps

### Step 1: Prepare
```powershell
cd c:\Users\shoai\ml-web-app
git init
git add .
git commit -m "Unified ML-CV prediction website"
```

### Step 2: Push to GitHub
```powershell
git remote add origin https://github.com/YOUR_USERNAME/ml-cv-prediction.git
git push -u origin main
```

### Step 3: Deploy on Render
1. Go to [render.com](https://render.com)
2. **New +** → **Web Service**
3. Select your repo
4. Configure:
   ```
   Name: ml-cv-prediction
   Environment: Python 3
   Build: cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements-prod.txt
   Start: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT main:app --timeout 120
   ```
5. Create!
6. Wait 12-15 minutes

✅ **Visit:** `https://ml-cv-prediction.onrender.com`

---

## 💻 Run Locally

### Quick Start (Copy & Paste)

**Terminal 1:**
```bash
cd c:\Users\shoai\ml-web-app\backend && pip install -r requirements.txt && python main.py
```

**Terminal 2:**
```bash
cd c:\Users\shoai\ml-web-app\frontend && npm install && npm start
```

**Browser:** Open `http://localhost:3000`

---

## 🗂️ Folder Structure

```
ml-web-app/
├── backend/
│   ├── main.py              ← Serves React + API
│   ├── requirements-prod.txt
│   ├── routes/              ← API endpoints
│   ├── models/              ← ML models
│   └── utils/               ← Preprocessing
│
├── frontend/
│   ├── src/
│   │   ├── services/api.js  ← Uses /api (no full URL needed)
│   │   ├── App.js
│   │   └── components/
│   ├── package.json
│   └── build/               ← Created after npm run build
│
├── Procfile                 ← Render build/start commands
├── render.yaml              ← Render config
├── .env.example
├── START_HERE.md            ← Quick deployment
├── UNIFIED_DEPLOYMENT.md    ← Full architecture
├── LOCAL_DEVELOPMENT.md     ← Local testing
└── README.md
```

---

## 🌐 URLs After Deployment

All on **one domain**:
```
https://ml-cv-prediction.onrender.com/
├── /                    React web interface
├── /api/datasets        API: List datasets
├── /api/upload-dataset  API: Upload dataset
├── /api/predict         API: Make prediction
├── /health              Health check
└── /docs                API documentation
```

---

## 📊 Architecture

```
Browser (http://localhost:3000 or deployed URL)
         ↓
React App (runs in browser)
         ↓
Makes calls to /api/*
         ↓
FastAPI Backend (same server)
         ├─ Serves React app
         └─ Handles ML predictions
```

---

## 🔨 Build Timeline

| Step | Time |
|------|------|
| Frontend build | 2-3 min |
| Backend setup (TensorFlow) | 8-10 min |
| Server startup | 1 min |
| **Total** | **12-15 min** |

---

## ✅ Key Files Changed

1. **backend/main.py** - Serves React build + API
2. **frontend/src/services/api.js** - Uses `/api` paths
3. **Procfile** - Builds frontend, then runs backend
4. **render.yaml** - Single service config
5. **.env.example** - Simplified env vars

---

## 🎯 One Command to Test Everything

```bash
# Terminal 1
python -m venv venv
venv\Scripts\activate
cd backend && pip install -r requirements.txt && python main.py

# Terminal 2 (new terminal)
cd frontend && npm install && npm start

# Then open: http://localhost:3000
```

---

## 📞 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot connect to API" | Make sure both servers running (backend on :8000, frontend on :3000) |
| "Blank page" | Clear cache: Ctrl+Shift+Del, then refresh |
| "Build taking forever" | TensorFlow takes 8-10 min - normal! Check logs in Render dashboard |
| "Port already in use" | Kill process: `taskkill /F /IM python.exe` |

---

## 📚 Guides by Use Case

| Need | Read |
|------|------|
| Quick deploy | **START_HERE.md** |
| Local testing | **LOCAL_DEVELOPMENT.md** |
| Architecture | **UNIFIED_DEPLOYMENT.md** |
| Full details | **UNIFIED_WEBSITE_SUMMARY.md** |

---

## 🎉 That's It!

Your app is:
- ✅ Frontend-Backend integrated
- ✅ Single URL
- ✅ No CORS needed
- ✅ Real-world pattern
- ✅ Ready to deploy

---

## 🔗 Your Website

After deployment, share this URL:

```
https://ml-cv-prediction.onrender.com
```

**Features:**
- Upload CV datasets
- Run ML predictions (XGBoost, TensorFlow, Random Forest)
- Compare model performance
- View real-time results

---

## 🚀 Deployment Status

- [ ] Prepare & commit locally
- [ ] Push to GitHub
- [ ] Create Render account
- [ ] Deploy Web Service
- [ ] Test website
- [ ] Share URL!

---

**Type:** Unified Web Application  
**Language:** Python (backend) + React (frontend)  
**Status:** Production Ready ✅  
**Time to Deploy:** ~15 minutes
