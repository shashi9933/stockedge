#!/usr/bin/env python3
"""
Debug script to test if yfinance API is working properly
Run this to diagnose connectivity issues
"""

import sys
import os
import yfinance as yf
from datetime import datetime, timedelta

def test_yfinance_api():
    """Test basic yfinance API functionality"""
    
    print("=" * 60)
    print("YFINANCE API DEBUG TEST")
    print("=" * 60)
    
    # Test 1: Simple global stock
    print("\n[TEST 1] Fetching AAPL (Apple) data...")
    try:
        aapl = yf.Ticker("AAPL")
        aapl_hist = aapl.history(period="5d")
        print(f"[SUCCESS] AAPL: {len(aapl_hist)} rows fetched")
        print(f"   Latest Close: ${aapl_hist['Close'].iloc[-1]:.2f}")
        print(aapl_hist.tail(2))
    except Exception as e:
        print(f"[FAILED] AAPL: {str(e)}")
    
    # Test 2: Indian NSE stock
    print("\n[TEST 2] Fetching RELIANCE.NS (Reliance Industries) data...")
    try:
        reliance = yf.Ticker("RELIANCE.NS")
        reliance_hist = reliance.history(period="5d")
        print(f"[SUCCESS] RELIANCE.NS: {len(reliance_hist)} rows fetched")
        print(f"   Latest Close: INR {reliance_hist['Close'].iloc[-1]:.2f}")
        print(reliance_hist.tail(2))
    except Exception as e:
        print(f"[FAILED] RELIANCE.NS: {str(e)}")
    
    # Test 3: Another global stock
    print("\n[TEST 3] Fetching MSFT (Microsoft) data...")
    try:
        msft = yf.Ticker("MSFT")
        msft_hist = msft.history(period="5d")
        print(f"[SUCCESS] MSFT: {len(msft_hist)} rows fetched")
        print(f"   Latest Close: ${msft_hist['Close'].iloc[-1]:.2f}")
        print(msft_hist.tail(2))
    except Exception as e:
        print(f"[FAILED] MSFT: {str(e)}")
    
    # Test 4: With custom date range
    print("\n[TEST 4] Fetching TCS.NS with custom date range...")
    try:
        start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        end = datetime.now().strftime("%Y-%m-%d")
        tcs = yf.Ticker("TCS.NS")
        tcs_hist = tcs.history(start=start, end=end)
        print(f"[SUCCESS] TCS.NS: {len(tcs_hist)} rows fetched")
        print(f"   Date range: {start} to {end}")
        print(f"   Latest Close: INR {tcs_hist['Close'].iloc[-1]:.2f}")
        print(tcs_hist.tail(2))
    except Exception as e:
        print(f"[FAILED] TCS.NS: {str(e)}")
    
    # Test 5: Test actual get_stock_data function
    print("\n[TEST 5] Testing actual get_stock_data function...")
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from utils.data_fetcher import get_stock_data
        
        data = get_stock_data("GOOGL", 
                            datetime.now() - timedelta(days=30), 
                            datetime.now())
        print(f"[SUCCESS] get_stock_data: {len(data)} rows fetched")
        print(f"   Latest Close: ${data['Close'].iloc[-1]:.2f}")
        print(data.tail(2))
    except Exception as e:
        print(f"[FAILED] get_stock_data: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("DEBUG TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_yfinance_api()
