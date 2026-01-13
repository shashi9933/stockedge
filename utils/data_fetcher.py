import yfinance as yf
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta
import streamlit as st
from utils.request_throttler import get_throttler

# User agents for API request rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

def get_available_markets():
    """Return a list of available stock markets."""
    return ["Global", "NSE (India)", "BSE (India)"]

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def get_stock_data(symbol, start_date, end_date):
    """
    Fetches stock data with intelligent rate limiting and smart caching.
    
    Strategy:
    - Fail fast on rate limits (don't keep retrying)
    - Use cached data when available
    - Only retry for network/transient errors
    - Suggest using cached data if rate limited
    
    Args:
        symbol (str): Stock symbol (e.g., AAPL, RELIANCE.NS)
        start_date (datetime): Start date for data
        end_date (datetime): End date for data
        
    Returns:
        pandas.DataFrame: Historical stock data
    """
    import yfinance as yf
    
    # Validate inputs
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Stock symbol must be a non-empty string")
    
    symbol = symbol.strip().upper()
    throttler = get_throttler()
    
    # Check if we should wait before requesting
    wait_time = throttler.wait_if_needed(symbol)
    if wait_time:
        st.info(f"⏳ Waiting {wait_time:.0f}s before retry (respecting API limits)...")
        time.sleep(wait_time)
    
    # Try fetching with MINIMAL retries for rate limits
    attempts = 0
    max_attempts = 2  # Only 2 attempts - fail fast on rate limits
    last_error = None
    
    while attempts < max_attempts:
        try:
            attempts += 1
            
            # Initial delay to avoid immediate hammering
            if attempts == 1:
                time.sleep(random.uniform(0.5, 1.5))
            
            # Create Ticker object
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            data = ticker.history(
                start=start_date, 
                end=end_date + timedelta(days=1)
            )
            
            # Validate data
            if data.empty:
                raise ValueError(f"No data found for {symbol}. Verify the symbol is correct.")
            
            # Check if we have valid OHLCV columns
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in data.columns for col in required_cols):
                raise ValueError(f"Invalid data structure for {symbol}")
            
            # Success! Record and return
            throttler.record_request(symbol)
            return data
            
        except Exception as e:
            last_error = str(e)
            is_rate_limit = any(phrase in last_error.lower() for phrase in 
                               ['too many requests', 'rate limit', '429', 'throttle', 'quota', 'http 429'])
            
            if is_rate_limit:
                # For rate limits: fail fast, don't retry
                throttler.record_rate_limit(symbol)
                
                raise Exception(
                    f"🔄 **API Rate Limit - Please Wait**\n\n"
                    f"The stock API is temporarily rate-limited due to high traffic.\n\n"
                    f"**What to do right now:**\n"
                    f"1. **Try a different stock** - Try AAPL, MSFT, or GOOGL\n"
                    f"2. **Check back in 2-3 minutes** - The limit resets quickly\n"
                    f"3. **Use your cached data** - Refresh to see previously loaded stocks\n\n"
                    f"**Why this happens:**\n"
                    f"yfinance is a free API shared by thousands of users. "
                    f"During busy times (like market open), everyone hits the same limits.\n\n"
                    f"**After waiting:**\n"
                    f"Come back and try {symbol} again - it should work!"
                )
            
            # For other errors, retry once more
            if attempts < max_attempts:
                wait_time = 3 + random.uniform(1, 2)
                st.info(f"⏳ Retrying in {wait_time:.0f}s... (Attempt {attempts}/{max_attempts})")
                time.sleep(wait_time)
            else:
                # Final attempt failed
                if "No data" in last_error or "not found" in last_error.lower():
                    raise Exception(
                        f"**❌ Stock Not Found**\n\n"
                        f"'{symbol}' doesn't exist or has no data.\n\n"
                        f"**Try these instead:**\n\n"
                        f"**US Stocks:**\n"
                        f"• AAPL - Apple\n"
                        f"• MSFT - Microsoft\n"
                        f"• GOOGL - Google\n"
                        f"• TSLA - Tesla\n\n"
                        f"**Indian Stocks (NSE):**\n"
                        f"• RELIANCE.NS - Reliance\n"
                        f"• TCS.NS - Tata Consultancy\n"
                        f"• INFY.NS - Infosys\n"
                        f"• HDFCBANK.NS - HDFC Bank"
                    )
                else:
                    raise Exception(
                        f"**Network Error**\n\n"
                        f"Could not fetch {symbol}.\n\n"
                        f"**Try:**\n"
                        f"• Check your internet connection\n"
                        f"• Wait a moment and try again\n"
                        f"• Try a different stock symbol"
                    )

@st.cache_data(ttl=86400)  # Cache for 24 hours
def get_stock_info(symbol):
    """
    Get detailed information about a stock.
    
    Args:
        symbol (str): Stock symbol
        
    Returns:
        dict: Stock information
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return info
    except Exception as e:
        raise Exception(f"Error fetching stock information: {str(e)}")

def format_indian_stock_symbol(symbol, exchange):
    """
    Formats stock symbols for Indian exchanges if not already formatted.
    
    Args:
        symbol (str): Stock symbol
        exchange (str): 'NSE' or 'BSE'
        
    Returns:
        str: Properly formatted stock symbol
    """
    if exchange == "NSE" and not symbol.endswith(".NS"):
        return f"{symbol}.NS"
    elif exchange == "BSE" and not symbol.endswith(".BO"):
        return f"{symbol}.BO"
    return symbol

def validate_stock_symbol(symbol):
    """
    Validates if a stock symbol exists.
    
    Args:
        symbol (str): Stock symbol to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # If we can fetch market cap, the stock likely exists
        if 'marketCap' in info and info['marketCap'] is not None:
            return True
        return False
    except:
        return False
