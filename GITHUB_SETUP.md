# GitHub & Deployment Setup Guide

## Quick Start - Push to GitHub

### Step 1: Prepare Your Repository

Navigate to your project directory:
```bash
cd e:\Coding\stocksense\StockSense
```

### Step 2: Initialize Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git init
```

### Step 3: Add Files to Staging

```bash
git add .
```

### Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: StockSense - Stock Market Analysis Platform"
```

### Step 5: Set Main Branch

```bash
git branch -M main
```

### Step 6: Connect to Remote Repository

```bash
git remote add origin https://github.com/shashi9933/stockedge.git
```

### Step 7: Push to GitHub

```bash
git push -u origin main
```

---

## If You Get Authentication Error

### For HTTPS (Token Method - Recommended)

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (ensure `repo` scope is selected)
3. Copy the token
4. When prompted for password in git, paste the token instead

### For SSH (More Secure)

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to GitHub
# https://github.com/settings/keys
```

Then use SSH URL:
```bash
git remote add origin git@github.com:shashi9933/stockedge.git
```

---

## Verify Your GitHub Repository

After pushing, verify:
1. Go to https://github.com/shashi9933/stockedge
2. You should see:
   - ✓ `app.py`
   - ✓ `pages/` folder with 4 analysis pages
   - ✓ `utils/` folder with all utilities
   - ✓ `requirements.txt`
   - ✓ `.gitignore`
   - ✓ `README.md`

---

## Create Compelling README.md

Replace your `README.md` with this:

```markdown
# StockSense - Stock Market Analysis Platform

A sophisticated stock market analysis platform that combines advanced data analysis techniques, multiple prediction models, and interactive visualization to provide comprehensive financial insights for both Indian and global markets.

## Features

### 📊 Data Retrieval & Processing
- **Real-time & Historical Data**: Yahoo Finance integration for global and Indian markets
- **Smart Caching**: 15-minute cache to reduce API calls while maintaining data freshness
- **Rate Limit Handling**: Multiple fallback mechanisms and randomized delays
- **Multi-Market Support**: NSE, BSE, and global markets (AAPL, RELIANCE.NS, etc.)

### 📈 Technical Analysis
- **Moving Averages**: SMA, EMA with crossover signals
- **Relative Strength Index (RSI)**: Momentum analysis
- **Bollinger Bands**: Volatility measurement
- **MACD**: Trend confirmation
- **Support & Resistance**: Automatic key level identification

### 🔮 AI-Powered Predictions
- **Multiple Models**: Linear, Quadratic, Fourier, ARIMA, Statistical Time Series
- **Ensemble Approach**: Weighted predictions based on historical accuracy
- **Market Regime Detection**: Adaptive models for trending/ranging markets
- **Confidence Metrics**: Reliability scores for all predictions

### 🔔 Price Alert System
- **SMS Notifications**: Twilio integration for mobile alerts
- **Customizable Triggers**: Above/below price targets
- **Real-time Monitoring**: Active alert tracking

### 📱 Interactive Visualization
- **Professional Charts**: Candlestick, OHLC, Line charts
- **Interactive Elements**: Zoom, pan, range selectors
- **Multi-page Dashboard**: Organized analysis sections
- **Real-time Updates**: Live price metrics

## Installation

### Requirements
- Python 3.11+
- pip or conda

### Local Setup

```bash
# Clone repository
git clone https://github.com/shashi9933/stockedge.git
cd stockedge

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

The app will open at: `http://localhost:8501`

## Usage

### Basic Workflow
1. **Select Market**: Choose Global, NSE, or BSE
2. **Enter Stock Symbol**: E.g., `AAPL`, `RELIANCE.NS`, `INFY.NS`
3. **Choose Date Range**: Select historical period for analysis
4. **Fetch Data**: Click to load stock data
5. **Explore Pages**:
   - **Chart Analysis**: View candlestick charts with volume
   - **Technical Indicators**: RSI, MACD, Bollinger Bands
   - **Prediction Models**: AI-based price predictions
   - **Price Alerts**: Set custom price alerts

### Example Stock Symbols
- **Global**: AAPL, GOOGL, MSFT, TSLA, AMZN
- **NSE (India)**: RELIANCE.NS, INFY.NS, TCS.NS, ICICIBANK.NS
- **BSE (India)**: RELIANCE.BO, INFY.BO, TCS.BO

## Architecture

```
stockedge/
├── app.py                 # Main Streamlit app
├── pages/
│   ├── 1_Chart_Analysis.py
│   ├── 2_Technical_Indicators.py
│   ├── 3_Prediction_Models.py
│   └── 4_Price_Alerts.py
├── utils/
│   ├── data_fetcher.py          # Yahoo Finance API
│   ├── technical_indicators.py  # TA calculations
│   ├── prediction_models.py     # ML models
│   ├── chart_helpers.py         # Plotly visualization
│   ├── price_alerts.py          # Alert system
│   └── market_regime.py         # Regime detection
└── requirements.txt
```

## Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [https://share.streamlit.io/](https://share.streamlit.io/)
3. Connect your GitHub account
4. Select this repository and `app.py`
5. Deploy!

**Live App**: [Your deployed URL will appear here]

### Other Options
- **Railway**: https://railway.app
- **Render**: https://render.com
- **Hugging Face Spaces**: https://huggingface.co/spaces

## Technologies Used

- **Frontend**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly
- **Machine Learning**: Scikit-learn, SciPy, Statsmodels
- **Data Source**: YFinance
- **Notifications**: Twilio

## API Integrations

- **Yahoo Finance**: Stock price data
- **Twilio**: SMS alerts (optional)

## Performance

- **Initial Load**: ~2-5 seconds
- **Data Fetch**: ~1-3 seconds per stock
- **Chart Rendering**: ~500ms
- **Caching**: 15-minute TTL on data

## Known Limitations

- RSI may produce NaN for stocks with no losses
- Alerts require manual checking (no background monitoring)
- SMS requires Twilio account
- Free tier limited to 1GB RAM

## Future Enhancements

- [ ] Database persistence for alerts
- [ ] User authentication system
- [ ] Real-time WebSocket updates
- [ ] Machine learning backtesting
- [ ] Advanced portfolio analysis
- [ ] Multiple timeframe analysis
- [ ] Custom indicator creation

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and create a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Check documentation in `DEPLOYMENT_GUIDE.md`
- See `BUG_REPORT.md` for known issues

## Disclaimer

This application is for educational and analysis purposes only. It is not financial advice. Always conduct your own research before making investment decisions.

---

**Built with ❤️ for traders and investors**
```

---

## Next Steps After GitHub Push

1. ✅ Code is backed up on GitHub
2. ✅ Ready for deployment to Streamlit Cloud
3. ✅ Can be shared with others via GitHub link
4. ✅ Version control is active

## Deployment Commands

After pushing to GitHub, deploy with:

**Option A: Streamlit Cloud (RECOMMENDED)**
```
1. Visit https://share.streamlit.io/
2. Click "New app"
3. Select: shashi9933/stockedge
4. Select Branch: main
5. Select File: app.py
6. Click Deploy
```

**Option B: One-line deployment**
```bash
streamlit run app.py --logger.level=debug
```

