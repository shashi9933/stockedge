#!/usr/bin/env python3
"""Test script to check for import and runtime errors."""

import sys
import traceback

print("=" * 60)
print("TESTING STOCKSENSE APPLICATION FOR BUGS")
print("=" * 60)

test_results = []

# Test 1: Check utils imports
print("\n[TEST 1] Checking utility module imports...")
try:
    from utils import data_fetcher
    print("    ✓ data_fetcher imported successfully")
    test_results.append(("data_fetcher import", "PASS"))
except Exception as e:
    print(f"    ✗ data_fetcher import failed: {e}")
    test_results.append(("data_fetcher import", "FAIL", str(e)))

try:
    from utils import technical_indicators
    print("    ✓ technical_indicators imported successfully")
    test_results.append(("technical_indicators import", "PASS"))
except Exception as e:
    print(f"    ✗ technical_indicators import failed: {e}")
    test_results.append(("technical_indicators import", "FAIL", str(e)))

try:
    from utils import prediction_models
    print("    ✓ prediction_models imported successfully")
    test_results.append(("prediction_models import", "PASS"))
except Exception as e:
    print(f"    ✗ prediction_models import failed: {e}")
    test_results.append(("prediction_models import", "FAIL", str(e)))

try:
    from utils import chart_helpers
    print("    ✓ chart_helpers imported successfully")
    test_results.append(("chart_helpers import", "PASS"))
except Exception as e:
    print(f"    ✗ chart_helpers import failed: {e}")
    test_results.append(("chart_helpers import", "FAIL", str(e)))

try:
    from utils import price_alerts
    print("    ✓ price_alerts imported successfully")
    test_results.append(("price_alerts import", "PASS"))
except Exception as e:
    print(f"    ✗ price_alerts import failed: {e}")
    test_results.append(("price_alerts import", "FAIL", str(e)))

try:
    from utils import market_regime
    print("    ✓ market_regime imported successfully")
    test_results.append(("market_regime import", "PASS"))
except Exception as e:
    print(f"    ✗ market_regime import failed: {e}")
    test_results.append(("market_regime import", "FAIL", str(e)))

# Test 2: Check function availability
print("\n[TEST 2] Checking critical function existence...")

try:
    from utils.data_fetcher import get_stock_data, get_available_markets
    print("    ✓ data_fetcher functions exist")
    test_results.append(("data_fetcher functions", "PASS"))
except ImportError as e:
    print(f"    ✗ Missing functions in data_fetcher: {e}")
    test_results.append(("data_fetcher functions", "FAIL", str(e)))

try:
    from utils.technical_indicators import calculate_sma, calculate_rsi
    print("    ✓ technical_indicators functions exist")
    test_results.append(("technical_indicators functions", "PASS"))
except ImportError as e:
    print(f"    ✗ Missing functions in technical_indicators: {e}")
    test_results.append(("technical_indicators functions", "FAIL", str(e)))

try:
    from utils.chart_helpers import create_candlestick_chart
    print("    ✓ chart_helpers functions exist")
    test_results.append(("chart_helpers functions", "PASS"))
except ImportError as e:
    print(f"    ✗ Missing functions in chart_helpers: {e}")
    test_results.append(("chart_helpers functions", "FAIL", str(e)))

try:
    from utils.price_alerts import validate_phone_number
    print("    ✓ price_alerts functions exist")
    test_results.append(("price_alerts functions", "PASS"))
except ImportError as e:
    print(f"    ✗ Missing functions in price_alerts: {e}")
    test_results.append(("price_alerts functions", "FAIL", str(e)))

try:
    from utils.market_regime import detect_market_regime
    print("    ✓ market_regime functions exist")
    test_results.append(("market_regime functions", "PASS"))
except ImportError as e:
    print(f"    ✗ Missing functions in market_regime: {e}")
    test_results.append(("market_regime functions", "FAIL", str(e)))

# Test 3: Test page imports
print("\n[TEST 3] Checking page file syntax...")

try:
    import ast
    with open('pages/1_Chart_Analysis.py', 'r') as f:
        ast.parse(f.read())
    print("    ✓ 1_Chart_Analysis.py syntax OK")
    test_results.append(("1_Chart_Analysis.py syntax", "PASS"))
except SyntaxError as e:
    print(f"    ✗ 1_Chart_Analysis.py syntax error: {e}")
    test_results.append(("1_Chart_Analysis.py syntax", "FAIL", str(e)))

try:
    with open('pages/2_Technical_Indicators.py', 'r') as f:
        ast.parse(f.read())
    print("    ✓ 2_Technical_Indicators.py syntax OK")
    test_results.append(("2_Technical_Indicators.py syntax", "PASS"))
except SyntaxError as e:
    print(f"    ✗ 2_Technical_Indicators.py syntax error: {e}")
    test_results.append(("2_Technical_Indicators.py syntax", "FAIL", str(e)))

try:
    with open('pages/3_Prediction_Models.py', 'r') as f:
        ast.parse(f.read())
    print("    ✓ 3_Prediction_Models.py syntax OK")
    test_results.append(("3_Prediction_Models.py syntax", "PASS"))
except SyntaxError as e:
    print(f"    ✗ 3_Prediction_Models.py syntax error: {e}")
    test_results.append(("3_Prediction_Models.py syntax", "FAIL", str(e)))

try:
    with open('pages/4_Price_Alerts.py', 'r') as f:
        ast.parse(f.read())
    print("    ✓ 4_Price_Alerts.py syntax OK")
    test_results.append(("4_Price_Alerts.py syntax", "PASS"))
except SyntaxError as e:
    print(f"    ✗ 4_Price_Alerts.py syntax error: {e}")
    test_results.append(("4_Price_Alerts.py syntax", "FAIL", str(e)))

# Test 4: Logical checks
print("\n[TEST 4] Checking common logic errors...")

# Check for missing phone validation function
try:
    from utils.price_alerts import validate_phone_number
    import pandas as pd
    import numpy as np
    
    # Test with valid phone
    result = validate_phone_number("+12025551234")
    if result:
        print("    ✓ Phone validation function works")
        test_results.append(("Phone validation", "PASS"))
    else:
        print("    ⚠ Phone validation may not work correctly")
        test_results.append(("Phone validation", "WARN", "Returns False for valid phone"))
except Exception as e:
    print(f"    ✗ Phone validation error: {e}")
    test_results.append(("Phone validation", "FAIL", str(e)))

# Print summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)

passed = sum(1 for r in test_results if r[1] == "PASS")
failed = sum(1 for r in test_results if r[1] == "FAIL")
warned = sum(1 for r in test_results if r[1] == "WARN")

print(f"\nTotal Tests: {len(test_results)}")
print(f"  PASS: {passed}")
print(f"  FAIL: {failed}")
print(f"  WARN: {warned}")

if failed > 0:
    print("\nFailed Tests:")
    for result in test_results:
        if result[1] == "FAIL":
            print(f"  - {result[0]}: {result[2] if len(result) > 2 else 'Unknown error'}")

if warned > 0:
    print("\nWarnings:")
    for result in test_results:
        if result[1] == "WARN":
            print(f"  - {result[0]}: {result[2] if len(result) > 2 else 'Unknown warning'}")

print("\n" + "=" * 60)
if failed == 0:
    print("Result: ALL TESTS PASSED - Ready to run!")
else:
    print(f"Result: {failed} TESTS FAILED - See errors above")
print("=" * 60)
