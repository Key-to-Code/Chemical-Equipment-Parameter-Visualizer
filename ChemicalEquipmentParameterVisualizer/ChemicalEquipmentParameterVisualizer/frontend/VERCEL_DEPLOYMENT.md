# Vercel Deployment Guide

This guide explains how to deploy the Chemical Equipment Parameter Visualizer React frontend to Vercel.

## Prerequisites

Before deploying, ensure you have:
- A [Vercel account](https://vercel.com/signup)
- Your Django backend deployed and accessible via a public URL
- The backend configured with proper CORS settings

## Quick Start

### 1. Connect Repository to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your Git repository
4. Vercel will auto-detect the Vite framework

### 2. Configure Environment Variables

In the Vercel project settings:

1. Navigate to **Settings** → **Environment Variables**
2. Add the following variable:

| Name | Value | Environment |
|------|-------|-------------|
| `VITE_API_URL` | `https://your-backend-url.com/api` | Production, Preview |

**Example values:**
- Production: `https://api.yourcompany.com/api`
- Preview: `https://staging-api.yourcompany.com/api`

### 3. Configure Build Settings

Vercel should auto-detect these settings, but verify:

| Setting | Value |
|---------|-------|
| Framework Preset | Vite |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Install Command | `npm install` |

### 4. Deploy

Click **"Deploy"** and Vercel will build and deploy your application.

---

## Backend CORS Configuration

Your Django backend must allow requests from your Vercel domain. Update your Django `settings.py`:

```python
# settings.py

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5000",           # Local development
    "http://localhost:4173",           # Vite preview
    "https://your-app.vercel.app",     # Production Vercel URL
    "https://your-custom-domain.com",  # Custom domain (if applicable)
]

# Or for development/testing, allow all origins (NOT recommended for production)
# CORS_ALLOW_ALL_ORIGINS = True
```

Also ensure you have `django-cors-headers` installed and configured:

```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

---

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `VITE_API_URL` | Full URL to your Django API (e.g., `https://api.example.com/api`) | Yes | `http://localhost:8000/api` |

> **Note:** Vite requires the `VITE_` prefix for environment variables to be accessible in the client-side code.

---

## Local Testing Before Deployment

### Test Production Build Locally

```bash
# Install dependencies (if not already done)
npm install

# Build for production
npm run build

# Preview the production build
npm run preview
```

The preview server runs at `http://localhost:4173`. Test all functionality:
- ✅ File upload
- ✅ Dataset list/history
- ✅ Dataset details with charts
- ✅ PDF download

---

## Deployment Checklist

Before deploying to production:

- [ ] Backend is deployed and accessible
- [ ] Backend CORS is configured for Vercel domain
- [ ] `VITE_API_URL` environment variable is set in Vercel
- [ ] Production build completes without errors (`npm run build`)
- [ ] All routes work correctly in preview mode
- [ ] File uploads work with the production backend
- [ ] PDF downloads work correctly
- [ ] Charts render properly

---

## Troubleshooting

### CORS Errors

**Symptom:** Console shows "Access-Control-Allow-Origin" errors

**Solution:**
1. Verify `VITE_API_URL` is set correctly (no trailing slash on base URL)
2. Add your Vercel domain to Django's `CORS_ALLOWED_ORIGINS`
3. Ensure `django-cors-headers` middleware is properly ordered

### API Connection Failed

**Symptom:** "Network Error" or timeout errors

**Solution:**
1. Check if `VITE_API_URL` is correctly set in Vercel
2. Verify the backend URL is accessible (try opening it in a browser)
3. Check if the backend server is running

### 404 on Page Refresh

**Symptom:** Refreshing on `/datasets` or `/datasets/:id` shows 404

**Solution:**
The `vercel.json` file includes rewrites to handle SPA routing. If you modified it, ensure the rewrite rules are intact:

```json
{
  "rewrites": [
    {
      "source": "/((?!assets/).*)",
      "destination": "/index.html"
    }
  ]
}
```

### Build Failures

**Symptom:** Build fails in Vercel

**Solution:**
1. Check Vercel build logs for specific errors
2. Ensure all dependencies are in `package.json`
3. Test build locally with `npm run build`

---

## Custom Domain Setup

To use a custom domain:

1. Go to **Settings** → **Domains** in Vercel
2. Add your custom domain
3. Configure DNS as directed by Vercel
4. Update backend CORS to include the custom domain

---

## Security Recommendations

For production deployments:

1. **Use HTTPS only** - Vercel provides this automatically
2. **Configure proper CORS** - Only allow specific origins, not all
3. **Set secure headers** - The `vercel.json` includes security headers
4. **Validate API responses** - Handle errors gracefully in the UI

---

## Support

For issues with:
- **Vercel deployment**: Check [Vercel Documentation](https://vercel.com/docs)
- **Django backend**: See the backend README
- **This frontend**: Check the project README or open an issue
