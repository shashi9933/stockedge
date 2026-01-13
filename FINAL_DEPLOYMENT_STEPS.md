# FINAL DEPLOYMENT STEPS

## Step 1: Push to GitHub

Run these commands in PowerShell:

```powershell
cd e:\Coding\stocksense\StockSense

# Add GitHub remote
git remote add origin https://github.com/shashi9933/stockedge.git

# Push to GitHub
git push -u origin main
```

## Step 2: Enter GitHub Credentials

When prompted, choose one of:

### Option A: Personal Access Token (RECOMMENDED)
1. Go to: https://github.com/settings/tokens/new
2. Select scopes:
   - ✓ repo (full control of private repositories)
   - ✓ workflow (if using GitHub Actions)
3. Generate and copy the token
4. When Git asks for password → paste the token

### Option B: Browser Sign-in
- Git will open your browser
- Sign in to GitHub
- Authorize the request
- Come back to terminal

---

## Step 3: Verify on GitHub

After successful push:
1. Open: https://github.com/shashi9933/stockedge
2. You should see:
   - ✓ All files uploaded
   - ✓ Latest commit visible
   - ✓ `main` branch selected

---

## Step 4: Deploy to Streamlit Cloud (EASIEST & FREE!)

### Option A: Automatic Deployment
1. Visit: https://share.streamlit.io/
2. Click: "New app"
3. Select:
   - **GitHub account**: shashi9933
   - **Repository**: stockedge
   - **Branch**: main
   - **Main file path**: app.py
4. Click: "Deploy"
5. Wait 2-5 minutes
6. Your app is LIVE!

### Option B: If Above Doesn't Work

**Alternative Platforms** (Still FREE):

#### Render
```
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repo
4. Build command: pip install -r requirements.txt
5. Start command: streamlit run app.py
6. Deploy
```

#### Railway
```
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Choose this repository
5. Auto-configures from Procfile
6. Deploy
```

#### Hugging Face Spaces
```
1. Go to https://huggingface.co/spaces
2. Create Space
3. Choose Docker template
4. Upload Dockerfile
5. Platform auto-deploys
```

---

## Commands to Run NOW

### CRITICAL: First Time Setup
```powershell
cd e:\Coding\stocksense\StockSense

# Configure git (if not done)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add remote repository
git remote add origin https://github.com/shashi9933/stockedge.git

# Verify remote was added
git remote -v

# Push to GitHub
git push -u origin main
```

### After Each Local Change
```powershell
cd e:\Coding\stocksense\StockSense

git add .
git commit -m "Description of changes"
git push origin main
```

---

## Deployment Timeline

| Step | Time | Action |
|------|------|--------|
| 1 | 1 min | Push code to GitHub |
| 2 | 2-5 min | Streamlit Cloud auto-deploys |
| 3 | 1 min | Configure app settings |
| **TOTAL** | **~10 min** | **App is LIVE!** |

---

## What Gets Deployed?

✅ `app.py` - Main application  
✅ `pages/` - All 4 analysis pages  
✅ `utils/` - All utility modules  
✅ `requirements.txt` - All dependencies  
✅ `.streamlit/config.toml` - App configuration  

❌ `.gitignore` - Ignored files  
❌ `.venv/` - Local environment (doesn't deploy)  
❌ `__pycache__/` - Python cache files  

---

## Monitor Your Deployment

### Streamlit Cloud Dashboard
- URL: https://share.streamlit.io/
- See: Run logs, resource usage, custom domain

### Check Logs
```
Click on your deployed app
→ Settings ⚙️
→ Logs
→ View recent activity
```

### Share Your App
```
URL: https://your-app-name.streamlit.app
Share with: https://share.streamlit.io/shashi9933/stockedge/main/app.py
```

---

## COMMON ISSUES & FIXES

### ❌ "Permission denied (publickey)"
**Fix**: Use HTTPS instead of SSH
```powershell
git remote set-url origin https://github.com/shashi9933/stockedge.git
git push -u origin main
```

### ❌ "fatal: 'origin' does not appear to be a git repository"
**Fix**: Add remote first
```powershell
git remote add origin https://github.com/shashi9933/stockedge.git
```

### ❌ "ImportError: No module named 'xyz'"
**Fix**: Add to requirements.txt, then:
```powershell
git add requirements.txt
git commit -m "Add missing dependency"
git push origin main
# Streamlit auto-redeploys!
```

### ❌ App deploys but shows blank page
**Fix**: 
1. Check `.streamlit/config.toml` exists
2. Verify `app.py` in root directory
3. Check logs for errors

---

## NEXT STEPS

1. ✅ **Run the git push commands** (see above)
2. ✅ **Connect to Streamlit Cloud**
3. ✅ **Get your public URL**
4. ✅ **Share with users/investors**
5. ✅ **Monitor performance**

## YOU'RE READY!

Your StockSense app is production-ready. Just follow the steps above and it will be live in 10 minutes!

