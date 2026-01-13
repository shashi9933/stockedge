# 🚀 DEPLOYMENT FLOW DIAGRAM

## Your Current Setup
```
┌─────────────────────────────────────────────────────────────┐
│                    LOCAL DEVELOPMENT                        │
│                                                             │
│  Frontend (React)          Backend (FastAPI)                │
│  localhost:5173     →      localhost:8000                   │
│  npm run dev               python main.py                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Push to GitHub (Done!)
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
   Frontend Repo                             Backend Repo
   stocksense_frontend                       stocksense_backend
   GitHub: Public                            GitHub: Public
```

---

## 📊 Deployment Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        YOUR USERS                            │
└──────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        ┌──────────────┐          ┌──────────────┐
        │   Frontend   │          │   Backend    │
        │   (Vercel)   │  ◄──────►│  (Railway)   │
        └──────────────┘  HTTPS   └──────────────┘
        https://xxx        REST   https://xxx
        .vercel.app        API    .railway.app
        
        React + Vite            FastAPI
        Tailwind CSS            Uvicorn
        Axios                   Python
```

---

## ⏱️ 15-Minute Deployment Timeline

```
0:00-5:00   Deploy Frontend (Vercel)
├── Sign in with GitHub
├── Select stocksense_frontend repo
├── Click Deploy
└── Wait for build

5:00-10:00  Deploy Backend (Railway)
├── Sign in with GitHub  
├── Select stocksense_backend repo
├── Click Deploy
└── Wait for build

10:00-15:00 Connect Them
├── Copy backend URL
├── Update Vercel environment variables
├── Redeploy frontend
└── Test connection

✅ LIVE!
```

---

## 🔄 Data Flow

### User Interaction Flow
```
1. User opens frontend
   https://xxx.vercel.app
                │
                ▼
2. React renders UI
                │
                ▼
3. User searches for stock
   "AAPL"
                │
                ▼
4. Frontend makes API call
   GET https://xxx.railway.app/api/search?query=AAPL
                │
                ▼
5. Backend processes request
   - Fetch from yfinance
   - Format data
   - Return JSON
                │
                ▼
6. Frontend receives data
   - Update state
   - Render components
                │
                ▼
7. User sees stock data
   Charts, metrics, info
```

---

## 📱 Frontend Deployment (Vercel)

### Build Process
```
Your Code (GitHub)
        │
        ▼
Vercel Auto-Detects
        │
        ▼
Run: npm install --legacy-peer-deps
        │
        ▼
Run: npm run build
        │
        ▼
Output: dist/ folder
        │
        ▼
Deploy to CDN
        │
        ▼
Global Distribution
        │
        ▼
User gets fast load
```

### What Vercel Handles
- ✅ GitHub integration
- ✅ Auto-builds on push
- ✅ Global CDN (super fast)
- ✅ Free SSL/HTTPS
- ✅ Automatic scaling
- ✅ Rollback if needed

---

## ⚙️ Backend Deployment (Railway)

### Build Process
```
Your Code (GitHub)
        │
        ▼
Railway Auto-Detects Python
        │
        ▼
Run: pip install -r requirements.txt
        │
        ▼
Run: uvicorn main:app --host 0.0.0.0 --port $PORT
        │
        ▼
Server Starts
        │
        ▼
Expose on Public URL
        │
        ▼
Users can call API
```

### What Railway Handles
- ✅ GitHub integration
- ✅ Auto-builds on push
- ✅ Python/Node environment
- ✅ Public URL assignment
- ✅ Environment variables
- ✅ Logging & monitoring

---

## 🔐 Security & Environment Variables

### Frontend (Vercel)
```
Environment Variables:
├── VITE_API_URL
│   └── https://your-backend.railway.app
│
Available during build:
├── import.meta.env.VITE_API_URL
└── Used in api.js for all API calls
```

### Backend (Railway)
```
Environment Variables:
├── PYTHONUNBUFFERED=1
├── PORT=8000
├── DATABASE_URL (if using DB)
├── API_KEY (if needed)
└── etc.

Available in code:
├── import os
└── api_key = os.getenv('API_KEY')
```

---

## ✅ Post-Deployment Verification

### Checklist
```
FRONTEND (Vercel)
[ ] Website loads without error
[ ] No blank page
[ ] Sidebar visible
[ ] Navigation works
[ ] No 404 errors
[ ] Mobile responsive
[ ] Open DevTools (F12)
    [ ] No console errors
    [ ] No network failures

BACKEND (Railway)  
[ ] API docs accessible
    https://your-backend.railway.app/docs
[ ] Health check passes
    GET /
[ ] Stock search works
    GET /api/search?query=AAPL
[ ] Check logs for errors
    Railway Dashboard > Logs tab

INTEGRATION
[ ] Frontend makes API calls
    DevTools > Network tab > try search
[ ] Data loads correctly
    Should see stock data
[ ] No CORS errors
    Red error about Access-Control-Allow-Origin
```

---

## 📊 Monitoring After Deployment

### Vercel Metrics
```
Dashboard shows:
├── Build status
├── Deployment history
├── Performance metrics
├── Edge function stats
└── Analytics
```

### Railway Monitoring
```
Dashboard shows:
├── Deployment logs
├── Container status
├── CPU/Memory usage
├── Network I/O
└── Error logs
```

### What to Watch
1. **First 24 hours**
   - Check logs for errors
   - Monitor API response times
   - Look for crash loops

2. **First week**
   - User feedback
   - Error patterns
   - Performance trends

3. **Ongoing**
   - Monthly cost review
   - Security updates
   - Dependency updates

---

## 🆘 If Deployment Fails

### Troubleshooting Flowchart
```
Deployment Failed?
        │
        ▼
Check Logs
        │
        ├─→ Build Error?
        │   └─→ npm install or python issues
        │       └─→ Check requirements.txt
        │
        ├─→ Runtime Error?
        │   └─→ App crashes on start
        │       └─→ Check main.py or start command
        │
        └─→ Connection Error?
            └─→ Can't reach GitHub
                └─→ Check token/permissions

Fix the issue → Commit → Push → Auto-redeploy
```

---

## 🔄 CI/CD Pipeline (Automatic)

### What Happens Automatically
```
You commit code locally
        │
        ▼
git push origin main
        │
        ▼
GitHub receives update
        │
        ▼
Webhook triggers Vercel/Railway
        │
        ├─→ [Vercel Frontend]
        │   ├── npm install
        │   ├── npm run build
        │   ├── Deploy to CDN
        │   └── Update URL
        │
        └─→ [Railway Backend]
            ├── pip install
            ├── Start uvicorn
            ├── Run on new port
            └── Update URL

Both live in ~5-10 minutes!
```

---

## 📞 Getting Help

### If Something Goes Wrong

1. **Check Logs First**
   - Vercel: Deployments → Click build → View logs
   - Railway: Project → View logs

2. **Common Solutions**
   - Frontend won't load → Hard refresh (Ctrl+Shift+R)
   - API error → Update VITE_API_URL
   - CORS error → Update backend main.py
   - 502 error → Restart Railway service

3. **Documentation**
   - DEPLOYMENT_GUIDE.md → Full details
   - DEPLOY_QUICK_START.md → Quick reference
   - Vercel/Railway docs → Platform-specific help

---

## 🎯 Success Criteria

You're done when:
- ✅ Frontend URL loads without errors
- ✅ Backend API docs show at `/docs`
- ✅ Frontend can search for stocks
- ✅ Data appears on screen
- ✅ No console errors or warnings
- ✅ Mobile view works
- ✅ All pages accessible

---

## 🚀 Next: Actually Deploy!

See `DEPLOY_QUICK_START.md` for 15-minute deployment guide.
