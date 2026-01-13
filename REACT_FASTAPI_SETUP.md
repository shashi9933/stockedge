# 🚀 React + FastAPI Architecture Setup Guide

Complete guide to running StockSense with React frontend and FastAPI backend.

## 📁 Architecture Overview

```
StockSense/
├── backend/                  # FastAPI server (port 8000)
│   ├── main.py              # API endpoints
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/                 # React UI (port 5173)
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API calls
│   │   └── App.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── utils/                    # Shared Python utilities
│   ├── data_fetcher.py
│   ├── technical_indicators.py
│   ├── prediction_models.py
│   └── ...
│
└── (existing files)
```

## 🎯 Quick Start (5 minutes)

### Step 1: Setup Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
copy .env.example .env

# Run the server
python main.py
```

✅ Backend running at: `http://localhost:8000`
✅ Docs available at: `http://localhost:8000/docs`

### Step 2: Setup Frontend (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

✅ Frontend running at: `http://localhost:5173`

### Step 3: Open in Browser

Visit: **http://localhost:5173**

You should see:
- 🎨 Modern dark-theme dashboard
- 📊 Sidebar navigation (8 pages)
- 🔍 Stock search bar
- 📱 Responsive design

---

## 🔧 Detailed Setup Instructions

### Backend Setup

#### 1. **Python Environment**
```bash
cd backend

# Create virtual environment (recommended)
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

#### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

Dependencies include:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pandas` - Data processing
- `yfinance` - Stock data
- `ta` - Technical indicators
- `scikit-learn` - ML models

#### 3. **Configure Environment**
```bash
# Copy example
copy .env.example .env

# Edit .env with your settings
# Add your Alpha Vantage API key if desired
ALPHA_VANTAGE_API_KEY=your_key_here
```

#### 4. **Run Backend**
```bash
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 5. **Test API**
```bash
# Test health check
curl http://localhost:8000/

# Test stock data
curl "http://localhost:8000/api/stock/AAPL?market=US&days=30"

# View interactive docs
# Open: http://localhost:8000/docs
```

### Frontend Setup

#### 1. **Install Node.js** (if not installed)
- Download from https://nodejs.org (LTS version recommended)
- Verify: `node --version` and `npm --version`

#### 2. **Install Dependencies**
```bash
cd frontend
npm install
```

This installs:
- `react` - UI framework
- `vite` - Build tool
- `tailwindcss` - Styling
- `lucide-react` - Icons
- `axios` - HTTP client

#### 3. **Configure API URL** (optional)
If backend is on different machine:

Create `.env` file in `frontend/`:
```env
REACT_APP_API_URL=http://your-server.com:8000
```

#### 4. **Run Frontend**
```bash
npm run dev
```

Expected output:
```
  VITE v... dev server running at:
  ➜  Local:   http://localhost:5173/
```

#### 5. **Build for Production**
```bash
npm run build
```

Creates optimized `dist/` folder for deployment.

---

## 🌐 API Endpoints

All endpoints return JSON responses.

### Stock Data
```
GET /api/stock/{symbol}
Parameters:
  - market: "US" | "NSE" | "BSE"
  - days: number (default: 365)

Example:
GET http://localhost:8000/api/stock/AAPL?market=US&days=180
```

### Technical Indicators
```
GET /api/indicators/{symbol}
Parameters:
  - market: "US" | "NSE" | "BSE"
  - days: number

Example:
GET http://localhost:8000/api/indicators/AAPL
```

### Predictions
```
GET /api/predict/{symbol}
Parameters:
  - market: "US" | "NSE" | "BSE"
  - days: number (prediction horizon)

Example:
GET http://localhost:8000/api/predict/AAPL?days=30
```

### Popular Stocks
```
GET /api/popular-stocks

Returns list of popular global and Indian stocks.
```

### Market Overview
```
GET /api/market-overview

Returns current market indices and statistics.
```

### Search
```
GET /api/search?query=apple

Returns matching stocks.
```

---

## 🔌 Frontend-Backend Communication

### How Data Flows

```
User Types "AAPL" in Search
    ↓
Frontend: /src/services/api.js
    ↓
axios GET http://localhost:8000/api/stock/AAPL
    ↓
Backend FastAPI /api/stock/{symbol}
    ↓
Python: utils/data_fetcher.py → yfinance
    ↓
Data returned as JSON
    ↓
React Component displays in UI
```

### Example: Get Stock Data

**Frontend (React):**
```javascript
import { getStockData } from "../services/api";

// In component:
const data = await getStockData("AAPL", "US", 365);
console.log(data);
```

**Backend (FastAPI):**
```python
@app.get("/api/stock/{symbol}")
def get_stock(symbol: str, market: str = "US", days: int = 365):
    # Fetches from yfinance
    # Processes with pandas
    # Returns JSON
```

---

## 🚀 Deployment

### Deploy Backend to Railway.app (Recommended)

1. **Prepare Repository**
```bash
git add .
git commit -m "Add backend and frontend"
git push origin main
```

2. **Create Railway Project**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Select `backend` directory

3. **Set Environment Variables**
   - Add `ALPHA_VANTAGE_API_KEY` in Railway dashboard
   - Set `PORT=8000`

4. **Deploy**
   - Railway automatically deploys on push
   - Get your API URL: `https://your-project.railway.app`

### Deploy Frontend to Vercel (Recommended)

1. **Build Frontend**
```bash
cd frontend
npm run build
```

2. **Deploy to Vercel**
```bash
npm i -g vercel
vercel deploy --prod
```

3. **Configure Environment**
   - In Vercel dashboard: Settings → Environment Variables
   - Add: `REACT_APP_API_URL=https://your-backend.railway.app`

4. **Redeploy**
```bash
vercel deploy --prod
```

### Your URLs
- **Frontend**: https://stocksense.vercel.app
- **Backend**: https://stocksense-api.railway.app
- **API Docs**: https://stocksense-api.railway.app/docs

---

## 🐛 Troubleshooting

### "Connection refused" error
**Problem**: Frontend can't reach backend
**Solution**:
```bash
# Check backend is running
curl http://localhost:8000

# Check API URL in frontend .env
cat frontend/.env

# Make sure ports are correct (8000 for backend, 5173 for frontend)
```

### CORS errors in console
**Problem**: "Access to XMLHttpRequest blocked by CORS"
**Solution**:
1. Check backend is running
2. Verify CORS origins in `backend/main.py`:
```python
# Should include your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
)
```
3. Restart backend

### Module not found errors
**Backend**:
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

**Frontend**:
```bash
# Reinstall dependencies
cd frontend
npm install

# Clear cache
rm -rf node_modules package-lock.json
npm install
```

### Port already in use
**For Backend** (change port):
```bash
python main.py
# Modify in main.py: uvicorn.run(..., port=8001)
```

**For Frontend**:
```bash
npm run dev -- --port 3000
```

### API responding but no data
**Problem**: Stock data not loading
**Solution**:
1. Check internet connection
2. Verify stock symbol is correct (AAPL, RELIANCE.NS, etc.)
3. Check yfinance isn't rate-limited
4. View backend logs for errors

---

## 📊 Project Structure Details

### Backend Files

**main.py** - API endpoints:
- `GET /` - Health check
- `GET /api/stock/{symbol}` - Stock data
- `GET /api/indicators/{symbol}` - Technical indicators
- `GET /api/predict/{symbol}` - Price predictions
- `GET /api/market-overview` - Market data
- `GET /api/popular-stocks` - Popular stocks list
- `GET /api/search` - Search stocks

**requirements.txt** - Python dependencies

**.env.example** - Environment variable template

### Frontend Files

**src/components/**:
- `Sidebar.jsx` - Navigation & stock search
- `Topbar.jsx` - Search bar & notifications
- `Card.jsx` - Reusable card component
- `MetricCard.jsx` - Metric display

**src/pages/**:
- `Dashboard.jsx` - Home page
- `ChartAnalysis.jsx` - Charts page
- `TechnicalIndicators.jsx` - Indicators page
- (More pages: Alerts, Financials, Company, Shareholding, Peers)

**src/services/**:
- `api.js` - All API calls

**src/App.jsx** - Main app component with routing

---

## 🎯 Next Steps After Setup

### 1. **Add More Pages**
Create new page components in `frontend/src/pages/` for:
- Price Alerts
- Financial Metrics
- Company Information
- Shareholding Analysis
- Peer Comparison

### 2. **Add Charting Library**
```bash
npm install recharts
# or
npm install chart.js react-chartjs-2
```

Then integrate into `ChartAnalysis.jsx`

### 3. **Add Real-time Data**
```bash
# Install WebSocket library
npm install socket.io-client
```

Update `api.js` to use WebSockets for live prices

### 4. **Add Authentication**
```bash
npm install @auth0/auth0-react
# or implement JWT-based auth
```

### 5. **Add Database**
In backend:
```bash
pip install sqlalchemy
# Create models for users, watchlists, alerts
```

---

## 📞 Support

- 📖 **Frontend Docs**: See `frontend/README.md`
- 🔧 **Backend Docs**: See `backend/README.md`
- 🐛 **Issues**: Check terminal logs
- 💬 **Help**: Review troubleshooting section

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend running: `curl http://localhost:8000/`
- [ ] API docs: Open `http://localhost:8000/docs`
- [ ] Frontend running: Open `http://localhost:5173`
- [ ] Can search stocks: Type "AAPL" in search
- [ ] Can view dashboard: See popular stocks & market overview
- [ ] Can fetch data: Click "Fetch Data" button
- [ ] Charts loading: Navigate to Chart Analysis page
- [ ] No console errors: Check browser dev tools (F12)

---

## 🎉 You're Ready!

Your complete React + FastAPI stock analysis platform is now running!

```
Frontend: http://localhost:5173 ✅
Backend:  http://localhost:8000 ✅
API Docs: http://localhost:8000/docs ✅
```

**Next**: Explore the dashboard, test stock searches, and start developing!

---

*Last updated: January 2026*
