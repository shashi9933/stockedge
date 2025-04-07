import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_fetcher import get_stock_data
from utils.chart_helpers import (
    create_candlestick_chart, 
    add_range_selector, 
    add_pivot_points,
    add_annotations
)
from utils.technical_indicators import detect_candlestick_patterns

# Set page configuration
st.set_page_config(
    page_title="Chart Analysis - Stock Market Analysis Platform",
    page_icon="📈",
    layout="wide"
)

st.title("Chart Analysis")
st.markdown("Interactive chart analysis with advanced features.")

# Check if stock data exists in session state
if 'stock_data' not in st.session_state or st.session_state.stock_data is None:
    st.warning("Please select a stock from the home page first.")
    st.stop()

# Get stock data from session state
stock_data = st.session_state.stock_data
stock_symbol = st.session_state.selected_stock

# Chart controls
st.sidebar.header("Chart Settings")

# Chart type selection
chart_type = st.sidebar.selectbox(
    "Chart Type",
    ["Candlestick", "OHLC", "Line"]
)

# Time range selection
time_range = st.sidebar.selectbox(
    "Time Range",
    ["All Data", "1 Month", "3 Months", "6 Months", "1 Year"]
)

# Filter data based on selected time range
end_date = stock_data.index[-1]
if time_range == "1 Month":
    start_date = end_date - timedelta(days=30)
    filtered_data = stock_data[stock_data.index >= start_date]
elif time_range == "3 Months":
    start_date = end_date - timedelta(days=90)
    filtered_data = stock_data[stock_data.index >= start_date]
elif time_range == "6 Months":
    start_date = end_date - timedelta(days=180)
    filtered_data = stock_data[stock_data.index >= start_date]
elif time_range == "1 Year":
    start_date = end_date - timedelta(days=365)
    filtered_data = stock_data[stock_data.index >= start_date]
else:
    filtered_data = stock_data.copy()

# Additional chart features
st.sidebar.subheader("Chart Features")
show_volume = st.sidebar.checkbox("Show Volume", value=True)
show_pivot_points = st.sidebar.checkbox("Show Pivot Points")
detect_patterns = st.sidebar.checkbox("Detect Candlestick Patterns")

# Create chart
if chart_type == "Candlestick":
    fig = create_candlestick_chart(
        filtered_data, 
        title=f"{stock_symbol} - Candlestick Chart",
        show_volume=show_volume
    )
elif chart_type == "OHLC":
    if show_volume:
        fig = go.Figure(
            data=[
                go.Ohlc(
                    x=filtered_data.index,
                    open=filtered_data['Open'],
                    high=filtered_data['High'],
                    low=filtered_data['Low'],
                    close=filtered_data['Close'],
                    name="Price"
                )
            ]
        )
    else:
        fig = go.Figure()
        fig.add_trace(
            go.Ohlc(
                x=filtered_data.index,
                open=filtered_data['Open'],
                high=filtered_data['High'],
                low=filtered_data['Low'],
                close=filtered_data['Close'],
                name="Price"
            )
        )
        
    fig.update_layout(
        title=f"{stock_symbol} - OHLC Chart",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        height=700
    )
else:  # Line chart
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['Close'],
            mode='lines',
            name="Close Price"
        )
    )
    
    fig.update_layout(
        title=f"{stock_symbol} - Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=700
    )
    
    # Add volume if requested
    if show_volume:
        fig = make_subplots(
            rows=2, 
            cols=1, 
            shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.8, 0.2]
        )
        
        # Add price line
        fig.add_trace(
            go.Scatter(
                x=filtered_data.index,
                y=filtered_data['Close'],
                mode='lines',
                name="Close Price"
            ),
            row=1, col=1
        )
        
        # Add volume bars
        colors = ['green' if row['Close'] >= row['Open'] else 'red' for _, row in filtered_data.iterrows()]
        
        fig.add_trace(
            go.Bar(
                x=filtered_data.index,
                y=filtered_data['Volume'],
                marker_color=colors,
                name="Volume"
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title=f"{stock_symbol} - Price Chart",
            template="plotly_white",
            height=700,
            xaxis_rangeslider_visible=False
        )
        
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

# Add range selector
fig = add_range_selector(fig)

# Add pivot points if requested
if show_pivot_points:
    fig = add_pivot_points(fig, filtered_data)

# Detect and display candlestick patterns if requested
if detect_patterns:
    patterns = detect_candlestick_patterns(filtered_data)
    
    # Collect all patterns for annotation
    annotations = []
    for pattern_type, pattern_list in patterns.items():
        for date, label in pattern_list:
            annotations.append((date, label))
    
    # Add annotations to chart
    if annotations:
        fig = add_annotations(fig, filtered_data, annotations)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Display pattern summary if patterns are detected
if detect_patterns:
    st.subheader("Detected Candlestick Patterns")
    
    has_patterns = False
    for pattern_name, pattern_list in patterns.items():
        if pattern_list:
            has_patterns = True
            st.write(f"**{pattern_name.capitalize()} Patterns:**")
            
            pattern_data = []
            for date, label in pattern_list:
                if date in filtered_data.index:
                    pattern_data.append({
                        'Date': date.strftime('%Y-%m-%d'),
                        'Pattern': label,
                        'Price': f"${filtered_data.loc[date, 'Close']:.2f}"
                    })
            
            if pattern_data:
                st.table(pd.DataFrame(pattern_data))
    
    if not has_patterns:
        st.info("No candlestick patterns detected in the selected time range.")

# Chart statistics
st.subheader("Chart Statistics")

# Create columns for statistics
col1, col2, col3 = st.columns(3)

# Calculate statistics
price_change = filtered_data['Close'].iloc[-1] - filtered_data['Close'].iloc[0]
price_change_pct = (price_change / filtered_data['Close'].iloc[0]) * 100

# Display statistics
with col1:
    st.metric(
        "Period Change", 
        f"${price_change:.2f}", 
        f"{price_change_pct:.2f}%"
    )
    st.metric("Highest Price", f"${filtered_data['High'].max():.2f}")
    st.metric("Lowest Price", f"${filtered_data['Low'].min():.2f}")

with col2:
    avg_volume = filtered_data['Volume'].mean()
    st.metric("Average Volume", f"{avg_volume:,.0f}")
    
    avg_daily_change = filtered_data['Close'].pct_change().mean() * 100
    st.metric("Avg. Daily Change", f"{avg_daily_change:.2f}%")
    
    trading_days = len(filtered_data)
    st.metric("Trading Days", f"{trading_days}")

with col3:
    volatility = filtered_data['Close'].pct_change().std() * 100
    st.metric("Volatility (Std. Dev.)", f"{volatility:.2f}%")
    
    price_range = filtered_data['High'].max() - filtered_data['Low'].min()
    price_range_pct = (price_range / filtered_data['Low'].min()) * 100
    st.metric("Price Range", f"${price_range:.2f}", f"{price_range_pct:.2f}%")
    
    current_from_high = (filtered_data['Close'].iloc[-1] - filtered_data['High'].max()) / filtered_data['High'].max() * 100
    st.metric("Current from High", f"{current_from_high:.2f}%")
