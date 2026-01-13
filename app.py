import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_fetcher import get_stock_data, get_available_markets
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Stock Market Analysis Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = None
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None
if 'active_alerts' not in st.session_state:
    st.session_state.active_alerts = []

# Add a title and description
st.title("Stock Market Analysis Platform")
st.markdown("""
This platform combines advanced data analysis techniques, multiple prediction models, 
and interactive visualization to provide comprehensive financial insights for both 
Indian and global markets.
""")

# Sidebar for global settings
st.sidebar.header("Stock Selection")

# Market selection (Global, NSE, BSE)
markets = get_available_markets()
selected_market = st.sidebar.selectbox("Select Market", markets)

# Stock symbol input
stock_input = st.sidebar.text_input(
    "Enter Stock Symbol", 
    help="For NSE stocks, add .NS suffix (e.g., RELIANCE.NS). For BSE stocks, add .BO suffix."
)

# Date range selection
st.sidebar.subheader("Date Range")
end_date = datetime.now().date()
start_date = st.sidebar.date_input(
    "Start Date",
    end_date - timedelta(days=365),
    max_value=end_date
)
end_date = st.sidebar.date_input(
    "End Date",
    end_date,
    min_value=start_date,
    max_value=end_date
)

# Fetch data button
fetch_data = st.sidebar.button("Fetch Stock Data")

# Main content
if fetch_data and stock_input:
    try:
        with st.spinner(f"Fetching data for {stock_input}..."):
            stock_data = get_stock_data(stock_input, start_date, end_date)
            st.session_state.stock_data = stock_data
            st.session_state.selected_stock = stock_input
            
            # Display basic stock information
            if not stock_data.empty:
                current_price = stock_data['Close'].iloc[-1]
                previous_price = stock_data['Close'].iloc[-2] if len(stock_data) > 1 else current_price
                price_change = current_price - previous_price
                price_change_pct = (price_change / previous_price) * 100 if previous_price != 0 else 0
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Current Price", f"${current_price:.2f}", f"{price_change:.2f} ({price_change_pct:.2f}%)")
                col2.metric("Volume", f"{stock_data['Volume'].iloc[-1]:,}")
                col3.metric("52-Week Range", f"${stock_data['Low'].min():.2f} - ${stock_data['High'].max():.2f}")
                
                # Display a simple candlestick chart on the home page
                fig = go.Figure(data=[go.Candlestick(
                    x=stock_data.index,
                    open=stock_data['Open'],
                    high=stock_data['High'],
                    low=stock_data['Low'],
                    close=stock_data['Close'],
                    name='Price'
                )])
                
                fig.update_layout(
                    title=f"{stock_input} Stock Price",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    height=600,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display last 5 days of data
                st.subheader("Recent Price Data")
                st.dataframe(stock_data.tail().style.format({
                    'Open': "${:.2f}",
                    'High': "${:.2f}",
                    'Low': "${:.2f}",
                    'Close': "${:.2f}",
                    'Volume': "{:,.0f}"
                }))
                
                st.success(f"✅ Successfully loaded data for {stock_input}")
            else:
                st.error("❌ No data returned for the selected stock and date range.")
    except Exception as e:
        error_msg = str(e)
        st.error(f"❌ Error fetching stock data: {error_msg}")
        
        # Provide helpful suggestions based on error type
        st.info(
            "**Troubleshooting Tips:**\n"
            "• **Correct the symbol**: Check if the stock symbol is spelled correctly\n"
            "• **For Indian stocks**: Add suffix .NS (NSE) or .BO (BSE)\n"
            "  - Example: RELIANCE.NS or TCS.NS\n"
            "• **Try different dates**: The selected date range might not have data\n"
            "• **Check symbol format**: Some symbols may be different (e.g., BRK.B instead of BRK)\n"
            "• **Network issues**: Try again in a moment if you see connection errors"
        )
elif fetch_data and not stock_input:
    st.warning("⚠️ Please enter a stock symbol first")
elif st.session_state.stock_data is not None:
    # Display previously loaded data
    stock_input = st.session_state.selected_stock
    stock_data = st.session_state.stock_data
    
    current_price = stock_data['Close'].iloc[-1]
    previous_price = stock_data['Close'].iloc[-2] if len(stock_data) > 1 else current_price
    price_change = current_price - previous_price
    price_change_pct = (price_change / previous_price) * 100 if previous_price != 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${current_price:.2f}", f"{price_change:.2f} ({price_change_pct:.2f}%)")
    col2.metric("Volume", f"{stock_data['Volume'].iloc[-1]:,}")
    col3.metric("52-Week Range", f"${stock_data['Low'].min():.2f} - ${stock_data['High'].max():.2f}")
    
    # Display a simple candlestick chart on the home page
    fig = go.Figure(data=[go.Candlestick(
        x=stock_data.index,
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name='Price'
    )])
    
    fig.update_layout(
        title=f"{stock_input} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price",
        height=600,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display last 5 days of data
    st.subheader("Recent Price Data")
    st.dataframe(stock_data.tail().style.format({
        'Open': "${:.2f}",
        'High': "${:.2f}",
        'Low': "${:.2f}",
        'Close': "${:.2f}",
        'Volume': "{:,.0f}"
    }))
else:
    # Display instructions
    st.info("👈 Enter a stock symbol in the sidebar to begin your analysis.")
    st.markdown("""
    ### Getting Started
    1. Select a market (Global, NSE, BSE)
    2. Enter a stock symbol (e.g., AAPL for Apple, RELIANCE.NS for Reliance Industries on NSE)
    3. Choose a date range for analysis
    4. Click 'Fetch Stock Data' to load the data
    
    ### Features Available
    - **Chart Analysis**: Interactive candlestick charts with zoom/pan capabilities
    - **Technical Indicators**: SMA, RSI, Bollinger Bands and more
    - **Prediction Models**: Multiple models with ensemble approach
    - **Price Alerts**: Set custom alerts for price movements
    """)

st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.info(
    """
    This platform combines advanced data analysis techniques, multiple prediction models, 
    and interactive visualization for informed trading decisions.
    """
)
