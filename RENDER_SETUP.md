# Render Deployment Guide

## Quick Setup for Render

This application is configured for automatic deployment on Render with the `render.yaml` configuration file.

### Prerequisites
- Render.com account (free tier available)
- GitHub repository connected to Render
- (Optional) Custom domain

### Automatic Deployment Steps

1. **Go to Render Dashboard**
   - Visit https://render.com
   - Sign in with GitHub account

2. **Create Blueprint Deployment**
   - Click "New" → "Blueprint"
   - Select your GitHub repository (ml-cv-prediction)
   - Render will automatically detect `render.yaml`
   - Click "Create"

3. **Wait for Deployment**
   - Render will automatically:
     - Deploy backend API service
     - Build and deploy frontend
     - Configure environment variables
     - Set up health checks
   - This takes 5-10 minutes

4. **Access Your App**
   - Backend API: `https://ml-cv-prediction-backend.onrender.com`
   - Frontend: Check Render dashboard for URL
   - Health check: `/api/health/status`

### Manual Deployment (Alternative)

If you prefer manual setup:

#### Deploy Backend
1. Create Web Service
   - Runtime: Python 3.11
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && gunicorn -w 2 -b 0.0.0.0:8000 main:app --timeout 120`
   - Environment Variables:
     ```
     FLASK_ENV=production
     UPLOAD_FOLDER=/tmp/datasets
     MAX_UPLOAD_SIZE=52428800
     ```

#### Deploy Frontend
1. Create Static Site
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/build`
   - Environment Variables:
     ```
     REACT_APP_API_URL=https://ml-cv-prediction-backend.onrender.com/api
     ```

### Managing Deployment

**View Logs**
- Render Dashboard → Services → Select service → Logs tab

**Update Code**
- Push to `main` branch
- Render automatically redeploys (if autoDeploy is enabled)

**Environment Variables**
- Render Dashboard → Environment tab
- Edit and deploy from there

### Troubleshooting

**Backend won't start**
- Check logs for Python errors
- Verify all packages in `requirements.txt` are compatible
- Ensure UPLOAD_FOLDER set to `/tmp` (persistent storage not available on free tier)

**Frontend can't reach API**
- Verify `REACT_APP_API_URL` matches backend URL
- Check CORS settings in `backend/main.py`
- Test API directly: `https://backend-url/api/health/status`

**Build fails**
- Check Node.js version compatibility
- Verify `npm install` in build logs succeeds
- Check backend Python version (3.11+)

**Timeout during training**
- Free tier has 30-second timeout for HTTP requests
- Model training takes 2-5 minutes
- Use Paid tier for longer-running tasks
- Or implement async job queue (future enhancement)

### Cost

**Free Tier (Included)**
- 750 hours per month per service
- Sufficient for hobby/learning projects
- Services spin down after 15 minutes of inactivity

**Paid Tiers Available**
- $7/month for always-on services
- Better performance, higher resource limits

### API Endpoints

All endpoints available at: `https://your-backend-url/api`

```
GET  /datasets/list              - List all datasets
POST /datasets/upload            - Upload new dataset
GET  /datasets/preview/{name}    - Preview dataset
DEL  /datasets/delete/{name}     - Delete dataset

POST /models/train               - Train models
POST /models/compare             - Compare models

GET  /health/status              - Health check
GET  /health/ready               - Readiness check
```

### Next Steps

1. Deploy to Render (follow steps above)
2. Test API endpoints
3. Upload datasets and train models
4. Monitor logs and adjust if needed
5. Upgrade to paid tier if needed for production

For more information, visit https://render.com/docs
