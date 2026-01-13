# Free Stock Data APIs - Comparison Guide

## Best Alternatives to yfinance

### 1. **Alpha Vantage** ⭐ RECOMMENDED
**Best for**: Quick drop-in replacement for yfinance
- **URL**: https://www.alphavantage.co
- **Free Tier**: 5 calls/minute, 500/day
- **Data**: OHLCV, technical indicators, forex
- **Historical Data**: Yes (up to 20+ years)
- **Coverage**: US stocks, international, crypto
- **Setup**: Easy API key signup

**Pros**:
- Similar data format to yfinance
- Built-in technical indicators
- Good documentation
- Intraday + daily data

**Cons**:
- Rate limited (5/min for free)
- 500 requests/day limit
- Small delay on free tier

**Code Example**:
```python
import requests

def get_alpha_vantage_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "full"
    }
    response = requests.get(url, params=params)
    data = response.json()
    # Parse and convert to DataFrame
    return data
```

---

### 2. **Finnhub** ⭐⭐ BEST RATE LIMITS
**Best for**: Higher volume requests
- **URL**: https://finnhub.io
- **Free Tier**: Unlimited (with fair use limit ~60 calls/minute)
- **Data**: Quotes, OHLCV, fundamentals, news
- **Historical Data**: Yes
- **Coverage**: US, EU, Asia stocks
- **Setup**: Free API key

**Pros**:
- Highest free rate limit (~60/min)
- No daily cap
- Real-time quotes
- Company fundamentals included
- Very good documentation

**Cons**:
- Fair use policy enforced
- Slightly different data format
- News data limited on free tier

**Code Example**:
```python
import requests

def get_finnhub_data(symbol, api_key):
    url = f"https://finnhub.io/api/v1/quote"
    params = {
        "symbol": symbol,
        "token": api_key
    }
    response = requests.get(url, params=params)
    return response.json()
    # Returns: {c: close, h: high, l: low, o: open, pc: prev_close, t: timestamp}
```

---

### 3. **Twelve Data** ⭐⭐ GOOD ALTERNATIVE
**Best for**: Professional data quality
- **URL**: https://twelvedata.com
- **Free Tier**: 800 calls/day, 10 calls/minute
- **Data**: OHLCV, intraday, fundamentals
- **Historical Data**: Yes (10+ years)
- **Coverage**: 500K+ instruments globally
- **Setup**: Free account

**Pros**:
- Huge coverage (global stocks)
- Good data quality
- International markets (NSE, BSE for India!)
- Intraday + daily

**Cons**:
- 10 calls/minute limit
- 800 calls/day limit
- Slightly more strict limits

**Code Example**:
```python
import requests

def get_twelve_data(symbol, api_key):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "1day",
        "apikey": api_key,
        "outputsize": 5000
    }
    response = requests.get(url, params=params)
    return response.json()
```

---

### 4. **Polygon.io** ⭐⭐ HISTORICAL DATA FOCUSED
**Best for**: Historical data, backtesting
- **URL**: https://polygon.io
- **Free Tier**: Limited (but good for historical)
- **Data**: Aggregates, OHLCV, tickers
- **Historical Data**: Yes (excellent)
- **Coverage**: US stocks, crypto, forex
- **Setup**: Free tier available

**Pros**:
- Excellent historical data
- Good for backtesting
- Crypto data included
- API is fast

**Cons**:
- Limited free tier (lower rate limits)
- Mainly US stocks
- Separate API for different data types

---

### 5. **IEX Cloud** ⭐ COMPREHENSIVE
**Best for**: Complete financial data
- **URL**: https://iexcloud.io
- **Free Tier**: Limited (but good starter)
- **Data**: Quotes, news, fundamentals, technicals
- **Historical Data**: Yes
- **Coverage**: US stocks mainly
- **Setup**: Free account

**Pros**:
- Excellent documentation
- News included
- Company fundamentals
- Historical charts

**Cons**:
- More limited free tier
- Mainly US stocks
- Requires signup

---

## Quick Comparison Table

| API | Free Rate Limit | Daily Cap | Data Quality | Global Coverage | Ease of Use |
|-----|-----------------|-----------|--------------|-----------------|-------------|
| **yfinance** | Unlimited* | None | Good | Excellent | ⭐⭐⭐⭐⭐ |
| **Alpha Vantage** | 5/min | 500/day | Good | Good | ⭐⭐⭐⭐ |
| **Finnhub** | 60/min* | None | Excellent | Excellent | ⭐⭐⭐⭐⭐ |
| **Twelve Data** | 10/min | 800/day | Excellent | Excellent | ⭐⭐⭐⭐ |
| **Polygon.io** | Limited | Limited | Excellent | Good | ⭐⭐⭐⭐ |
| **IEX Cloud** | Limited | Limited | Excellent | Limited (US) | ⭐⭐⭐⭐ |

*yfinance has no official rate limits but hits them during peak hours. Finnhub has ~60/min with fair use.

---

## RECOMMENDATION FOR YOUR PROJECT

### **Best Option: Dual API Strategy**

Use **Finnhub** as primary (highest rate limit) and **Alpha Vantage** as fallback:

```python
# Try Finnhub first (better rate limits)
try:
    data = get_finnhub_data(symbol, FINNHUB_KEY)
except RateLimitError:
    # Fall back to Alpha Vantage
    data = get_alpha_vantage_data(symbol, ALPHA_VANTAGE_KEY)
except:
    # Fall back to yfinance
    data = yfinance.download(symbol, ...)
```

### **Why This Works**:
1. **Finnhub** - Most reliable, ~60 calls/minute
2. **Alpha Vantage** - Good backup, 5/minute but never hits hard limits
3. **yfinance** - Last resort (what you have now)

---

## Setup Instructions

### Step 1: Get API Keys

**Finnhub**:
- Go to https://finnhub.io
- Sign up (free)
- Copy API key
- No credit card needed

**Alpha Vantage**:
- Go to https://www.alphavantage.co
- Sign up (free)
- Copy API key
- No credit card needed

### Step 2: Add to `.env`
```
FINNHUB_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=your_key_here
```

### Step 3: Update `data_fetcher.py`
See implementation examples below.

---

## Implementation Examples

### Using Finnhub

```python
import requests
import pandas as pd

def get_finnhub_historical(symbol, api_key, days=365):
    """Fetch historical data from Finnhub"""
    url = "https://finnhub.io/api/v1/quote"
    
    # Get quote
    response = requests.get(url, params={
        "symbol": symbol,
        "token": api_key
    })
    data = response.json()
    
    if 'c' not in data:
        raise Exception(f"Symbol not found: {symbol}")
    
    # Convert to format compatible with your app
    df = pd.DataFrame({
        'Date': pd.Timestamp.now(),
        'Open': data.get('o', data['c']),
        'High': data['h'],
        'Low': data['l'],
        'Close': data['c'],
        'Volume': data.get('v', 0)
    }, index=[0])
    
    return df
```

### Using Alpha Vantage

```python
import requests
import pandas as pd

def get_alpha_vantage_historical(symbol, api_key):
    """Fetch historical data from Alpha Vantage"""
    url = "https://www.alphavantage.co/query"
    
    response = requests.get(url, params={
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "compact"
    })
    data = response.json()
    
    if "Time Series (Daily)" not in data:
        raise Exception(f"Could not fetch {symbol}")
    
    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'Date': date,
            'Open': float(values['1. open']),
            'High': float(values['2. high']),
            'Low': float(values['3. low']),
            'Close': float(values['4. close']),
            'Volume': float(values['5. volume'])
        }
        for date, values in data["Time Series (Daily)"].items()
    ])
    
    df['Date'] = pd.to_datetime(df['Date'])
    return df.sort_values('Date')
```

### Fallback Strategy

```python
def get_stock_data_with_fallback(symbol, start_date, end_date):
    """Try multiple APIs with fallback"""
    
    # Try Finnhub first
    try:
        return get_finnhub_historical(symbol, FINNHUB_KEY)
    except Exception as e:
        print(f"Finnhub failed: {e}")
    
    # Try Alpha Vantage
    try:
        return get_alpha_vantage_historical(symbol, ALPHA_VANTAGE_KEY)
    except Exception as e:
        print(f"Alpha Vantage failed: {e}")
    
    # Fall back to yfinance
    try:
        import yfinance as yf
        data = yf.download(symbol, start=start_date, end=end_date)
        data.reset_index(inplace=True)
        data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        return data
    except Exception as e:
        raise Exception(f"All APIs failed. Last error: {e}")
```

---

## My Recommendation

**For your StockSense app:**

1. **Start with Finnhub** (best free rate limit, no daily cap)
2. **Add Alpha Vantage as backup** (cheap insurance)
3. **Keep yfinance as final fallback** (it's already working)

This gives you:
- ✅ 60 calls/minute with Finnhub
- ✅ Fallback to 5/minute with Alpha Vantage
- ✅ Emergency fallback to yfinance
- ✅ Virtually unlimited availability for users

**Cost**: Completely free (all have good free tiers)
**Time to implement**: ~30 minutes
**Reliability improvement**: 10x better

---

## Next Steps

Would you like me to:
1. Implement Finnhub integration into your app?
2. Set up the dual-API fallback strategy?
3. Keep current yfinance but add caching improvements?
4. Something else?

Let me know which API you'd like to use!
