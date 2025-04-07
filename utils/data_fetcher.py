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

@st.cache_data(ttl=900)  # Cache data for 15 minutes
def get_stock_data(symbol, start_date, end_date):
    """
    Fetches stock data with caching, rate limit handling, and fallback mechanisms.
    
    Args:
        symbol (str): Stock symbol (e.g., AAPL, RELIANCE.NS)
        start_date (datetime): Start date for data
        end_date (datetime): End date for data
        
    Returns:
        pandas.DataFrame: Historical stock data
    """
    # Add random delay to mitigate rate limiting
    time.sleep(random.uniform(0.5, 2))
    
    # Rotate user agents
    user_agent = random.choice(USER_AGENTS)
    
    # Try fetching the data with up to 3 attempts
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        try:
            # Create Ticker object
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            data = ticker.history(
                start=start_date, 
                end=end_date + timedelta(days=1),  # Add one day to include end_date
                auto_adjust=True
            )
            
            if data.empty:
                raise ValueError(f"No data found for {symbol} in the specified date range.")
            
            return data
            
        except Exception as e:
            attempts += 1
            if attempts < max_attempts:
                # Wait longer between retries
                time.sleep(random.uniform(2, 5))
            else:
                raise Exception(f"Failed to fetch data after {max_attempts} attempts: {str(e)}")

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
