# Render Deployment Fix - Cached Start Command Issue

## Problem
Render.com is using a **CACHED START COMMAND** from a previous manual deployment that runs:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

But `uvicorn` is **NOT installed** in requirements.txt. Instead, `gunicorn==21.2.0` is installed.

**Error from Render deploy logs:**
```
==> Running 'cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT'
bash: line 1: uvicorn: command not found
==> Exited with status 127
```

## Root Cause
When you first deployed to Render, the Start Command was manually set to use uvicorn. Now, even though render.yaml specifies gunicorn, Render's service configuration cache is taking precedence over the Blueprint.

## Solution: Manual Override on Render UI

### Step 1: Update Start Command on Render Dashboard
1. Go to https://render.com/dashboard
2. Click on **`ml-cv-prediction-backend`** service
3. Click **Settings** tab (on the left sidebar)
4. Scroll down to **"Start Command"** field
5. **Replace the current value** with:
   ```
   cd backend && gunicorn -w 2 -b 0.0.0.0:8000 main:app --timeout 120 --access-logfile - --error-logfile -
   ```
6. Click **"Save Changes"** button
7. Click **"Manual Deploy"** button
8. Click **"Deploy latest commit"**

### Step 2: Verify Deployment
- Check the deployment logs for: `✓ Deploy successful`
- Verify the app responds at: https://ml-cv-prediction-backend.onrender.com/api/health/status

## Configuration Files (All Correct ✓)

### render.yaml - ✓ CORRECT
- StartCommand: `cd backend && gunicorn -w 2 -b 0.0.0.0:8000 main:app --timeout 120 --access-logfile - --error-logfile -`
- BuildCommand: `cd backend && pip install -r requirements.txt`

### Procfile - ✓ CORRECT  
- Web: `cd backend && gunicorn -w 2 -b 0.0.0.0:${PORT:-8000} main:app --timeout 120 --access-logfile - --error-logfile -`

### requirements.txt - ✓ CORRECT
- Contains: `gunicorn==21.2.0`

## Alternative: Full Blueprint Redeploy (If manual override fails)

If the manual override doesn't work:

1. Go to https://render.com/dashboard
2. Click `ml-cv-prediction-backend` → **Settings** → **Danger Zone** → **Delete Service**
3. Confirm deletion
4. Wait 30 seconds
5. Go to https://render.com/blueprints
6. Find your deployment for this project
7. Click **Create New Deployment**
8. Render will read render.yaml fresh and deploy with correct configuration

## Status
- **Code:** Production ready ✓
- **Configuration:** Production ready ✓
- **Dependencies:** All installed (gunicorn, Flask, TensorFlow, etc.) ✓
- **Issue:** Render cache only - no code changes needed
