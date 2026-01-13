# StockSense Deployment Guide (React + FastAPI)

## 🚀 Deployment Overview

Your application uses **2 separate repositories** requiring separate deployment:
- **Frontend**: React + Vite → Deploy to Vercel/Netlify
- **Backend**: FastAPI → Deploy to Railway/Render

---

## 📊 Recommended Stack (2026)

### ✅ BEST OPTION (Free & Easy)
| Component | Platform | Cost | Setup Time |
|-----------|----------|------|-----------|
| Frontend | **Vercel** | Free | 5 min |
| Backend | **Railway** | Free | 10 min |
| **Total** | - | **$0/month** | **15 min** |

### ✅ ALTERNATIVE
| Component | Platform | Cost | Setup Time |
|-----------|----------|------|-----------|
| Frontend | **Netlify** | Free | 5 min |
| Backend | **Render** | Free | 10 min |
| **Total** | - | **$0/month** | **15 min** |

---

## 🎯 QUICK START DEPLOYMENT (15 minutes)

### Prerequisites
- GitHub account (already set up)
- Vercel account (free)
- Railway account (free)
- Both repos already pushed to GitHub

### Your Repos
- Frontend: https://github.com/shashi9933/stocksense_frontend.git
- Backend: https://github.com/shashi9933/stocksense_backend.git

---

## STEP 1: Deploy Frontend to Vercel (5 minutes)

### A. Create Vercel Account
1. Go to **vercel.com**
2. Click "Sign Up"
3. Select "GitHub"
4. Authorize your GitHub account
5. Create free account

### B. Import Frontend Project
1. Click "New Project"
2. Select "Import Git Repository"
3. Search for **stocksense_frontend**
4. Click "Import"

### C. Configure Build Settings
Vercel auto-detects Vite. Verify:
- **Framework**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install --legacy-peer-deps`

### D. Add Environment Variables
1. Click "Environment Variables"
2. Add:
   ```
   Name: VITE_API_URL
   Value: https://stocksense-backend.railway.app
   ```
   (We'll get the exact Railway URL in next step)

### E. Deploy
1. Click "Deploy"
2. Wait for build (~2-3 minutes)
3. Get your URL: `https://stocksense-frontend-xxx.vercel.app`

---

## STEP 2: Deploy Backend to Railway (10 minutes)

### A. Create Railway Account
1. Go to **railway.app**
2. Click "Login"
3. Select "Continue with GitHub"
4. Authorize GitHub account

### B. New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Search for **stocksense_backend**
4. Click "Import and Deploy"

### C. Configure Backend
1. Wait for auto-detection (should find Python)
2. If needed, set **Start Command**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### D. Add Environment Variables
1. Go to Variables section
2. Add:
   ```
   PYTHONUNBUFFERED=1
   PORT=8000
   ```

### E. Deploy & Get URL
1. Click "Deploy"
2. Wait for build (~3-5 minutes)
3. Get your backend URL: `https://stocksense-backend-xxx.railway.app`

### F. Test Backend
1. Visit: `https://your-backend-url/docs`
2. Should see Swagger UI
3. Try the `/api/popular-stocks` endpoint
4. Should get JSON response

---

## STEP 3: Connect Frontend to Backend (2 minutes)

### A. Update Vercel Environment Variable
1. Go to Vercel Dashboard
2. Project: **stocksense_frontend**
3. Settings → Environment Variables
4. Update `VITE_API_URL`:
   ```
   VITE_API_URL=https://your-railway-backend-url
   ```
   (Use the exact URL from Railway)

### B. Redeploy Frontend
1. Vercel auto-redeploys on git push
2. Or: Deployments → Click latest → Redeploy
3. Wait for build (~2 minutes)

### C. Test Connection
1. Visit your Vercel frontend URL
2. Open DevTools (F12) → Network tab
3. Search for a stock (e.g., "AAPL")
4. Watch Network tab for API calls
5. Should see calls to your backend URL
6. Data should load correctly

---

## 🔐 CORS Configuration (If API Errors)

If you get CORS errors in browser console:

### Update Backend (main.py)
```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stocksense-frontend-xxx.vercel.app",  # Your Vercel URL
        "http://localhost:5173",  # Local dev
        "http://localhost:3000",  # Alternative local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then:
1. Commit and push to GitHub
2. Railway auto-rebuilds
3. Redeploy Frontend in Vercel
4. Test again

---

## 📋 Verification Checklist

After deployment, test these:

### Frontend
- [ ] Website loads (no blank page)
- [ ] Sidebar visible and clickable
- [ ] Page navigation works
- [ ] No console errors (F12)
- [ ] Mobile responsive (zoom to 50%)

### Backend
- [ ] API docs work: `/docs` endpoint
- [ ] Health check: `GET /` returns success
- [ ] Stock search: `GET /api/search?query=AAPL` returns data
- [ ] Popular stocks: `GET /api/popular-stocks` works

### Integration
- [ ] Frontend can call backend
- [ ] Data loads in frontend
- [ ] Charts/indicators display
- [ ] Search finds stocks
- [ ] No network errors

---

## 🌐 Custom Domain (Optional - $10-15/year)

### A. Buy Domain
- GoDaddy, Namecheap, Google Domains
- Cost: ~$10-15/year

### B. Point to Vercel
1. Vercel Dashboard → Project Settings
2. Domains → Add Domain
3. Follow Vercel's DNS instructions
4. Add DNS records in domain provider
5. Takes 15-60 minutes to propagate

### C. Custom Backend URL
1. Railway → Project Settings
2. Custom Domain
3. Add your domain
4. Update CORS and frontend env variables
5. Redeploy both

---

## 🔄 Auto-Deployment Setup

Both platforms auto-deploy on GitHub push:

### Frontend (Vercel)
- Every push to `main` → Auto builds & deploys
- Staging deployments for PRs available
- Rollback to previous versions anytime

### Backend (Railway)
- Every push to `main` → Auto builds & deploys
- View logs in Railway dashboard
- One-click redeploy if needed

---

## 📊 Cost Breakdown

### Option 1: Free (Recommended for MVP)
```
Vercel Frontend:  $0   (100 GB bandwidth/month free)
Railway Backend:  $0   (Free tier sufficient for <1000 users)
Domain:           $0   (optional, ~$1/month if added)
────────────────────────
Monthly Total:    $0
```

### Option 2: Production Scale ($30-50/month)
```
Vercel Pro:       $20  (Unlimited deployments)
Railway Paid:     $5-15 (More compute)
Database:         $15+ (PostgreSQL, if needed)
────────────────────────
Monthly Total:    $40-50
```

---

## 🚨 Common Issues & Fixes

### Issue 1: "Cannot connect to API"
**Error**: Frontend shows "Failed to fetch"
**Cause**: Wrong backend URL in `VITE_API_URL`
**Fix**: 
1. Double-check Railway backend URL
2. Update Vercel environment variable
3. Redeploy frontend

### Issue 2: "CORS error in console"
**Error**: "Access-Control-Allow-Origin" error
**Cause**: Frontend URL not in backend CORS allowed list
**Fix**:
1. Update backend `main.py` CORS origins
2. Add your Vercel URL to allowed origins
3. Commit, push, Railway auto-rebuilds
4. Redeploy frontend

### Issue 3: "502 Bad Gateway"
**Error**: Backend returns error on API call
**Cause**: Backend crashed or not responding
**Fix**:
1. Check Railway logs (Project → Logs tab)
2. Look for Python errors
3. Click Redeploy button
4. Check if API dependencies installed

### Issue 4: "Build fails in Vercel"
**Error**: Deployment shows "Build failed"
**Cause**: Missing dependencies or build error
**Fix**:
1. Check Vercel build logs
2. Ensure `npm install` runs correctly
3. Verify `npm run build` works locally
4. Check for missing environment variables

### Issue 5: "Blank page on frontend"
**Error**: Website loads but shows nothing
**Cause**: Build output wrong or React not mounting
**Fix**:
1. Check Vercel logs for build errors
2. Ensure `dist/index.html` exists
3. Check browser console (F12) for JS errors
4. Try hard refresh (Ctrl+Shift+R)

---

## ✅ Full Deployment Checklist

```
PRE-DEPLOYMENT
[ ] Frontend repo pushed to GitHub
[ ] Backend repo pushed to GitHub
[ ] Both repos are public
[ ] GitHub account verified

FRONTEND DEPLOYMENT (VERCEL)
[ ] Vercel account created
[ ] Frontend project imported
[ ] Build command correct
[ ] Output directory: dist
[ ] Deployment successful
[ ] URL obtained & noted

BACKEND DEPLOYMENT (RAILWAY)
[ ] Railway account created
[ ] Backend project imported
[ ] Start command set
[ ] Environment variables added
[ ] Deployment successful
[ ] URL obtained & noted
[ ] API docs accessible (/docs)

INTEGRATION
[ ] Frontend environment variables updated
[ ] VITE_API_URL points to backend
[ ] Frontend redeployed
[ ] No CORS errors in console
[ ] API calls working
[ ] Data loading correctly

TESTING
[ ] Frontend loads without errors
[ ] All pages accessible
[ ] Stock search works
[ ] Charts display data
[ ] No 404 errors
[ ] Mobile responsive
[ ] No console errors (F12)

FINAL
[ ] Production URLs documented
[ ] Error monitoring setup
[ ] Performance acceptable
[ ] All features working
[ ] Ready for users!
```

---

## 🎯 Next Steps After Deployment

### Week 1
- Monitor logs for errors
- Get user feedback
- Fix any issues
- Document setup process

### Month 1
- Analyze performance metrics
- Optimize slow endpoints
- Scale if traffic increases
- Add monitoring alerts

### Ongoing
- Weekly: Check logs & metrics
- Monthly: Security updates
- Quarterly: Major feature releases
- Yearly: Infrastructure review

---

## 📞 Troubleshooting Links

- **Vercel Issues**: https://vercel.com/support
- **Railway Issues**: https://docs.railway.app
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment
- **Vite Build Issues**: https://vitejs.dev/guide

#### Step 4: Add Remote Repository
```bash
git remote add origin https://github.com/shashi9933/stockedge.git
```

#### Step 5: Push to GitHub
```bash
git push -u origin main
```

---

### PHASE 2: Create .gitignore (IMPORTANT!)
Create a `.gitignore` file before pushing to exclude unnecessary files:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Streamlit
.streamlit/
.cache/

# API Keys & Secrets
.env
.env.local
secrets.toml

# Data & Logs
*.log
*.db
*.sqlite
```

---

### PHASE 3: Prepare for Deployment

#### Create `requirements.txt` (CRITICAL!)
This file tells the deployment platform which packages to install:

```
streamlit>=1.44.1
pandas>=2.2.3
numpy>=2.2.4
yfinance>=0.2.55
plotly>=6.0.1
scikit-learn>=1.6.1
scipy>=1.15.2
statsmodels>=0.14.4
twilio>=9.5.1
anthropic>=0.49.0
openai>=1.70.0
```

#### Create `config.toml` for Streamlit
Location: `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
maxUploadSize = 200
enableXsrfProtection = true

[logger]
level = "info"
```

#### Create `runtime.txt` (Specifies Python version)
```
python-3.11.0
```

---

### PHASE 4: RECOMMENDED DEPLOYMENT - Streamlit Cloud

#### Step 1: Connect GitHub Account
1. Go to https://share.streamlit.io/
2. Click "New app"
3. Sign in with GitHub
4. Authorize Streamlit

#### Step 2: Deploy Your App
1. Select Repository: `shashi9933/stockedge`
2. Select Branch: `main`
3. Select File: `app.py`
4. Click "Deploy"

#### Step 3: Wait for Deployment
- Streamlit automatically installs dependencies from `requirements.txt`
- Takes 2-5 minutes
- You'll get a public URL like: `https://stocksense-xxxxx.streamlit.app`

#### Step 4: Auto-Updates
- Every push to GitHub automatically redeploys your app
- No manual steps needed

---

### PHASE 5: Alternative - Hugging Face Spaces (Even Easier!)

#### Step 1: Create Space
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Name: `stocksense`
4. Select "Docker" as runtime
5. Create Space

#### Step 2: Clone and Push
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/stocksense
cd stocksense

# Copy your app files here
# Then:
git add .
git commit -m "Add StockSense"
git push
```

#### Step 3: Create Dockerfile (if needed)
```dockerfile
FROM python:3.11-slim

RUN pip install streamlit pandas numpy yfinance plotly scikit-learn scipy statsmodels

WORKDIR /app
COPY . .

CMD ["streamlit", "run", "app.py"]
```

---

## COMPLETE WORKFLOW SUMMARY

```
1. Setup GitHub Repo
   ↓
2. Create requirements.txt
   ↓
3. Create .gitignore
   ↓
4. Push to GitHub
   ↓
5. Deploy to Streamlit Cloud (Recommended)
   OR Alternative Platform
   ↓
6. App is LIVE!
```

---

## COMMANDS CHEAT SHEET

### Initialize Git (First Time Only)
```bash
cd e:\Coding\stocksense\StockSense
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/shashi9933/stockedge.git
git push -u origin main
```

### Update Deployment (After Local Changes)
```bash
git add .
git commit -m "Update: [description]"
git push origin main
# Deployment updates automatically!
```

---

## IMPORTANT CONSIDERATIONS

### 1. **Environment Variables & Secrets**
If using Twilio or API keys:
- Store in `.streamlit/secrets.toml` (local)
- Add to platform's secrets manager before deployment
- Never commit API keys to GitHub!

### 2. **Data Storage**
- Session data is temporary (clears on app restart)
- For persistent alerts: implement SQLite or cloud database
- Use Streamlit's session state carefully

### 3. **Performance**
- Caching improves speed (already implemented)
- First-time load ~30 seconds
- Subsequent loads ~2 seconds

### 4. **Limitations**
- Streamlit Cloud free tier: 1 GB RAM
- App sleeps after 7 days of inactivity
- Upgrade to Pro for more resources ($10/month)

---

## TROUBLESHOOTING

### App Won't Deploy
- Check `requirements.txt` syntax
- Ensure `app.py` is in root directory
- Check for Python syntax errors

### ImportError After Deployment
- Add missing package to `requirements.txt`
- Push update to GitHub
- Wait for auto-redeploy

### App Too Slow
- Check for expensive operations in `@st.cache_data`
- Reduce data fetching frequency
- Optimize prediction models

---

## POST-DEPLOYMENT

### Monitor Your App
- Streamlit Cloud dashboard shows usage
- Check logs for errors
- Monitor API rate limits (yfinance)

### Share Your App
- URL: `https://your-app-name.streamlit.app`
- Share with users/investors
- Collect feedback

### Next Steps for Production
1. Add user authentication
2. Implement database for persistent storage
3. Add email/SMS notifications
4. Custom domain setup
5. Premium Streamlit features

