# Alpha Vantage API Setup Guide

## Quick Start (5 minutes)

### Step 1: Get Your Free API Key
1. Visit https://www.alphavantage.co/
2. Click **"Get Free API Key"** in the top right
3. Enter your email and name
4. You'll receive an API key instantly (check your inbox if not visible immediately)

### Step 2: Configure Your Environment
1. Open the `.env` file in your project root (create if it doesn't exist):
   ```bash
   ALPHA_VANTAGE_API_KEY=your_api_key_here
   ```
2. Replace `your_api_key_here` with the key you received
3. Save the file

### Step 3: Verify It Works
Run this test in your terminal:
```bash
python test_alpha_vantage.py
```

You should see stock data from Apple (AAPL) if everything works correctly.

---

## API Key Limits & Usage

| Limit | Free Tier |
|-------|-----------|
| **Calls per Minute** | 5 |
| **Calls per Day** | 500 |
| **Data Points** | Last 100 for daily, full history for premium |
| **Latency** | 1 second between calls recommended |

### Best Practices

✅ **DO:**
- Use caching to minimize API calls
- Space API calls 1+ seconds apart
- Cache results for 1 hour
- Reuse data when possible

❌ **DON'T:**
- Make rapid successive calls
- Query the same stock repeatedly in short time
- Query more than 5 stocks per minute
- Leave your API key in public repos

---

## What's Included in Your App

### Available Endpoints

**Stock Price Data:**
- TIME_SERIES_DAILY - Daily OHLCV data (20+ years)
- TIME_SERIES_WEEKLY - Weekly data
- TIME_SERIES_MONTHLY - Monthly data
- GLOBAL_QUOTE - Real-time quote

**Fundamental Data:**
- OVERVIEW - Company info & financial ratios
- INCOME_STATEMENT - P&L statements (annual & quarterly)
- BALANCE_SHEET - Balance sheets
- CASH_FLOW - Cash flow statements
- EARNINGS - Historical earnings & estimates

**Technical Indicators:**
- SMA - Simple Moving Average
- EMA - Exponential Moving Average
- RSI - Relative Strength Index
- MACD - Moving Average Convergence Divergence
- BBANDS - Bollinger Bands
- And 50+ more indicators

---

## Troubleshooting

**Problem:** "API key not configured"
- **Solution:** Make sure `.env` file exists with `ALPHA_VANTAGE_API_KEY=your_key`
- Check there are no spaces around `=`

**Problem:** "Invalid API key"
- **Solution:** Check you copied the full key (usually 20+ characters)
- Go to alphavantage.co and verify the key in your account

**Problem:** "Rate limit exceeded"
- **Solution:** You've hit the 5 calls/minute limit
- The app automatically waits and retries
- Upgrade to premium if you need more calls

**Problem:** "No data returned"
- **Solution:** Symbol may be invalid
- Try using US-traded tickers like AAPL, MSFT, GOOGL
- Indian stocks like RELIANCE.BSE also work

---

## Using Financial Statements in Your App

The Financial Metrics page now includes:

### Income Statement
Shows revenue, operating income, net income for:
- Last 4 fiscal years (annual)
- Last 8 quarters (quarterly)
- Trend analysis

### Balance Sheet
Shows assets, liabilities, equity:
- Fiscal year comparison
- Quarterly snapshots

### Cash Flow
Shows operating, investing, financing cash flows:
- Year-over-year trends

---

## Next Steps

1. Set up your `.env` file with your API key
2. Visit the app and test with a stock ticker
3. Check the "Financial Metrics" page for statements
4. Monitor your API usage (alphavantage.co dashboard)
5. Consider upgrading if you need more than 500 calls/day

---

## API Key Management

Never commit `.env` files to git. The app automatically:
- Loads from `.env` file (local)
- Loads from Streamlit Secrets (when deployed)
- Falls back to cached data if no key provided

## Questions?

- Alpha Vantage Support: https://www.alphavantage.co/support/
- Documentation: https://www.alphavantage.co/documentation/
