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
    Fetches stock data with intelligent rate limiting, smart caching, and exponential backoff.
    
    Features:
    - Client-side request throttling
    - Aggressive caching (1 hour TTL)
    - Smart exponential backoff
    - Per-symbol rate limit cooldown
    - Clear progress messages
    - Working example suggestions on failure
    
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
        st.info(f"⏳ Waiting {wait_time:.0f}s before retry (throttling to avoid rate limits)...")
        time.sleep(wait_time)
    
    # Try fetching the data with exponential backoff
    attempts = 0
    max_attempts = 5  # More attempts now
    last_error = None
    
    while attempts < max_attempts:
        # Check if we should continue retrying
        if not throttler.can_retry(symbol):
            raise Exception(
                f"⏳ **Rate Limit Cooldown Active**\n\n"
                f"Too many failed attempts for {symbol}.\n\n"
                f"**Please wait at least 5 minutes before trying again.**\n\n"
                f"In the meantime:\n"
                f"• Try a different stock symbol\n"
                f"• View previously fetched data\n"
                f"• Refresh the page and try later"
            )
        
        try:
            attempts += 1
            
            # Initial delay to avoid hammering
            if attempts == 1:
                time.sleep(random.uniform(1, 2))
            
            # Create Ticker object
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            data = ticker.history(
                start=start_date, 
                end=end_date + timedelta(days=1)
            )
            
            # Validate data
            if data.empty:
                last_error = f"No data found for {symbol}. Verify the symbol is correct."
                raise ValueError(last_error)
            
            # Check if we have valid OHLCV columns
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in data.columns for col in required_cols):
                last_error = f"Invalid data structure for {symbol}"
                raise ValueError(last_error)
            
            # Success! Record it and return
            throttler.record_request(symbol)
            return data
            
        except Exception as e:
            last_error = str(e)
            is_rate_limit = any(phrase in last_error.lower() for phrase in 
                               ['too many requests', 'rate limit', '429', 'throttle', 'quota', 'http 429'])
            
            if is_rate_limit:
                # Record the rate limit
                throttler.record_rate_limit(symbol)
            
            if attempts < max_attempts:
                # Calculate wait time with exponential backoff
                if is_rate_limit:
                    # Much longer wait for rate limits
                    wait_time = throttler.get_retry_wait_time(symbol, attempts)
                    wait_time += random.uniform(2, 5)  # Add randomness
                else:
                    # Standard backoff for other errors
                    wait_time = (2 ** attempts) + random.uniform(1, 3)
                
                wait_display = f"{wait_time:.0f}s"
                
                if is_rate_limit:
                    st.warning(
                        f"⏳ Rate limited. Waiting {wait_display}... "
                        f"(Attempt {attempts}/{max_attempts})"
                    )
                else:
                    st.info(
                        f"⏳ Retrying in {wait_display}... "
                        f"(Attempt {attempts}/{max_attempts})"
                    )
                
                time.sleep(wait_time)
            else:
                # All attempts failed
                if is_rate_limit:
                    raise Exception(
                        f"**⏳ API Rate Limit Hit**\n\n"
                        f"The yfinance API is rate-limited (too many requests).\n\n"
                        f"**What to do:**\n"
                        f"1. **Wait 2-5 minutes** - The API limit resets\n"
                        f"2. **Try a different stock** - Switch to another symbol\n"
                        f"3. **Come back later** - Try after a few minutes\n\n"
                        f"**Why it happens:**\n"
                        f"yfinance is a free service with shared API limits. During peak hours "
                        f"(market open), many users hit the same limits.\n\n"
                        f"**Working examples to try:**\n"
                        f"• AAPL (Apple)\n"
                        f"• MSFT (Microsoft)\n"
                        f"• RELIANCE.NS (Reliance)"
                    )
                elif "No data" in last_error or "not found" in last_error.lower():
                    raise Exception(
                        f"**❌ Symbol Not Found**\n\n"
                        f"'{symbol}' not found or has no data.\n\n"
                        f"**Try these working examples:**\n\n"
                        f"**Global Stocks:**\n"
                        f"• AAPL (Apple)\n"
                        f"• MSFT (Microsoft)\n"
                        f"• GOOGL (Google)\n"
                        f"• TSLA (Tesla)\n\n"
                        f"**Indian Stocks (NSE):**\n"
                        f"• RELIANCE.NS (Reliance)\n"
                        f"• TCS.NS (Tata Consultancy)\n"
                        f"• INFY.NS (Infosys)\n"
                        f"• HDFCBANK.NS (HDFC Bank)"
                    )
                else:
                    raise Exception(
                        f"**Failed to fetch data after {max_attempts} attempts**\n\n"
                        f"Error: {last_error}\n\n"
                        f"**Troubleshooting:**\n"
                        f"• Check symbol spelling (AAPL, not APPLE)\n"
                        f"• For Indian stocks, add .NS or .BO (RELIANCE.NS)\n"
                        f"• Ensure the date range has trading data\n"
                        f"• Try again in a few moments"
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
