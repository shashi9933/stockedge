# 🚀 DEPLOYMENT QUICK START (15 Minutes)

## Your Setup
- **Frontend**: stocksense_frontend (React + Vite)
- **Backend**: stocksense_backend (FastAPI)
- **Both on GitHub**: Ready to deploy

---

## ✅ 3-Step Deployment

### STEP 1: Deploy Frontend (5 min)
1. Go to **vercel.com**
2. Sign in with GitHub
3. Click "New Project"
4. Select **stocksense_frontend**
5. Click "Deploy"
6. Wait ~2-3 minutes
7. **Copy your URL**: `https://stocksense-frontend-xxx.vercel.app`

### STEP 2: Deploy Backend (10 min)
1. Go to **railway.app**
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select **stocksense_backend**
5. Click "Deploy"
6. Wait ~3-5 minutes
7. **Copy your URL**: `https://stocksense-backend-xxx.railway.app`

### STEP 3: Connect Them (2 min)
1. Go back to **Vercel**
2. Click **stocksense_frontend** project
3. Settings → Environment Variables
4. Add new variable:
   ```
   VITE_API_URL = https://stocksense-backend-xxx.railway.app
   ```
5. Click "Save"
6. Deployments → Redeploy
7. Done! ✅

---

## 🎉 You're Live!

### Test It
1. Visit your Vercel URL
2. Try searching for a stock
3. Should see data from your backend

### Share It
- Frontend: `https://stocksense-frontend-xxx.vercel.app`
- Backend API: `https://stocksense-backend-xxx.railway.app/docs`

---

## ❓ If Something Breaks

| Problem | Fix |
|---------|-----|
| API errors in browser | Update `VITE_API_URL` in Vercel |
| Backend gives 502 error | Check Railway logs, click Redeploy |
| CORS errors | Update backend `main.py` CORS origins |
| Page blank | Hard refresh (Ctrl+Shift+R) |

---

## 💰 Cost
**$0/month** (using free tiers)

More details in [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
