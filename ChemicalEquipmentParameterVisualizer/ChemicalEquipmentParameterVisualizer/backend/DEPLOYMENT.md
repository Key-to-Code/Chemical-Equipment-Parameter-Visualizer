# Django Backend Deployment Guide

This guide explains how to deploy the Chemical Equipment Parameter Visualizer Django backend to a public URL.

## Recommended Platforms

| Platform | Free Tier | Ease of Use | Best For |
|----------|-----------|-------------|----------|
| **Railway** | $5 credit/month | ⭐⭐⭐⭐⭐ | Beginners |
| **Render** | 750 hours/month | ⭐⭐⭐⭐ | Long-running apps |
| **PythonAnywhere** | Limited | ⭐⭐⭐ | Python-specific hosting |

---

## Option 1: Railway (Recommended)

Railway is the easiest option with automatic Django detection.

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account

### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your repository
4. Select your repository

### Step 3: Configure Root Directory
Since your backend is in a subdirectory:
1. Go to **Settings** → **Build**
2. Set **Root Directory** to: `ChemicalEquipmentParameterVisualizer/ChemicalEquipmentParameterVisualizer/backend`

### Step 4: Set Environment Variables
Go to **Variables** tab and add:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Generate at: https://djecrety.ir/ |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.up.railway.app` (Railway will provide this) |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` |

### Step 5: Deploy
Railway will automatically:
- Detect Django and Python
- Install dependencies from `requirements.txt`
- Run migrations
- Start the server using the `Procfile`

### Step 6: Get Your Public URL
Once deployed, Railway provides a URL like:
```
https://your-app-name.up.railway.app
```

Your API will be at: `https://your-app-name.up.railway.app/api`

---

## Option 2: Render

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Create Web Service
1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository

### Step 3: Configure Build Settings

| Setting | Value |
|---------|-------|
| Name | `chemical-equipment-api` |
| Root Directory | `ChemicalEquipmentParameterVisualizer/ChemicalEquipmentParameterVisualizer/backend` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| Start Command | `gunicorn equipment_api.wsgi:application` |

### Step 4: Add Environment Variables
In the **Environment** section:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Your generated secret key |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` |
| `PYTHON_VERSION` | `3.11.0` |

### Step 5: Deploy
Click **"Create Web Service"**. Render will build and deploy automatically.

Your API URL will be: `https://your-app.onrender.com/api`

---

## Option 3: PythonAnywhere

### Step 1: Create Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free "Beginner" account

### Step 2: Upload Code
1. Open a **Bash console**
2. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   ```

### Step 3: Set Up Virtual Environment
```bash
cd your-repo/ChemicalEquipmentParameterVisualizer/ChemicalEquipmentParameterVisualizer/backend
mkvirtualenv --python=/usr/bin/python3.11 myenv
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to **Web** tab
2. Click **"Add a new web app"**
3. Choose **Manual configuration** → **Python 3.11**

### Step 5: Configure WSGI
Edit the WSGI configuration file:
```python
import os
import sys

path = '/home/yourusername/your-repo/ChemicalEquipmentParameterVisualizer/ChemicalEquipmentParameterVisualizer/backend'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'equipment_api.settings'
os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['DEBUG'] = 'False'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 6: Set Static Files
In the **Web** tab, add:
- URL: `/static/`
- Directory: `/home/yourusername/your-repo/.../backend/staticfiles`

Run: `python manage.py collectstatic`

Your API URL: `https://yourusername.pythonanywhere.com/api`

---

## After Deployment

### 1. Run Migrations (if not automatic)
Most platforms run migrations automatically. If not:
```bash
python manage.py migrate
```

### 2. Update Frontend Environment
In your Vercel project, set:
```
VITE_API_URL=https://your-backend-url.com/api
```

### 3. Update CORS
Make sure `CORS_ALLOWED_ORIGINS` includes your Vercel frontend URL.

### 4. Test the API
Visit your backend URL in a browser:
- `https://your-backend.com/api/` - Should show the API root
- `https://your-backend.com/api/datasets/` - Should return empty list or data

---

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key (generate a secure one!) | `abc123xyz...` |
| `DEBUG` | Set to `False` in production | `False` |
| `ALLOWED_HOSTS` | Your deployment domain(s), comma-separated | `your-app.up.railway.app` |
| `CORS_ALLOWED_ORIGINS` | Frontend URL(s) allowed to access API | `https://your-frontend.vercel.app` |

---

## Troubleshooting

### "Disallowed Host" Error
Add your deployment domain to `ALLOWED_HOSTS` environment variable.

### CORS Errors
Make sure `CORS_ALLOWED_ORIGINS` includes your frontend URL (with `https://`).

### Static Files Not Loading
Run `python manage.py collectstatic` and ensure WhiteNoise is configured.

### Database Issues
SQLite works for demos but resets on some platforms. For persistent data, consider:
- Railway: Add PostgreSQL addon
- Render: Add PostgreSQL database
- PythonAnywhere: SQLite persists on free tier

---

## Quick Reference: Railway Deployment

```bash
# Your backend will be accessible at:
https://[your-app].up.railway.app/api

# API Endpoints:
POST /api/upload/          # Upload CSV
GET  /api/datasets/        # List datasets
GET  /api/datasets/{id}/   # Dataset detail
GET  /api/datasets/{id}/generate_pdf/  # Download PDF
```
