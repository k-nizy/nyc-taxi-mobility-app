# Vercel Deployment Checklist

## Pre-Deployment Verification

### Files Cleaned Up ✓
- [x] Removed empty component files (BrandShowcase, Header, StatsCards, ThemeToggle)
- [x] Removed unnecessary docs (HOW_TO_RUN.md, ESSENTIAL_FILES.md, etc.)
- [x] Removed Python cache and venv
- [x] Removed data processing scripts (not needed for production)
- [x] Removed log files

### Essential Files Present ✓
- [x] `vercel.json` - Deployment configuration
- [x] `frontend/package.json` - Dependencies
- [x] `frontend/.env.example` - Environment template
- [x] `backend/.env.example` - Backend config template
- [x] `backend/nyc_taxi.db` - Database with sample data (3.7MB)
- [x] `README.md` - Updated with deployment instructions
- [x] `DEPLOYMENT.md` - Detailed deployment guide
- [x] `.gitignore` - Properly configured

### Current Structure
```
nyc-taxi-mobility-app/
├── backend/
│   ├── algorithms.py (16KB)
│   ├── app.py (18KB)
│   ├── models.py (7.6KB)
│   ├── nyc_taxi.db (3.7MB)
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/ (7 files)
│   │   ├── pages/ (5 files)
│   │   ├── services/ (1 file)
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   └── .env.example
├── .gitignore
├── .vercelignore
├── vercel.json
├── README.md
├── DEPLOYMENT.md
└── VERCEL_CHECKLIST.md
```

---

## Deployment Steps

### 1. Push to GitHub
```bash
# In your project directory
git init
git add .
git commit -m "Ready for Vercel deployment"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. Deploy Frontend to Vercel

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New Project"
4. Import your GitHub repository
5. Vercel will auto-detect the configuration from `vercel.json`
6. **IMPORTANT:** Add environment variable:
   ```
   Name: REACT_APP_API_URL
   Value: YOUR_BACKEND_URL (add after backend deployment)
   ```
7. Click "Deploy"

### 3. Deploy Backend

**Recommended: Render.com**

1. Go to https://render.com
2. New > Web Service
3. Connect GitHub repo
4. Settings:
   - **Name:** nyc-taxi-api
   - **Root Directory:** backend
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Environment Variables:
   ```
   USE_SQLITE=true
   SECRET_KEY=your-random-string
   ```
6. Click "Create Web Service"
7. Wait for deployment (~3 minutes)
8. Copy the deployed URL (e.g., https://nyc-taxi-api.onrender.com)

### 4. Connect Frontend to Backend

1. Go back to Vercel dashboard
2. Select your project
3. Go to Settings > Environment Variables
4. Update `REACT_APP_API_URL` with your Render backend URL
5. Go to Deployments tab
6. Click "..." on latest deployment > Redeploy

### 5. Test Deployment

- Visit your Vercel URL
- Check browser console for errors (F12)
- Test filtering and navigation
- Verify API calls are working

---

## Post-Deployment URLs

**Frontend (Vercel):**
- Production: `https://your-app.vercel.app`
- Dashboard: https://vercel.com/dashboard

**Backend (Render):**
- API: `https://your-app.onrender.com`
- Health check: `https://your-app.onrender.com/health`
- Dashboard: https://dashboard.render.com

---

## Common Issues & Fixes

### Issue: Frontend shows "Network Error"
**Fix:**
- Verify `REACT_APP_API_URL` is set in Vercel
- Ensure backend URL has no trailing slash
- Check backend is running (test health endpoint)

### Issue: Backend fails on Render
**Fix:**
- Check logs in Render dashboard
- Verify Python version is 3.8+
- Ensure all dependencies are in requirements.txt

### Issue: CORS errors
**Fix:**
- Backend already has Flask-CORS enabled
- Check backend logs for specific error

### Issue: Database not found
**Fix:**
- Ensure `nyc_taxi.db` is in repository
- Check `.gitignore` doesn't exclude .db files
- Verify `USE_SQLITE=true` is set

---

## File Sizes (for reference)

- Total repo size: ~5MB (without node_modules)
- Frontend build size: ~2MB
- Database: 3.7MB
- Backend code: ~42KB

---

## Next Steps After Deployment

1. Test all features on production URLs
2. Share URLs with team/instructor
3. Update README with actual deployment URLs
4. (Optional) Add custom domain
5. (Optional) Set up monitoring

---

## Maintenance

**Update deployment:**
```bash
git add .
git commit -m "Update message"
git push origin main
```

Both Vercel and Render will auto-deploy on push!

---

## Need Help?

- Check `DEPLOYMENT.md` for detailed instructions
- View platform logs for error messages
- Test API endpoints with curl or Postman
- Ensure environment variables are set correctly .
