# ML Web Application - Installation & Troubleshooting

## 📦 Full Installation Steps

### Prerequisites Verification

```bash
# Check Python version (need 3.8+)
python --version

# Check Node.js version (need 14+)
node --version

# Check npm version
npm --version
```

---

## 🔧 Backend Installation Details

### Alternative Installation Methods

#### Using Poetry (Optional)

```bash
cd backend
pip install poetry
poetry install
poetry run python main.py
```

#### Using Conda (Optional)

```bash
cd backend
conda create -n ml-app python=3.10
conda activate ml-app
pip install -r requirements.txt
python main.py
```

### Checking Dependencies

```bash
pip list
```

Should include:
- fastapi
- uvicorn
- pandas
- numpy
- scikit-learn
- xgboost
- tensorflow
- python-multipart
- openpyxl

---

## 🎨 Frontend Installation Details

### Node Modules Size

The `node_modules` folder will be ~500MB (normal for React projects with all dependencies).

### Clear Cache & Reinstall

If you encounter npm issues:

```bash
# Option 1: Clean reinstall
cd frontend
del node_modules  # Windows
rm -rf node_modules  # macOS/Linux
del package-lock.json  # Windows
rm -f package-lock.json  # macOS/Linux
npm cache clean --force
npm install

# Option 2: Using npm ci (for exact versions)
npm ci

# Option 3: Using yarn
npm install -g yarn
yarn install
yarn start
```

---

## 🚨 Common Issues & Solutions

### Backend Issues

#### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
cd backend
pip install -r requirements.txt
# OR
pip install fastapi uvicorn
```

#### Issue: "tensorflow not found" or installation fails

**Solution (TensorFlow can be large):**
```bash
# Install without GPU support (lighter)
pip install tensorflow-cpu

# Or install CPU-optimized version
pip install tensorflow==2.12.0
```

#### Issue: "Port 8000 already in use"

**Solution - Find and kill the process:**

Windows:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

macOS/Linux:
```bash
lsof -i :8000
kill -9 <PID>
```

Or run on different port:
```bash
python -m uvicorn main:app --port 8001 --reload
```

#### Issue: CORS errors in browser console

**Response from backend:** "Access-Control-Allow-Origin missing"

**Solution:** Verify CORS is enabled in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific URLs in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Issue: XGBoost installation fails

**Solution:**
```bash
# Install build tools if needed
# Windows: Install Visual C++ Build Tools
# macOS: Install Xcode command line tools
xcode-select --install

# Then retry
pip install xgboost
```

### Frontend Issues

#### Issue: npm install very slow

**Solution - Use registry mirror:**
```bash
npm config set registry https://registry.npmmirror.com
npm install
```

#### Issue: "npm ERR! code EACCES"

**Solution:**
```bash
# Fix npm permissions (macOS/Linux)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
```

#### Issue: React port 3000 already in use

**Solution:**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :3000
kill -9 <PID>
```

Or specify different port:
```bash
PORT=3001 npm start  # macOS/Linux
set PORT=3001 && npm start  # Windows
```

#### Issue: "Cannot find module 'react'"

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Issue: Blank page or "Failed to compile"

**Solution:**
```bash
# Check browser console (F12)
# Check terminal for error messages
# Clear browser cache (Ctrl+Shift+Delete)
# Restart npm start
```

---

## 🔗 Connectivity Issues

### "Cannot GET /api/datasets"

This means frontend can't reach backend.

**Checklist:**
1. Is backend running? (Check terminal)
2. Is it on port 8000?
3. Check API URL in `frontend/src/services/api.js`:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000/api';
   ```
4. Check browser console (F12) for network errors

**Solution:**
```bash
# Terminal 1: Start backend with explicit binding
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start frontend
cd frontend
npm start

# Open http://localhost:3000
```

### CORS Issues in Production

If deploying, update frontend API URL:
```javascript
const API_BASE_URL = 'https://your-backend-domain.com/api';
```

And update backend CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧪 Testing Connectivity

### Test Backend Directly

```bash
# In browser or using curl
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","message":"ML API is running"}
```

### Test Datasets Endpoint

```bash
curl http://localhost:8000/api/datasets

# Should return:
# {"datasets":[]}  # Empty initially
```

### Test with Sample Data Generation

```bash
cd backend/datasets
python generate_sample_datasets.py

# Creates:
# - BiFeO3_dataset.csv
# - MnO2_dataset.csv
# - Graphene_dataset.csv
```

---

## 📋 System Requirements

### Minimum

- **RAM:** 4GB
- **Storage:** 2GB (without node_modules: 500MB)
- **CPU:** Dual-core

### Recommended

- **RAM:** 8GB+ (for faster model training)
- **Storage:** 5GB
- **CPU:** Quad-core
- **GPU:** Optional (for TensorFlow acceleration)

---

## 🐳 Docker Setup (Alternative)

Create `Dockerfile` in project root:

```dockerfile
# Multi-stage build
FROM python:3.10-slim as backend
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend .

FROM node:18 as frontend
WORKDIR /app/frontend
COPY frontend/package*.json .
RUN npm ci
COPY frontend .
RUN npm run build

FROM python:3.10-slim
WORKDIR /app
COPY --from=backend /app/backend .
COPY --from=frontend /app/frontend/build ./static
EXPOSE 8000
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t ml-web-app .
docker run -p 8000:8000 ml-web-app
```

---

## ✅ Final Verification

After installation, run this:

```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm start

# Terminal 3: Test
curl http://localhost:8000/health
```

Should see:
- Backend: "Uvicorn running..."
- Frontend: "Compiled successfully!"
- Test: JSON response with status

---

## 📞 Still Having Issues?

1. **Check logs:** Look at terminal output carefully
2. **Check Python version:** `python --version` (need 3.8+)
3. **Check Node version:** `node --version` (need 14+)
4. **Reinstall:** Delete folders and reinstall cleanly
5. **Search error:** Copy error message into your favorite search engine
6. **Create issue:** Provide error message, OS, Python/Node versions

---

## 🎉 Once Everything Works

- Backend: `http://localhost:8000/docs` (API documentation)
- Frontend: `http://localhost:3000` (Web UI)
- Upload sample datasets and test!
