# Deployment Guide

## Local Development

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

### Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

### Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

---

## Production Deployment

### Option 1: Render.com (Recommended)

#### Backend Deployment

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Select backend folder
   - Name: `ml-app-backend`

3. **Configure**
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`
   - Environment: Add from `.env`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for build (2-3 min)
   - Get URL: `https://ml-app-backend.onrender.com`

#### Frontend Deployment

1. **Build React**
   ```bash
   cd frontend
   npm run build
   ```

2. **Create Static Site on Render**
   - Click "New +" → "Static Site"
   - Connect GitHub
   - Name: `ml-app-frontend`
   - Build Command: `npm run build`
   - Publish Directory: `build`

3. **Update API URL**
   - In frontend/.env: 
   ```
   REACT_APP_API_URL=https://ml-app-backend.onrender.com/api
   ```

4. **Deploy**
   - Commit and push changes
   - Render auto-deploys

#### Update CORS on Backend
```python
# In main.py
CORS(app, origins=[
    "https://ml-app-frontend.onrender.com",
    "http://localhost:3000"  # Keep for dev
])
```

---

### Option 2: Docker Deployment

#### Create Dockerfile (backend)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create datasets directory
RUN mkdir -p datasets

# Expose port
EXPOSE 5000

# Run app
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000"]
```

#### Create Dockerfile (frontend)
```dockerfile
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

# Build React app
ENV REACT_APP_API_URL=/api
RUN npm run build

# Production server
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
```yaml
version: '3'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./backend/datasets:/app/datasets

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

#### Deploy Docker
```bash
# Build images
docker-compose build

# Run containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

### Option 3: Heroku (Legacy but still available)

#### Backend

1. **Create Procfile**
```
web: gunicorn main:app
```

2. **Create runtime.txt**
```
python-3.9.13
```

3. **Deploy**
```bash
heroku login
heroku create ml-app-backend
git push heroku main
```

#### Frontend

1. **Create buildpack**
```bash
heroku buildpacks:add heroku/nodejs --index 1
```

2. **Deploy**
```bash
git push heroku main
```

---

### Option 4: AWS Deployment

#### Backend (EC2)

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - Security group: Allow port 5000, 22

2. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3.9 python3-pip nginx

# Clone repo
git clone <your-repo>
cd backend

# Setup virtual env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn
```

3. **Create Systemd Service**
```bash
sudo nano /etc/systemd/system/ml-app.service
```

```ini
[Unit]
Description=ML Web App Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ml-web-app/backend
ExecStart=/home/ubuntu/ml-web-app/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable ml-app
sudo systemctl start ml-app
```

4. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/default
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo nginx -t
sudo systemctl restart nginx
```

#### Frontend (S3 + CloudFront)

1. **Build React**
```bash
npm run build
```

2. **Create S3 Bucket**
   - Upload contents of `build/` folder
   - Enable "Block public access" (use CloudFront)

3. **Create CloudFront Distribution**
   - Origin: S3 bucket
   - Set API URL in environment before build

---

## Environment Variables

### Backend (.env)
```
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=5000
UPLOAD_FOLDER=datasets
MAX_UPLOAD_SIZE=52428800
LOG_LEVEL=INFO
```

### Frontend (.env)
```
REACT_APP_API_URL=https://your-api-domain.com/api
```

---

## Monitoring & Logging

### Render.com
- Built-in logs: Dashboard → Logs
- Error tracking: Integrated
- Metrics: CPU, Memory usage

### Docker
```bash
# View logs
docker logs -f container-name

# Login to container
docker exec -it container-name bash

# Monitor resources
docker stats
```

### AWS EC2
```bash
# SSH into instance
ssh -i keyfile.pem ubuntu@ip-address

# View logs
tail -f /var/log/syslog
journalctl -u ml-app -f

# Monitor
top
ps aux | grep gunicorn
```

---

## Database Considerations (Future)

### PostgreSQL Setup
```bash
# Install
sudo apt install postgresql postgresql-contrib

# Create database
createdb ml_app
createdb -U postgres ml_app

# Connect
psql ml_app
```

### Update Flask
```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/ml_app'
db = SQLAlchemy(app)
```

---

## CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy Backend
      env:
        RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        RENDER_SERVICE_ID: ${{ secrets.RENDER_SERVICE_ID }}
      run: |
        curl -X POST https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys \
          -H "Authorization: Bearer $RENDER_API_KEY"
    
    - name: Deploy Frontend
      env:
        RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        RENDER_SERVICE_ID: ${{ secrets.RENDER_SERVICE_ID_FRONTEND }}
      run: |
        curl -X POST https://api.render.com/v1/services/$RENDER_SERVICE_ID_FRONTEND/deploys \
          -H "Authorization: Bearer $RENDER_API_KEY"
```

---

## Debugging Production Issues

### Backend Connection Issues
```bash
# Check if port is open
telnet your-domain.com 5000

# Check process
ps aux | grep gunicorn

# Check logs
tail -100 /var/log/application.log
```

### CORS Errors
Check backend CORS configuration:
```python
CORS(app, origins=["https://your-frontend.com"])
```

### Dataset Upload Fails
```bash
# Check permissions
ls -la datasets/
chmod 755 datasets/

# Check disk space
df -h

# Check upload size limit
# In nginx config: client_max_body_size 50M;
```

### Model Training Timeout
- Increase timeout on server
- Split large datasets
- Use smaller batch sizes

---

## SSL Certificate (HTTPS)

### Let's Encrypt (Free)
```bash
sudo apt install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d your-domain.com

# Auto-renew
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Update Nginx
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
}
```

---

## Backup Strategy

### Database Backup
```bash
# PostgreSQL
pg_dump ml_app > backup.sql
pg_restore -d ml_app backup.sql
```

### Dataset Backup
```bash
# Backup datasets folder
tar -czf datasets-backup.tar.gz datasets/

# Upload to cloud storage
aws s3 cp datasets-backup.tar.gz s3://your-bucket/
```

---

## Performance Optimization

### Caching Strategy
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/datasets/list')
@cache.cached(timeout=300)  # Cache for 5 minutes
def list_datasets():
    ...
```

### Database Indexing
```python
# In SQLAlchemy models
class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True)
```

### CDN Setup
- Use CloudFront for frontend assets
- Use CloudFlare for API caching

---

## Scaling Recommendations

### Current Single-Instance Setup
- Suitable for: Development, testing, < 100 users
- Performance: 1-5 min model training time
- Cost: ~$0-10/month (depending on provider)

### Medium Scale (100-1000 users)
- Database: Postgres
- Caching: Redis
- Load Balancer: Nginx
- API Server: 2-4 instances
- Cost: $50-200/month

### Large Scale (1000+ users)
- Kubernetes orchestration
- Auto-scaling groups
- Distributed training
- Dedicated model serving
- Cloud ML platforms

---

## Troubleshooting Deployment

| Problem | Solution |
|---------|----------|
| 503 Service Unavailable | Check backend logs, restart service |
| CORS errors | Update allowed origins in Flask |
| Timeout on training | Increase timeout, use background jobs |
| Out of memory | Reduce batch size, add more RAM |
| File upload fails | Check File size limit, permissions |
| Long load times | Enable caching, optimize frontend bundle |
| Model not training | Check dataset format, validate columns |

---

## Post-Deployment Checklist

- [ ] Backend running on production server
- [ ] Frontend accessible on HTTPS
- [ ] CORS properly configured
- [ ] Environment variables set
- [ ] Database backed up
- [ ] Datasets folder writable
- [ ] SSL certificate valid
- [ ] Monitoring/logging enabled
- [ ] Error tracking configured
- [ ] Load testing completed
- [ ] Stress tested with large datasets
- [ ] User documentation updated

---

**Ready to deploy? Follow the Render.com option above for quickest setup!**
