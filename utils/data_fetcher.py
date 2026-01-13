import yfinance as yf
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta
import streamlit as st

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

@st.cache_data(ttl=3600)  # Cache data for 1 hour (increased for better rate limit handling)
def get_stock_data(symbol, start_date, end_date):
    """
    Fetches stock data with intelligent caching, rate limit handling, and exponential backoff.
    
    Features:
    - Aggressive caching to minimize API calls
    - Exponential backoff for rate limiting
    - User-agent rotation
    - Smart retry logic
    - Clear error messages
    
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
    
    # Initial delay to avoid hammering the API
    time.sleep(random.uniform(1, 3))
    
    # Try fetching the data with exponential backoff
    attempts = 0
    max_attempts = 4  # Increased attempts for rate limiting
    last_error = None
    
    while attempts < max_attempts:
        try:
            # Rotate user agents to avoid IP-based rate limiting
            user_agent = random.choice(USER_AGENTS)
            
            # Create Ticker object with user agent
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            # Using a longer timeout and better error handling
            data = ticker.history(
                start=start_date, 
                end=end_date + timedelta(days=1)
            )
            
            # Validate data
            if data.empty:
                last_error = f"No data found for {symbol}. Verify the symbol is correct."
                raise ValueError(last_error)
            
            # Check if we have any valid OHLCV columns
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in data.columns for col in required_cols):
                last_error = f"Invalid data structure for {symbol}"
                raise ValueError(last_error)
            
            # Success! Return the data
            return data
            
        except Exception as e:
            attempts += 1
            last_error = str(e)
            
            # Check if it's a rate limit error
            is_rate_limit = any(phrase in str(e).lower() for phrase in 
                               ['too many requests', 'rate limit', '429', 'throttle', 'quota'])
            
            if attempts < max_attempts:
                if is_rate_limit:
                    # For rate limit errors, use longer exponential backoff
                    wait_time = (2 ** attempts) + random.uniform(1, 5)  # 2^1 to 2^4 seconds
                    st.warning(f"⏳ Rate limited. Retrying in {wait_time:.0f}s... (Attempt {attempts}/{max_attempts})")
                else:
                    # For other errors, use standard backoff
                    wait_time = random.uniform(2 + (2 * attempts), 5 + (2 * attempts))
                
                time.sleep(wait_time)
            else:
                # All attempts failed - provide helpful error message
                error_msg = f"Failed to fetch data for {symbol} after {max_attempts} attempts."
                
                if is_rate_limit:
                    error_msg += "\n\n⏳ **API Rate Limit Hit**\nThe API is receiving too many requests. "
                    error_msg += "Please wait a moment and try again. This is temporary."
                elif "No data" in last_error or "not found" in last_error.lower():
                    error_msg += "\n\n❌ **Symbol Not Found**\nPlease verify the stock symbol is correct."
                    error_msg += "\nExamples: AAPL (Apple), RELIANCE.NS (Reliance), INFY.NS (Infosys)"
                elif "connection" in last_error.lower() or "network" in last_error.lower():
                    error_msg += "\n\n🌐 **Network Error**\nPlease check your internet connection and try again."
                else:
                    error_msg += f"\n\n❌ Details: {last_error}"
                
                raise Exception(error_msg)

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
