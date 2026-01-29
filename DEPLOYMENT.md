# Deployment Guide

## 🚀 Deploy Your Translator

Your application is ready for production deployment! Here are several options:

---

## 1. 🟢 Heroku (Easiest)

### Prerequisites
- Heroku account (free at heroku.com)
- Heroku CLI installed
- Git installed

### Steps

```bash
# Login to Heroku
heroku login

# Create Procfile in project root
echo "web: gunicorn app:app" > Procfile

# Create runtime.txt for Python version
echo "python-3.9.16" > runtime.txt

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Create Heroku app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

**Free tier includes**: 550 hours/month (always on = ~23 hours/day)

---

## 2. 🐳 Docker (Most Flexible)

### Prerequisites
- Docker installed
- Docker Hub account (optional, for sharing)

### Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 5000

# Run app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

### Build and Run

```bash
# Build image
docker build -t kannada-translator .

# Run container
docker run -p 5000:5000 kannada-translator

# Push to Docker Hub
docker tag kannada-translator your-username/kannada-translator
docker push your-username/kannada-translator
```

---

## 3. ☁️ AWS (Scalable)

### Option A: AWS Elastic Beanstalk

```bash
# Install AWS CLI and EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 kannada-translator

# Create environment
eb create kannada-translator-env

# Deploy
eb deploy

# View app
eb open
```

### Option B: AWS EC2

1. Launch Ubuntu EC2 instance
2. SSH into instance
3. Install Python, pip, git
4. Clone repository
5. Setup virtual environment
6. Install dependencies
7. Run with Gunicorn + Nginx

```bash
# On EC2 instance
ssh -i your-key.pem ubuntu@instance-ip

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install -y python3-pip python3-venv nginx

# Clone repository
git clone your-repo-url
cd English_to_kannada_translator

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with Gunicorn
gunicorn app:app --bind 0.0.0.0:5000 &
```

---

## 4. 🔵 Google Cloud Run

### Prerequisites
- Google Cloud account
- gcloud CLI installed
- Docker installed

### Deploy

```bash
# Authenticate
gcloud auth login

# Create Dockerfile (see above)

# Build and push to Cloud Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/kannada-translator

# Deploy to Cloud Run
gcloud run deploy kannada-translator \
  --image gcr.io/PROJECT_ID/kannada-translator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 5. 🟣 Microsoft Azure

### Steps

1. Create Azure Container Registry
2. Build Docker image
3. Push to registry
4. Create App Service
5. Deploy from container

```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# Create App Service plan
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku FREE --is-linux

# Create web app
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myapp --deployment-container-image-name-user

# Configure container
az webapp config container set --name myapp --resource-group myResourceGroup --docker-custom-image-name gcr.io/PROJECT_ID/kannada-translator
```

---

## 6. 🟡 PythonAnywhere (Simple)

### Steps

1. Go to pythonanywhere.com
2. Create account (free tier available)
3. Upload files via Web interface
4. Configure WSGI file
5. Add web app
6. Reload

### WSGI Configuration

Create `mysite_wsgi.py`:

```python
import sys
path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

---

## 7. 🖥️ DigitalOcean (Affordable)

### Prerequisites
- DigitalOcean account
- SSH key configured

### Manual Deployment

```bash
# Create droplet (Ubuntu 20.04)
# SSH into droplet
ssh root@your.droplet.ip

# Setup
apt-get update && apt-get upgrade -y
apt-get install -y python3-pip python3-venv nginx git

# Clone and setup
git clone your-repo
cd English_to_kannada_translator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Nginx
# Edit /etc/nginx/sites-available/default
# Point to localhost:5000

# Run with supervisor for auto-restart
sudo apt-get install supervisor
# Configure supervisor config
# Start: supervisorctl reread && supervisorctl update
```

### Using App Platform

1. Connect GitHub repo
2. Select branch (main)
3. Configure build/run commands
4. Deploy!

---

## 8. 🎁 Railway (New & Easy)

### Steps

1. Go to railway.app
2. Connect GitHub
3. Select repository
4. Set environment variables
5. Deploy!

```bash
# No additional setup needed!
# Railway automatically detects Python
# Installs from requirements.txt
# Runs with gunicorn
```

---

## Production Checklist

### Before Deploying

- [ ] Test all features locally
- [ ] Set `debug=False` in app.py
- [ ] Configure proper logging
- [ ] Add error monitoring
- [ ] Set environment variables
- [ ] Use strong secrets
- [ ] Test with real data
- [ ] Performance test
- [ ] Security audit

### After Deploying

- [ ] Test all endpoints
- [ ] Monitor logs
- [ ] Setup uptime monitoring
- [ ] Configure auto-scaling
- [ ] Enable backups
- [ ] Setup CI/CD pipeline
- [ ] Document deployment
- [ ] Create runbook

---

## Environment Variables (Production)

Create `.env` for production:

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

---

## Scaling Considerations

### For High Traffic

1. **Database**: Add persistent storage
2. **Cache**: Use Redis
3. **CDN**: Serve static files from CDN
4. **Monitoring**: Setup alerts
5. **Load Balancing**: Multiple instances
6. **Auto-scaling**: Based on CPU/memory

### Configuration Examples

**Gunicorn with multiple workers**:
```bash
gunicorn app:app --workers 4 --worker-class sync --bind 0.0.0.0:5000
```

**Nginx reverse proxy** (add to nginx.conf):
```nginx
upstream flask_app {
    server localhost:5000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/static/;
        expires 30d;
    }
}
```

---

## Cost Comparison

| Platform | Free Tier | Price | Best For |
|----------|-----------|-------|----------|
| Heroku | 550 hrs/mo | $7/mo | Development |
| Railway | 5GB RAM | $5/mo | Small apps |
| Render | ✅ | $7/mo | Static only |
| PythonAnywhere | ✅ | $5/mo | Simple |
| AWS Free | ✅ (1 yr) | Variable | Enterprise |
| DigitalOcean | ✅ | $4/mo | Custom |
| GCP | ✅ ($300) | Variable | Google services |
| Azure | ✅ ($200) | Variable | Microsoft stack |

---

## Monitoring & Analytics

### Popular Tools

1. **Error Tracking**: Sentry
2. **Uptime Monitoring**: UptimeRobot
3. **Analytics**: Google Analytics
4. **Performance**: New Relic
5. **Logs**: CloudWatch, Stackdriver

### Basic Setup

```python
# Add to app.py for error tracking
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    "your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

---

## HTTPS/SSL Certificates

Most platforms provide free HTTPS:
- Heroku: Automatic
- Railway: Automatic
- AWS: Use ACM
- DigitalOcean: Use Let's Encrypt

---

## Troubleshooting Deployment

### App won't start
```bash
# Check logs
heroku logs --tail  # Heroku
eb logs  # AWS EB

# Common issues:
# - Missing dependencies
# - Wrong Python version
# - Port conflicts
# - Missing environment variables
```

### Static files not loading
```bash
# Ensure Flask serves static files
app = Flask(__name__, static_folder='static')

# Or use whitenoise
pip install whitenoise
```

### Database connection errors
- Check connection strings
- Verify network access
- Check credentials
- Test from deployment environment

---

## Next Steps

1. Choose a platform
2. Follow deployment guide
3. Test thoroughly
4. Monitor logs
5. Celebrate! 🎉

---

**Successfully deploy your translator!** 🚀

For platform-specific help, visit their documentation websites.
