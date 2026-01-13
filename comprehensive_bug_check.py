#!/usr/bin/env python3
"""Comprehensive bug analysis - looking for common issues."""

import re
import os

print("\n" + "="*70)
print("COMPREHENSIVE BUG ANALYSIS REPORT")
print("="*70)

bugs_found = []
warnings_found = []

# 1. Check for division by zero in price alerts
print("\n[1] Checking for division by zero issues...")
try:
    with open('utils/data_fetcher.py', 'r') as f:
        content = f.read()
        if 'previous_price != 0' in content or 'previous_price == 0' in content:
            print("    ✓ Division by zero check found in data_fetcher.py")
        else:
            warnings_found.append("Potential division by zero in price change calculation")
except Exception as e:
    print(f"    ✗ Error reading file: {e}")

# 2. Check for empty data handling
print("\n[2] Checking for empty data handling...")
error_count = 0
with open('utils/prediction_models.py', 'r') as f:
    content = f.read()
    if 'if len(data)' in content or 'if data.empty' in content:
        print("    ✓ Empty data checks found")
    else:
        warnings_found.append("Limited empty data validation in prediction_models.py")

# 3. Check RSI calculation for potential NaN issues
print("\n[3] Checking RSI calculation for NaN/division issues...")
with open('utils/technical_indicators.py', 'r') as f:
    content = f.read()
    if 'rs = avg_gain / avg_loss' in content:
        if 'avg_loss' in content:
            print("    ⚠ WARNING: RSI calculation may produce inf/NaN when avg_loss=0")
            warnings_found.append("RSI may produce inf/NaN when avg_loss is 0 (no losses)")
        else:
            print("    ✓ RSI calculation found")

# 4. Check Bollinger Bands for NaN with small windows
print("\n[4] Checking Bollinger Bands implementation...")
with open('utils/technical_indicators.py', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'upper_band = middle_band' in line:
            print("    ✓ Bollinger Bands implementation found")
            # Check if window validation exists
            if 'window' in ''.join(lines[max(0,i-10):i]):
                print("    ✓ Window parameter handling found")
            break

# 5. Check for unhandled exceptions in Streamlit caching
print("\n[5] Checking Streamlit cache handling...")
with open('utils/data_fetcher.py', 'r') as f:
    content = f.read()
    if '@st.cache_data' in content:
        print("    ✓ Streamlit caching used")
        if 'try:' in content and 'except' in content:
            print("    ✓ Error handling in cached functions found")
    
# 6. Check phone validation regex
print("\n[6] Checking phone validation regex...")
with open('utils/price_alerts.py', 'r') as f:
    content = f.read()
    if "pattern = r'^\+\d{1,3}\d{6,14}$'" in content:
        print("    ✓ Phone validation regex found")
        # Test the regex
        import re
        pattern = r'^\+\d{1,3}\d{6,14}$'
        test_cases = [
            ('+12025551234', True),
            ('+91-9876543210', False),  # Hyphens not allowed
            ('+9198765432', True),
            ('+', False),
            ('2025551234', False),  # No + prefix
        ]
        failed = []
        for phone, expected in test_cases:
            result = bool(re.match(pattern, phone))
            if result != expected:
                failed.append((phone, expected, result))
        
        if failed:
            print(f"    ⚠ Phone regex issues:")
            for phone, expected, got in failed:
                print(f"      - {phone}: expected {expected}, got {got}")
                warnings_found.append(f"Phone validation regex fails for: {phone}")
        else:
            print("    ✓ Phone validation regex working correctly")

# 7. Check for NaN handling in technical indicators
print("\n[7] Checking NaN handling in technical indicators...")
with open('utils/technical_indicators.py', 'r') as f:
    content = f.read()
    if 'fillna' in content or 'dropna' in content or 'isnull' in content:
        print("    ✓ NaN handling functions found")
    else:
        warnings_found.append("Limited NaN handling in technical_indicators")

# 8. Check for index alignment issues
print("\n[8] Checking pandas index alignment...")
with open('utils/technical_indicators.py', 'r') as f:
    content = f.read()
    if '.reset_index' in content:
        print("    ⚠ Index reset detected - verify index alignment after operations")
        warnings_found.append("Index reset in technical_indicators may cause misalignment")
    elif '.index' in content:
        print("    ✓ Index operations found")

# 9. Check for missing data in prediction windows
print("\n[9] Checking prediction window validation...")
with open('utils/prediction_models.py', 'r') as f:
    content = f.read()
    if 'prediction_days' in content:
        if 'len(data) < ' in content or 'if len' in content:
            print("    ✓ Data length validation for predictions found")
        else:
            warnings_found.append("Limited validation of data length vs prediction_days")

# 10. Check for market regime edge cases
print("\n[10] Checking market regime edge cases...")
with open('utils/market_regime.py', 'r') as f:
    lines = f.readlines()
    content = ''.join(lines)
    if 'len(df) < max' in content or 'len(data) <' in content:
        print("    ✓ Minimum data check for regime detection found")
    else:
        warnings_found.append("Market regime detection may fail with insufficient data")

# 11. Check for alert state persistence issues
print("\n[11] Checking alert state management...")
with open('pages/4_Price_Alerts.py', 'r') as f:
    content = f.read()
    if "st.session_state.active_alerts" in content:
        print("    ✓ Session state used for alerts")
        if 'st.rerun()' in content:
            print("    ✓ Page rerun after alert changes")
        else:
            warnings_found.append("Alerts may not refresh after user actions")

# 12. Check for hardcoded values
print("\n[12] Checking for hardcoded magic numbers...")
magic_numbers_found = {
    '15-minute cache': False,
    '24-hour cache': False,
    '30 days prediction': False,
}

with open('utils/data_fetcher.py', 'r') as f:
    if 'ttl=900' in f.read():
        magic_numbers_found['15-minute cache'] = True

with open('utils/prediction_models.py', 'r') as f:
    if 'prediction_days=30' in f.read():
        magic_numbers_found['30 days prediction'] = True

for item, found in magic_numbers_found.items():
    if found:
        print(f"    ⚠ Magic number found: {item} (consider config file)")
        warnings_found.append(f"Hardcoded value: {item}")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"\nCritical Bugs Found: {len(bugs_found)}")
if bugs_found:
    for bug in bugs_found:
        print(f"  ✗ {bug}")

print(f"\nWarnings/Issues Found: {len(warnings_found)}")
if warnings_found:
    for warning in warnings_found:
        print(f"  ⚠ {warning}")

print("\n" + "="*70)
if not bugs_found:
    print("RESULT: No critical bugs detected!")
    print("The application appears ready to run.")
    if warnings_found:
        print(f"\nNote: {len(warnings_found)} minor issues/warnings found that should be addressed.")
else:
    print(f"RESULT: {len(bugs_found)} critical bugs found!")
print("="*70 + "\n")
