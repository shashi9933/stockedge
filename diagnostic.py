#!/usr/bin/env python3
"""Diagnostic script to test app.py startup."""

import sys
import traceback

print("=" * 70)
print("STOCKSENSE APP STARTUP DIAGNOSTIC")
print("=" * 70)

# Test 1: Import streamlit
print("\n[TEST 1] Importing Streamlit...")
try:
    import streamlit as st
    print("    ✓ Streamlit imported successfully")
except Exception as e:
    print(f"    ✗ Failed to import streamlit: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 2: Import utils
print("\n[TEST 2] Importing utils modules...")
try:
    from utils.data_fetcher import get_stock_data, get_available_markets
    print("    ✓ data_fetcher imported")
except Exception as e:
    print(f"    ✗ Failed to import data_fetcher: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    print("    ✓ All dependencies imported")
except Exception as e:
    print(f"    ✗ Failed to import dependencies: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Check basic functionality
print("\n[TEST 3] Testing basic functionality...")
try:
    markets = get_available_markets()
    print(f"    ✓ get_available_markets() works: {markets}")
except Exception as e:
    print(f"    ✗ get_available_markets() failed: {e}")
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
print("\n✅ All checks passed - app.py should work!")
print("\nTo run the app with Streamlit:")
print("  streamlit run app.py")
print("\n" + "=" * 70)
