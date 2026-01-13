# Rate Limiting & API Handling Guide

## What Happened

You encountered a **yfinance API rate limit error**:
```
❌ Too Many Requests. Rate limited. Try after a while.
```

This is normal and temporary. Here's what was done to improve it.

## Improvements Made

### 1. **Increased Cache Duration**
- **Before**: 15 minutes
- **After**: 1 hour
- **Benefit**: Same stock data is reused for up to 1 hour, reducing API calls

### 2. **Smarter Exponential Backoff**
- **Before**: Simple fixed delays (2-5 seconds)
- **After**: Exponential backoff (2^1 to 2^4 = 2 to 16 seconds)
- **Benefit**: Better handling of rate limits with increasingly longer wait times

### 3. **Better Rate Limit Detection**
- Detects "too many requests", "rate limit", "429" errors specifically
- Provides context-aware error messages
- Shows retry progress to the user

### 4. **More Retry Attempts**
- **Before**: 3 attempts
- **After**: 4 attempts with longer waits
- **Benefit**: Higher chance of success during temporary spikes

### 5. **User-Friendly Error Messages**
- Detects if it's a rate limit vs. symbol not found vs. network error
- Provides specific advice for each type of error
- Shows working examples when symbol errors occur

## Understanding Rate Limiting

### Why It Happens
- YFinance API has usage limits
- Free tier users share the API bandwidth
- Peak market hours = more requests = more limits
- Too many requests from the same IP can trigger limits

### How Long Does It Last?
- Usually **1-2 minutes**
- Can be longer during peak market hours (9:30-10:30 AM US time)
- Never permanent - always temporary

### When It's Most Likely
- ⏰ Market opening hours (9:30-10:00 AM EST)
- 📊 Right after major news events
- 🔄 Multiple rapid requests in short time
- 👥 When many users fetch data simultaneously

## How to Avoid Rate Limiting

### ✅ Best Practices

1. **Wait Between Requests**
   - The app automatically adds delays
   - Additional manual wait helps

2. **Use Caching**
   - Recent data is cached for 1 hour
   - Fetching the same stock twice uses cache (no new API call)
   - Reload same stock = instant results

3. **Fetch Less Frequently**
   - Don't repeatedly refresh the same symbol
   - Switch between different symbols
   - Let data cache naturally

4. **Try During Quiet Hours**
   - After market close (4:00+ PM EST)
   - Before market open (before 9:30 AM EST)
   - Weekends

5. **Use Multiple Symbols**
   - If INFY.NS fails, try RELIANCE.NS
   - Then come back to INFY.NS later
   - Spreads the API load

### ❌ What to Avoid

❌ Rapid clicking of "Fetch Stock Data"
❌ Fetching the same stock every 10 seconds
❌ Opening the app in multiple tabs
❌ Refreshing the page repeatedly
❌ During peak market hours (if possible)

## What Happens Now

### On Rate Limit Error

The app will:
1. **Show a warning**: "⏳ Rate limited. Retrying..."
2. **Wait longer each time**: Exponential backoff
3. **Retry up to 4 times**: Better chance of success
4. **Give you advice**: Specific instructions on what to do

### Example Flow
```
Attempt 1: Try → Rate limit → Wait 2-3 seconds
Attempt 2: Try → Rate limit → Wait 4-5 seconds
Attempt 3: Try → Rate limit → Wait 8-9 seconds
Attempt 4: Try → Rate limit → Show error message & advice
```

### User-Friendly Messages

**Rate Limit Error:**
```
❌ API Rate Limit Reached

⏳ The stock data API is receiving too many requests.

✅ What to do:
• Wait 1-2 minutes and try again
• Try a different stock symbol first
• The app caches data for 1 hour to reduce requests
```

**Symbol Not Found:**
```
💡 Stock Symbol Not Found

✅ Try these working examples:
• AAPL (Apple)
• RELIANCE.NS (Reliance Industries)
• INFY.NS (Infosys)
```

## Caching Explained

### How It Works
```
First fetch of AAPL:
  → API call → Get data → Cache it

Second fetch of AAPL (within 1 hour):
  → Check cache → Found → Return instantly
  → No API call needed!

After 1 hour:
  → Cache expires → Next fetch calls API again
```

### Benefits
- ✅ Instant results for recently fetched stocks
- ✅ Reduces API calls significantly
- ✅ Better performance overall
- ✅ Helps avoid rate limiting

## If You Still Get Rate Limited

### Immediate Actions
1. **Wait 2-3 minutes** - This is usually enough
2. **Try a different stock** - Use one of the examples
3. **Come back later** - After market hours are quieter
4. **Close & reopen** - Fresh session sometimes helps

### Long-term Solution
The app now automatically:
- ✅ Caches for 1 hour
- ✅ Uses exponential backoff
- ✅ Detects rate limits early
- ✅ Retries intelligently
- ✅ Shows helpful messages

## Technical Details

### Cache Settings
```python
@st.cache_data(ttl=3600)  # 1 hour cache
def get_stock_data(symbol, start_date, end_date):
    # ...
```

### Backoff Algorithm
```python
wait_time = (2 ** attempts) + random.uniform(1, 5)
# Attempt 1: 2^1 = 2 seconds (+ 1-5 random)
# Attempt 2: 2^2 = 4 seconds (+ 1-5 random)
# Attempt 3: 2^3 = 8 seconds (+ 1-5 random)
# Attempt 4: 2^4 = 16 seconds (+ 1-5 random)
```

### Rate Limit Detection
```python
is_rate_limit = any(phrase in str(error).lower() for phrase in
    ['too many requests', 'rate limit', '429', 'throttle', 'quota'])
```

## Alternative Solutions

If rate limiting continues to be an issue:

1. **Use API Key** (Advanced)
   - Some free stock APIs offer higher limits with a key
   - Would require code changes

2. **Cache Locally** (Advanced)
   - Store historical data locally
   - Reduces repeated API calls

3. **Different API** (Advanced)
   - Alpha Vantage
   - IEX Cloud
   - Polygon.io
   - (Would require code changes)

## Summary

### ✅ What's Fixed
- Smarter rate limit handling
- Better error messages
- Longer cache duration
- More intelligent retries
- Helpful user guidance

### ✅ What to Do
- Wait 1-2 minutes if you see rate limit
- Try different stocks meanwhile
- Come back to the failed symbol later
- The app automatically handles the rest

### ✅ When to Worry
- You don't need to! Rate limiting is temporary and handled
- The app will retry automatically
- Clear messages guide you

---

**Status**: ✅ Rate limiting improved and handled gracefully

*Updated: January 13, 2026*
