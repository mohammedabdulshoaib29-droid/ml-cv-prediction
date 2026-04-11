# 🖥️ LOCAL DEVELOPMENT - Unified Website

## How to Run Locally

Since frontend and backend are unified, you can run them together in two ways:

---

## Method 1: React Dev Server + Backend (Recommended for Development)

**Fastest for development** - Hot reload for React code changes

### Terminal 1: Start Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Output should show:
```
Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Start React Dev Server
```bash
cd frontend
npm install
npm start
```
Browser should open to `http://localhost:3000`

### How It Works
- React dev server runs on `http://localhost:3000`
- All API calls to `/api/*` are proxy'd to backend on `http://localhost:8000`
- React automatically reloads on code changes
- Backend requires manual restart for changes

---

## Method 2: Production Build (Test Final Output)

**Slower, but tests production build** - Frontend built into backend

### Step 1: Build Frontend
```bash
cd frontend
npm install
npm run build
```
This creates `frontend/build/` with optimized React app

### Step 2: Run Backend with Built Frontend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend will serve:
- `/` - React app (from `frontend/build`)
- `/api` - API endpoints
- `/docs` - API documentation

Open browser: `http://localhost:8000`

---

## File Structure During Development

```
ml-web-app/
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── services/
│   │   │   └── api.js (uses /api base path)
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── build/          ← Created after npm run build
│
├── backend/
│   ├── main.py         (serves built React from /api endpoints)
│   ├── requirements.txt
│   ├── routes/
│   ├── models/
│   ├── utils/
│   └── datasets/
```

---

## Testing the API Directly

### From Terminal
```bash
# Health check
curl http://localhost:8000/health

# Get datasets
curl http://localhost:8000/api/datasets

# View API docs
# Open browser to: http://localhost:8000/docs
```

---

## Debugging Tips

### Debugging Frontend (Method 1)
1. Open browser dev tools: F12
2. Go to **Console** tab
3. Check for API errors
4. Set breakpoints in **Sources** tab

### Debugging Backend
1. Add print statements in `.py` files
2. Check console output from Terminal 1
3. View FastAPI docs: `http://localhost:8000/docs`
4. Test endpoints directly in docs UI

### Clear Cache
```bash
# If things act weird
# Windows
rmdir /s /q frontend\node_modules\.cache
npm cache clean --force

# Mac/Linux
rm -rf frontend/node_modules/.cache
npm cache clean --force
```

---

## Common Issues

### Issue: "Cannot find module" in React
```bash
Solution: Reinstall dependencies
cd frontend
npm install
```

### Issue: Backend API gives 404
```bash
Solution: Check if backend is running on port 8000
# Terminal 1 should show: Uvicorn running on http://0.0.0.0:8000
```

### Issue: Frontend shows "Cannot connect to API"
```bash
Solution: Make sure:
1. Backend is running (Terminal 1)
2. React dev server is running (Terminal 2)
3. Check browser console for errors
4. API base path is /api (not http://localhost:8000/api)
```

### Issue: Port Already in Use
```bash
# Port 8000 in use
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

---

## NPM Scripts Available

```bash
# In frontend/
npm start              # Start dev server on :3000
npm run build          # Build for production
npm test               # Run tests
npm run eject          # Advanced: eject from create-react-app

# In backend/
python main.py         # Run development server
gunicorn main:app      # Run production server (like Render)
```

---

## Environment Variables for Local Dev

No special setup needed! Just run both servers:

```
Frontend (http://localhost:3000):
  → Uses relative path /api for all API calls
  → Automatically routes to http://localhost:8000

Backend (http://localhost:8000):
  → Serves both API and static files
  → Loads React build if it exists
  → Falls back to API message if React not built
```

---

## Testing Dataset Upload

1. Create a test CSV file:
   ```csv
   feature1,feature2,feature3,target
   1.2,3.4,5.6,0
   2.1,4.3,6.5,1
   ```

2. Upload via web interface at `http://localhost:3000`
3. Run predictions
4. Check results in real-time

---

## Quick Start Commands (Copy & Paste)

### Terminal 1 (Backend)
```bash
cd c:\Users\shoai\ml-web-app\backend && pip install -r requirements.txt && python main.py
```

### Terminal 2 (Frontend)
```bash
cd c:\Users\shoai\ml-web-app\frontend && npm install && npm start
```

Then open: `http://localhost:3000`

---

## Switching Between Development Methods

### To go from Method 1 to Method 2:
```bash
# Stop React dev server (Ctrl+C in Terminal 2)
# Build frontend
cd frontend && npm run build

# Backend still on Terminal 1 will now serve the built files
# Just refresh browser at http://localhost:8000
```

### To go from Method 2 to Method 1:
```bash
# Stop backend (Ctrl+C in Terminal 1)
# Delete build (optional, keeps things fresh)
rm -r frontend/build

# Restart backend (Terminal 1)
python main.py

# Start React dev server (Terminal 2)
cd frontend && npm start
```

---

## Production Simulation

To test exactly how it runs on Render:

```bash
# Build frontend production build
cd frontend && npm run build

# Install production Python dependencies
cd ../backend && pip install -r requirements-prod.txt

# Run with Gunicorn (like on Render)
gunicorn -w 4 -b 0.0.0.0:8000 main:app --timeout 120
```

Then open: `http://localhost:8000`

---

## Next Steps

1. Run locally using Method 1 (dev mode)
2. Test all features work
3. When ready, build frontend: `npm run build`
4. Commit to GitHub
5. Deploy to Render (following START_HERE.md)

---

**Pro Tip:** Use Method 1 during development (fast reload), then use Method 2 to verify before deploying! 🚀
