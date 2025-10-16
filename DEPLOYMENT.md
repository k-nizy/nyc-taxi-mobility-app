# 🚀 Deployment Guide - NYC Taxi Analytics

## Frontend Deployment (Vercel)

### Quick Deploy

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_REPO_URL
git push -u origin main
```

2. **Deploy to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect React app in `frontend/` folder

3. **Configure Project:**
   - **Root Directory:** Leave blank (Vercel will use vercel.json)
   - **Framework Preset:** Create React App
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Output Directory:** `frontend/build`

4. **Environment Variables:**
   Add in Vercel dashboard under Settings > Environment Variables:
   ```
   REACT_APP_API_URL=https://your-backend-url.com
   ```

5. **Deploy:** Click "Deploy" and wait 2-3 minutes

---

## Backend Deployment Options

### Option 1: Render.com (Recommended - Free Tier)

1. **Create Web Service:**
   - Go to [render.com](https://render.com)
   - New > Web Service
   - Connect your GitHub repo
   - Select `backend` as root directory

2. **Configuration:**
   - **Name:** nyc-taxi-api
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

3. **Environment Variables:**
   ```
   USE_SQLITE=true
   SECRET_KEY=your-random-secret-key
   ```

4. **Deploy** and copy the URL (e.g., `https://nyc-taxi-api.onrender.com`)

5. **Update Frontend:**
   - Go back to Vercel
   - Update `REACT_APP_API_URL` with your Render backend URL
   - Redeploy

---

### Option 2: Railway.app

1. **Create Project:**
   - Go to [railway.app](https://railway.app)
   - New Project > Deploy from GitHub
   - Select your repo

2. **Configuration:**
   - Railway auto-detects Python
   - Set root directory to `backend`
   - Add environment variables in Settings

3. **Generate Domain:**
   - Go to Settings > Generate Domain
   - Copy the URL

---

### Option 3: Heroku

1. **Create App:**
```bash
cd backend
heroku create your-app-name
```

2. **Add Buildpack:**
```bash
heroku buildpacks:set heroku/python
```

3. **Create Procfile** (if not exists):
```
web: gunicorn app:app
```

4. **Deploy:**
```bash
git push heroku main
```

---

## Post-Deployment Checklist

- [ ] Backend is accessible and returns data
- [ ] Test health endpoint: `https://your-backend-url/health`
- [ ] Frontend loads without errors
- [ ] API calls work from frontend
- [ ] Environment variables are set correctly
- [ ] Database has sample data (or add via backend scripts)

---

## Troubleshooting

### Frontend shows "Network Error"
- Check `REACT_APP_API_URL` is set correctly in Vercel
- Ensure backend URL includes `https://` and no trailing slash
- Verify CORS is enabled in backend (`Flask-CORS` is installed)

### Backend fails to start
- Check Python version (should be 3.8+)
- Verify all dependencies in `requirements.txt` are installed
- Check logs for specific error messages

### Database errors
- Ensure `nyc_taxi.db` file exists or is created on startup
- For SQLite, make sure `USE_SQLITE=true` environment variable is set

---

## Free Tier Limits

**Vercel:**
- 100 GB bandwidth/month
- Unlimited deployments
- Custom domains

**Render.com:**
- 750 hours/month (free tier)
- Spins down after 15min inactivity
- Takes ~30s to wake up

**Railway.app:**
- $5 free credit/month
- ~500 hours runtime

---

## Custom Domain (Optional)

### Vercel (Frontend)
1. Go to Project Settings > Domains
2. Add your domain
3. Update DNS records as shown

### Render/Railway (Backend)
1. Go to Settings > Custom Domain
2. Add your domain
3. Update DNS records

---

## Maintenance

**Update Deployment:**
```bash
git add .
git commit -m "Update features"
git push origin main
```

Vercel and most platforms auto-deploy on git push.

**View Logs:**
- Vercel: Dashboard > Deployment > View Function Logs
- Render: Dashboard > Logs tab
- Railway: Dashboard > Deployments > Logs

---

## Need Help?

- Check platform-specific documentation
- Review application logs for error messages
- Test backend API endpoints directly using Postman or curl
