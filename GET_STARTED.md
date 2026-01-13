# 🚀 Quick Start - React + FastAPI

Get StockSense running in 2 minutes!

## Step 1: Start Backend (Terminal 1)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **API ready at**: http://localhost:8000/docs

---

## Step 2: Start Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

**Output:**
```
VITE ... dev server running at:
➜  Local:   http://localhost:5173/
```

✅ **App ready at**: http://localhost:5173

---

## 🎉 Done!

Your professional stock analysis platform is now running!

### What You Get

✅ **Modern Dark Theme** - Professional fintech UI
✅ **Sidebar Navigation** - 8 analysis pages
✅ **Stock Search** - Real-time search & autocomplete
✅ **API Integration** - FastAPI backend with 6 endpoints
✅ **Popular Stocks** - Quick access grid
✅ **Market Overview** - Key indices
✅ **Responsive Design** - Mobile, tablet, desktop

### Test It

1. Open http://localhost:5173
2. Search for "AAPL" or "RELIANCE.NS"
3. Click "Fetch Data"
4. Explore the dashboard

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Make sure both terminal 1 & 2 are running |
| CORS error | Restart backend server |
| Port in use | Change port in config file |
| API not responding | Check backend logs for errors |

### Full Setup Guide

See [REACT_FASTAPI_SETUP.md](./REACT_FASTAPI_SETUP.md) for detailed instructions.

### Project Structure

```
frontend/          ← React UI (port 5173)
backend/           ← FastAPI server (port 8000)
utils/             ← Shared Python code
```

### Next Steps

- [ ] Explore all 8 pages
- [ ] Test stock search
- [ ] Check API docs at /docs
- [ ] Add your API keys to .env
- [ ] Deploy to production

---

**Happy Analyzing!** 📊
