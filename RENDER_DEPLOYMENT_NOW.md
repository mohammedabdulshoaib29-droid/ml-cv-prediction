# 🚀 RENDER DEPLOYMENT - COMPLETE SETUP GUIDE
## ML-Based CV Behavior Prediction

### ✅ What's Been Done

Everything is configured and ready for deployment! Here's what was set up:

#### Backend Configuration
- ✅ FastAPI updated with environment-based CORS
- ✅ Production requirements file (`backend/requirements-prod.txt`)
- ✅ Gunicorn added for production serving
- ✅ Procfile configured for Render

#### Frontend Configuration
- ✅ React app updated to use environment variables for API URL
- ✅ HTML title and description updated
- ✅ App header renamed to "ML-Based CV Behavior Prediction"
- ✅ Build configuration ready

#### Deployment Files Created
1. **render.yaml** - Render deployment configuration
2. **Procfile** - Application startup configuration
3. **.env.example** - Environment variables template
4. **deploy.sh / deploy.bat** - Quick deployment scripts
5. **DEPLOYMENT_GUIDE.md** - Comprehensive guide
6. **RENDER_SETUP.md** - Render-specific setup
7. **.gitignore** - Proper Git ignore rules

---

## 📋 STEP-BY-STEP DEPLOYMENT

### Step 1: Prepare Your Local Repository

```bash
# Navigate to project directory
cd ml-web-app

# Initialize Git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: ML-Based CV Behavior Prediction ready for Render deployment"
```

### Step 2: Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click **New Repository**
3. Name it: `ml-cv-prediction` (or your preferred name)
4. Make it **Public** (required for free Render deployment)
5. **Do NOT** initialize with README

Then push your code:
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ml-cv-prediction.git
git push -u origin main
```

### Step 3: Create Render Account & Deploy Backend

1. Go to [render.com](https://render.com)
2. Click **Sign up** (use GitHub account for easy integration)
3. Authorize GitHub access
4. Click **New +** → **Web Service**
5. Select your `ml-cv-prediction` repository
6. Configure Backend Service:

| Setting | Value |
|---------|-------|
| **Name** | ml-cv-prediction-api |
| **Environment** | Python 3 |
| **Region** | Closest to your users |
| **Branch** | main |
| **Build Command** | `pip install -r backend/requirements-prod.txt` |
| **Start Command** | `cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT main:app --timeout 120` |
| **Instance Type** | Standard (minimum) |

7. **Add Environment Variables**:
   - Click **Advanced** → **Add Environment Variable**
   ```
   Key: CORS_ORIGINS
   Value: TBD (you'll set this after frontend deployment)
   ```
   
   ```
   Key: PYTHONUNBUFFERED
   Value: 1
   ```

8. Click **Create Web Service**
9. Wait for build (8-10 minutes)

### Step 4: Deploy Frontend

Once backend is deployed:

1. Click **New +** → **Static Site**
2. Select your repository
3. Configure Frontend Service:

| Setting | Value |
|---------|-------|
| **Name** | ml-cv-prediction-frontend |
| **Branch** | main |
| **Build Command** | `cd frontend && npm install && npm run build` |
| **Publish Directory** | `frontend/build` |

4. **Add Environment Variable**:
   ```
   Key: REACT_APP_API_URL
   Value: https://ml-cv-prediction-api.onrender.com
   ```

5. Click **Create Static Site**
6. Wait for deployment (3-5 minutes)

### Step 5: Link Backend & Frontend

1. Go to **ml-cv-prediction-api** service
2. Click **Environment** tab
3. Edit `CORS_ORIGINS`:
   ```
   https://ml-cv-prediction-frontend.onrender.com
   ```
4. Click **Save**
5. Service will redeploy automatically

### Step 6: Verify Deployment

✅ **Backend Health Check:**
```
https://ml-cv-prediction-api.onrender.com/health
```
Should return: `{"status":"healthy","message":"ML API is running"}`

✅ **Frontend:**
```
https://ml-cv-prediction-frontend.onrender.com
```
Should load the web interface

✅ **API Connection:**
- Upload a dataset in frontend
- Run a prediction
- Verify results display

---

## 🔒 Important: Free Tier Considerations

**Render Free Tier Limitations:**
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Limited resources (512MB RAM, shared CPU)

**Upgrade if needed:**
- Click service → **Settings** → **Instance Type**
- Upgrade to **Starter** or **Standard** for better performance

---

## 🎯 Your Deployment URLs

Once deployed, you'll have:
- **Backend API**: `https://ml-cv-prediction-api.onrender.com`
- **Frontend**: `https://ml-cv-prediction-frontend.onrender.com`
- **API Docs**: `https://ml-cv-prediction-api.onrender.com/docs`

---

## 🌐 Custom Domain (Optional)

To add a custom domain:

1. Go to frontend service
2. Click **Settings** → **Custom Domain**
3. Add your domain (e.g., `cv-prediction.com`)
4. Update DNS records as instructed
5. Wait for SSL certificate (5-10 minutes)

---

## 📊 Monitoring & Logs

**Backend Logs:**
1. Render Dashboard → `ml-cv-prediction-api`
2. Click **Logs** tab
3. View real-time logs for debugging

**Frontend Logs:**
1. Render Dashboard → `ml-cv-prediction-frontend`
2. Click **Logs** tab

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend build fails | Check `pip install -r backend/requirements-prod.txt` locally first |
| API not responding | Check CORS_ORIGINS environment variable matches frontend URL |
| Frontend shows blank | Check REACT_APP_API_URL environment variable is set |
| Timeout errors | Increase `--timeout` value in Procfile (default 120s) |
| Service spins down | Upgrade from free tier or use cron job to keep alive |

---

## ✨ Post-Deployment Tasks

### Update Documentation
- [ ] Update README.md with deployment URLs
- [ ] Document any custom configurations
- [ ] Create deployment checklist for team

### Monitor & Maintain
- [ ] Set up error notifications
- [ ] Monitor API response times
- [ ] Regularly update dependencies for security

### Optional Enhancements
- [ ] Add custom domain
- [ ] Enable auto-deploy on Git push
- [ ] Set up database (PostgreSQL) if needed
- [ ] Configure CI/CD pipeline

---

## 📞 Quick Support

**Issue**: Services won't communicate
```
✅ Solution: Verify CORS_ORIGINS and REACT_APP_API_URL environment variables
```

**Issue**: Long first request
```
✅ Solution: Normal on free tier (services spin down after 15 min)
         → Upgrade to Starter+ tier for always-on
```

**Issue**: ML model inference slow
```
✅ Solution: Upgrade Render instance type
         → Consider offloading heavy computation
```

---

## 🎉 You're All Set!

Your ML-Based CV Behavior Prediction application is ready to go live on Render!

**Next Step:** Follow the 6 deployment steps above to get your services running.

**Questions?** Check:
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Detailed technical guide
- [RENDER_SETUP.md](RENDER_SETUP.md) - Render-specific configuration
- [Render Documentation](https://render.com/docs) - Official Render docs

---

**Project:** ML-Based CV Behavior Prediction  
**Deployment Platform:** Render.com  
**Status:** ✅ Ready for Production  
**Last Updated:** April 2026
