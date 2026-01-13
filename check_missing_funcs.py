#!/usr/bin/env python3
"""Deep dive bug detection - check for missing imported functions."""

import ast

def get_functions_from_file(filepath):
    """Extract all function names from a Python file."""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    
    functions = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.add(node.name)
    
    return functions

print("\n" + "="*70)
print("CHECKING FOR MISSING IMPORTS/FUNCTION DEFINITIONS")
print("="*70)

# Check price_alerts.py
print("\n[1] Checking utils/price_alerts.py for required functions...")
price_alerts_funcs = get_functions_from_file('utils/price_alerts.py')
required_price_alerts = {
    'validate_phone_number',
    'add_price_alert',
    'remove_price_alert',
    'display_alerts',
    'check_price_alerts',
    'send_alert_notification'
}

missing_price_alerts = required_price_alerts - price_alerts_funcs
if missing_price_alerts:
    print(f"    ERROR: Missing functions in price_alerts.py:")
    for func in missing_price_alerts:
        print(f"      ✗ {func}")
else:
    print(f"    OK: All required functions present")

# Check prediction_models.py
print("\n[2] Checking utils/prediction_models.py for required functions...")
pred_funcs = get_functions_from_file('utils/prediction_models.py')
required_pred = {
    'linear_regression_prediction',
    'quadratic_regression_prediction',
    'fourier_transform_prediction',
    'time_series_prediction',
    'arima_model_prediction',
    'ensemble_prediction',
    'plot_predictions',
    'plot_ensemble_weights'
}

missing_pred = required_pred - pred_funcs
if missing_pred:
    print(f"    ERROR: Missing functions in prediction_models.py:")
    for func in missing_pred:
        print(f"      ✗ {func}")
else:
    print(f"    OK: All required functions present")

# Check chart_helpers.py
print("\n[3] Checking utils/chart_helpers.py for required functions...")
chart_funcs = get_functions_from_file('utils/chart_helpers.py')
required_chart = {
    'create_candlestick_chart',
    'add_range_selector',
    'add_pivot_points',
    'add_annotations'
}

missing_chart = required_chart - chart_funcs
if missing_chart:
    print(f"    ERROR: Missing functions in chart_helpers.py:")
    for func in missing_chart:
        print(f"      ✗ {func}")
else:
    print(f"    OK: All required functions present")

# Check technical_indicators.py
print("\n[4] Checking utils/technical_indicators.py for required functions...")
tech_funcs = get_functions_from_file('utils/technical_indicators.py')
required_tech = {
    'detect_candlestick_patterns',
    'plot_with_indicators'
}

missing_tech = required_tech - tech_funcs
if missing_tech:
    print(f"    ERROR: Missing functions in technical_indicators.py:")
    for func in missing_tech:
        print(f"      ✗ {func}")
else:
    print(f"    OK: All required functions present")

# Check market_regime.py
print("\n[5] Checking utils/market_regime.py for required functions...")
regime_funcs = get_functions_from_file('utils/market_regime.py')
required_regime = {
    'detect_market_regime',
    'get_regime_description',
    'get_recommended_settings',
    'plot_market_regime',
    'get_preferred_models_for_regime'
}

missing_regime = required_regime - regime_funcs
if missing_regime:
    print(f"    ERROR: Missing functions in market_regime.py:")
    for func in missing_regime:
        print(f"      ✗ {func}")
else:
    print(f"    OK: All required functions present")

# Summary
all_missing = missing_price_alerts | missing_pred | missing_chart | missing_tech | missing_regime

print("\n" + "="*70)
if all_missing:
    print(f"FOUND {len(all_missing)} MISSING FUNCTION(S):")
    for func in sorted(all_missing):
        print(f"  - {func}")
    print("\nTHESE NEED TO BE IMPLEMENTED!")
else:
    print("SUCCESS: All required functions exist!")
print("="*70 + "\n")
