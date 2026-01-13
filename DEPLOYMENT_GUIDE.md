# StockSense Deployment Guide

## Deployment Options for Streamlit Apps (FREE)

### 1. **Streamlit Cloud** (RECOMMENDED - Easiest)
- **Cost**: Free tier available
- **Deployment Time**: < 2 minutes
- **Pros**: Automatic deployment from GitHub, free SSL, custom domain support
- **URL**: https://share.streamlit.io/

### 2. **Heroku** (Free tier limited)
- **Cost**: Free tier ending (was free, now requires paid plan)
- **Alternative**: Use alternative free platforms

### 3. **Railway** (New option - Free tier)
- **Cost**: Free starter tier
- **Deployment Time**: 5-10 minutes
- **URL**: https://railway.app

### 4. **Render** (Free tier)
- **Cost**: Free tier available
- **Deployment Time**: 10-15 minutes
- **URL**: https://render.com

### 5. **Hugging Face Spaces**
- **Cost**: Completely free
- **Deployment Time**: 5 minutes
- **URL**: https://huggingface.co/spaces

---

## STEP-BY-STEP DEPLOYMENT PROCESS

### PHASE 1: GitHub Setup (Required for all options)

#### Step 1: Initialize Git Repository
```bash
cd e:\Coding\stocksense\StockSense
git init
```

#### Step 2: Add Your Files
```bash
git add .
git commit -m "Initial commit: StockSense application"
```

#### Step 3: Create Main Branch
```bash
git branch -M main
```

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

