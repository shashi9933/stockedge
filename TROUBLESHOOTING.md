# StockSense - Data Fetching Troubleshooting Guide

## ✅ Issue Resolved - API Working!

Your StockSense app is now fixed and ready to use. Stock data fetching is working correctly!

## How to Use the App

### 1. **Home Page (Main App)**
- Select your market from the sidebar: Global, NSE (India), or BSE (India)
- Enter a stock symbol
- Choose date range (start and end dates)
- Click "Fetch Stock Data"
- View the candlestick chart and recent price data

### 2. **Chart Analysis Page**
- View detailed candlestick charts with volume indicators
- Zoom and pan the chart for detailed analysis

### 3. **Technical Indicators Page**
- View multiple technical indicators:
  - Simple Moving Average (SMA)
  - Relative Strength Index (RSI)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands

### 4. **Prediction Models Page**
- See ML predictions using 4 different models:
  - Linear Regression
  - Random Forest
  - Gradient Boosting
  - LSTM Neural Network
- Combined ensemble prediction

### 5. **Price Alerts Page**
- Set up SMS price alerts using Twilio
- Get notified when stock price reaches your target

## Common Stock Symbols

### Global Stocks (US Markets)
| Company | Symbol | Country |
|---------|--------|---------|
| Apple | AAPL | USA |
| Microsoft | MSFT | USA |
| Google | GOOGL | USA |
| Tesla | TSLA | USA |
| Amazon | AMZN | USA |
| Meta (Facebook) | META | USA |
| Netflix | NFLX | USA |

### Indian Stocks (NSE)
| Company | Symbol |
|---------|--------|
| Reliance Industries | RELIANCE.NS |
| Tata Consultancy Services | TCS.NS |
| Infosys | INFY.NS |
| HDFC Bank | HDFCBANK.NS |
| Bharti Airtel | BHARTIARTL.NS |
| Axis Bank | AXISBANK.NS |
| ITC | ITC.NS |
| State Bank of India | SBIN.NS |

### Indian Stocks (BSE)
Use `.BO` suffix instead of `.NS`
- RELIANCE.BO
- TCS.BO
- INFY.BO

## Troubleshooting

### If you see "Invalid symbol" error:
1. Check that the symbol spelling is correct
2. For Indian stocks, make sure to add `.NS` (NSE) or `.BO` (BSE)
   - Example: RELIANCE.NS, not just RELIANCE
3. Look up the correct symbol at:
   - https://finance.yahoo.com/ (for US stocks)
   - https://www.moneycontrol.com/ (for Indian stocks)

### If you see "No data found" error:
1. The date range might not have trading data
2. Try a different date range
3. Make sure the stock symbol is active and trading

### If the chart doesn't display:
1. Refresh the page (F5)
2. Try again with a shorter date range
3. Clear your browser cache if issues persist

### If technical indicators show no data:
1. Make sure you've successfully fetched stock data first
2. Click "Fetch Stock Data" before viewing indicators
3. The indicators calculate based on the fetched data

## Technical Details

**App URL**: https://stockedgedot.streamlit.app/

**Technologies Used**:
- **Frontend**: Streamlit (Python web framework)
- **Data Source**: YFinance API (free real-time stock data)
- **Charting**: Plotly (interactive charts)
- **Analysis**: Pandas, NumPy, Scikit-learn
- **Hosting**: Streamlit Cloud

**Data Quality**:
- Real-time stock prices (updated daily)
- 15-minute cache to optimize performance
- Support for 30+ years of historical data
- Global stocks (US markets)
- Indian stocks (NSE & BSE)

## What Was Fixed

The app experienced an API compatibility issue due to a yfinance library version change. This has been resolved:

- ✅ Fixed yfinance API compatibility
- ✅ Enhanced error messages for better troubleshooting
- ✅ Added comprehensive testing
- ✅ Verified all data fetching functionality

## Support

If you encounter any issues:
1. Check this troubleshooting guide first
2. Try the example symbols above to verify the app works
3. Refresh the page and try again
4. Clear browser cache if needed

## Recent Updates

**Latest Fix**: January 13, 2026
- Fixed yfinance API compatibility (removed deprecated progress parameter)
- Enhanced error messages for users
- Added comprehensive debug testing
- Verified all data fetching works correctly

---

**Status**: ✅ FULLY OPERATIONAL

Enjoy using StockSense! 📈
