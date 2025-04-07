import streamlit as st
import pandas as pd
import re
from datetime import datetime
from utils.price_alerts import (
    validate_phone_number,
    add_price_alert,
    remove_price_alert,
    display_alerts,
    check_price_alerts,
    send_alert_notification
)

# Set page configuration
st.set_page_config(
    page_title="Price Alerts - Stock Market Analysis Platform",
    page_icon="📈",
    layout="wide"
)

st.title("Price Alerts")
st.markdown("Set up custom price alerts for your selected stocks.")

# Check if stock data exists in session state
if 'stock_data' not in st.session_state or st.session_state.stock_data is None:
    st.warning("Please select a stock from the home page first.")
    st.stop()

# Get stock data from session state
stock_data = st.session_state.stock_data
stock_symbol = st.session_state.selected_stock

# Display current stock info
current_price = stock_data['Close'].iloc[-1]
st.subheader(f"Current Stock: {stock_symbol}")
st.metric("Current Price", f"${current_price:.2f}")

# Create alert form
st.subheader("Create New Alert")

with st.form("price_alert_form"):
    # Create two columns for the form
    col1, col2 = st.columns(2)
    
    with col1:
        target_price = st.number_input(
            "Target Price ($)",
            min_value=0.01,
            value=round(current_price, 2),
            step=0.01,
            format="%.2f"
        )
        
        direction = st.radio(
            "Alert Trigger",
            options=["above", "below"],
            horizontal=True
        )
    
    with col2:
        phone_number = st.text_input(
            "Phone Number",
            placeholder="+1234567890",
            help="Enter your phone number in international format (e.g., +1234567890)"
        )
        
        # Validate phone format
        is_valid_phone = phone_number and validate_phone_number(phone_number)
        if phone_number and not is_valid_phone:
            st.error("Invalid phone number format. Please use international format (e.g., +1234567890)")
    
    # Submit button
    submit_button = st.form_submit_button("Create Alert")
    
    if submit_button:
        if is_valid_phone:
            # Add the alert
            if add_price_alert(stock_symbol, target_price, direction, phone_number):
                st.success(f"Alert created! You will be notified when {stock_symbol} price goes {direction} ${target_price:.2f}.")
            else:
                st.error("Failed to create alert. Please check your inputs and try again.")
        else:
            st.error("Please enter a valid phone number in international format.")

# Display existing alerts
st.subheader("Active Alerts")
indices_to_remove = display_alerts()

# Remove selected alerts
if indices_to_remove:
    remove_button = st.button("Remove Selected Alerts")
    
    if remove_button:
        # Remove alerts in reverse order to avoid index shifting
        for index in sorted(indices_to_remove, reverse=True):
            remove_price_alert(index)
        
        st.success("Selected alerts have been removed.")
        st.rerun()

# Check if any alerts should be triggered
if 'active_alerts' in st.session_state and st.session_state.active_alerts:
    check_button = st.button("Check Alerts Now")
    
    if check_button:
        triggered_alerts, updated_alerts = check_price_alerts(stock_data, st.session_state.active_alerts)
        
        if triggered_alerts:
            st.session_state.active_alerts = updated_alerts
            
            for alert in triggered_alerts:
                if not alert.triggered:  # Avoid sending notifications for already triggered alerts
                    success = send_alert_notification(alert)
                    
                    if success:
                        st.success(f"Alert triggered and notification sent for {alert.stock_symbol} at ${alert.target_price:.2f}!")
                    else:
                        st.warning(f"Alert triggered for {alert.stock_symbol} at ${alert.target_price:.2f}, but notification failed to send.")
        else:
            st.info("No alerts triggered at current price levels.")

# Alert guidelines and FAQ
with st.expander("Alert Guidelines and FAQ"):
    st.markdown("""
    ### Setting Up Price Alerts

    Price alerts notify you when a stock reaches a specified price level. Here's how to use them effectively:

    #### Guidelines
    - **Above Alerts**: Triggered when the stock price moves above your target price
    - **Below Alerts**: Triggered when the stock price moves below your target price
    - **Phone Numbers**: Must be in international format (e.g., +1234567890 for US numbers)
    
    #### How It Works
    1. The system checks your alerts against current price data
    2. When a price condition is met, an in-app notification is displayed
    3. Alerts remain active until removed or triggered
    
    #### Limitations
    - Alerts are checked when you load this page or click "Check Alerts Now"
    - For continuous monitoring, you'll need to keep the application running
    - Notifications are only displayed within the application
    
    #### Troubleshooting
    - Not seeing alerts? Make sure to click "Check Alerts Now" to trigger checks
    - Verify that the alert conditions are reasonable for the stock's price range
    - Currently, we only support in-app notifications (no SMS or email)
    """)

# Alert history (if implemented)
if st.checkbox("Show Alert History"):
    st.info("Alert history feature will be implemented in a future update.")
