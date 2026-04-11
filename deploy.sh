#!/bin/bash
# Quick deployment script for Render

echo "🚀 ML-Based CV Behavior Prediction - Render Deployment"
echo "======================================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: ML-Based CV Behavior Prediction"
    echo "✅ Git repository initialized"
else
    echo "📦 Git repository already exists"
fi

echo ""
echo "📋 Next Steps to Deploy:"
echo "1. Push your code to GitHub/GitLab:"
echo "   git push origin main"
echo ""
echo "2. Go to https://render.com and sign up/login"
echo ""
echo "3. Create Backend Service:"
echo "   - New → Web Service"
echo "   - Connect your repository"
echo "   - Build Command: pip install -r backend/requirements-prod.txt"
echo "   - Start Command: cd backend && gunicorn -w 4 -b 0.0.0.0:\$PORT main:app --timeout 120"
echo "   - Add Environment Variable: CORS_ORIGINS=https://your-frontend-url.onrender.com"
echo ""
echo "4. Create Frontend Service:"
echo "   - New → Static Site"
echo "   - Connect your repository"
echo "   - Build Command: cd frontend && npm install && npm run build"
echo "   - Publish Directory: frontend/build"
echo "   - Add Environment Variable: REACT_APP_API_URL=https://your-backend-url.onrender.com"
echo ""
echo "5. Wait for builds to complete (5-15 minutes)"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo ""
