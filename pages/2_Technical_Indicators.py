import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.technical_indicators import (
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_bollinger_bands,
    calculate_macd,
    calculate_support_resistance,
    plot_with_indicators
)

# Set page configuration
st.set_page_config(
    page_title="Technical Indicators - Stock Market Analysis Platform",
    page_icon="📈",
    layout="wide"
)

st.title("Technical Indicators")
st.markdown("Analyze stock data with various technical indicators.")

# Check if stock data exists in session state
if 'stock_data' not in st.session_state or st.session_state.stock_data is None:
    st.warning("Please select a stock from the home page first.")
    st.stop()

# Get stock data from session state
stock_data = st.session_state.stock_data
stock_symbol = st.session_state.selected_stock

# Sidebar controls
st.sidebar.header("Indicator Settings")

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

# Indicator selection
st.sidebar.subheader("Select Indicators")
show_sma = st.sidebar.checkbox("Moving Averages (SMA)", value=True)
show_bollinger = st.sidebar.checkbox("Bollinger Bands")
show_rsi = st.sidebar.checkbox("Relative Strength Index (RSI)")
show_macd = st.sidebar.checkbox("MACD")
show_support_resistance = st.sidebar.checkbox("Support & Resistance")

# Create list of selected indicators
selected_indicators = []
if show_sma:
    selected_indicators.append("SMA")
if show_bollinger:
    selected_indicators.append("Bollinger Bands")
if show_rsi:
    selected_indicators.append("RSI")
if show_macd:
    selected_indicators.append("MACD")
if show_support_resistance:
    selected_indicators.append("Support/Resistance")

# Display chart with selected indicators
if selected_indicators:
    fig = plot_with_indicators(filtered_data, selected_indicators)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please select at least one technical indicator from the sidebar.")

# Technical analysis descriptions and insights
st.subheader("Technical Analysis Insights")

# Create tabs for different indicator types
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Moving Averages", 
    "Bollinger Bands", 
    "RSI", 
    "MACD",
    "Support & Resistance"
])

with tab1:
    st.markdown("### Moving Averages Analysis")
    
    # Calculate different SMAs
    sma_20 = calculate_sma(filtered_data, window=20)
    sma_50 = calculate_sma(filtered_data, window=50)
    sma_200 = calculate_sma(filtered_data, window=200)
    
    # Current price relative to SMAs
    current_price = filtered_data['Close'].iloc[-1]
    
    # Create columns for SMA metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if len(sma_20) > 0:
            sma20_value = sma_20.iloc[-1]
            sma20_diff = ((current_price / sma20_value) - 1) * 100
            st.metric("20-Day SMA", f"${sma20_value:.2f}", f"{sma20_diff:.2f}%")
        else:
            st.metric("20-Day SMA", "Insufficient data")
    
    with col2:
        if len(sma_50) > 0:
            sma50_value = sma_50.iloc[-1]
            sma50_diff = ((current_price / sma50_value) - 1) * 100
            st.metric("50-Day SMA", f"${sma50_value:.2f}", f"{sma50_diff:.2f}%")
        else:
            st.metric("50-Day SMA", "Insufficient data")
    
    with col3:
        if len(sma_200) > 0:
            sma200_value = sma_200.iloc[-1]
            sma200_diff = ((current_price / sma200_value) - 1) * 100
            st.metric("200-Day SMA", f"${sma200_value:.2f}", f"{sma200_diff:.2f}%")
        else:
            st.metric("200-Day SMA", "Insufficient data")
    
    # SMA crossover analysis
    st.markdown("#### SMA Crossover Analysis")
    
    if len(sma_20) > 0 and len(sma_50) > 0:
        # Check for recent crossovers
        crossovers = []
        for i in range(1, len(sma_20)):
            if sma_20.iloc[i-1] < sma_50.iloc[i-1] and sma_20.iloc[i] >= sma_50.iloc[i]:
                crossovers.append(("Golden Cross", sma_20.index[i], "Bullish signal where 20-day SMA crosses above 50-day SMA"))
            elif sma_20.iloc[i-1] > sma_50.iloc[i-1] and sma_20.iloc[i] <= sma_50.iloc[i]:
                crossovers.append(("Death Cross", sma_20.index[i], "Bearish signal where 20-day SMA crosses below 50-day SMA"))
        
        if crossovers:
            crossover_data = []
            for signal, date, desc in crossovers:
                crossover_data.append({
                    "Signal": signal,
                    "Date": date.strftime('%Y-%m-%d'),
                    "Description": desc
                })
            
            st.table(pd.DataFrame(crossover_data))
        else:
            st.info("No SMA crossovers detected in the selected time range.")
    else:
        st.info("Insufficient data for SMA crossover analysis.")

with tab2:
    st.markdown("### Bollinger Bands Analysis")
    
    # Calculate Bollinger Bands
    upper_band, middle_band, lower_band = calculate_bollinger_bands(filtered_data)
    
    # Create metrics
    current_price = filtered_data['Close'].iloc[-1]
    
    if len(upper_band) > 0 and len(lower_band) > 0:
        upper_value = upper_band.iloc[-1]
        middle_value = middle_band.iloc[-1]
        lower_value = lower_band.iloc[-1]
        
        # Calculate bandwidth and %B
        bandwidth = (upper_value - lower_value) / middle_value * 100
        percent_b = (current_price - lower_value) / (upper_value - lower_value) if upper_value != lower_value else 0.5
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Bollinger Bandwidth", f"{bandwidth:.2f}%")
            st.metric("Upper Band", f"${upper_value:.2f}")
            st.metric("Lower Band", f"${lower_value:.2f}")
        
        with col2:
            st.metric("%B (Position within Bands)", f"{percent_b:.2f}")
            st.metric("Middle Band (20-day SMA)", f"${middle_value:.2f}")
            
            # Band penetration status
            if current_price > upper_value:
                st.info("📈 Price is above upper band (potentially overbought)")
            elif current_price < lower_value:
                st.info("📉 Price is below lower band (potentially oversold)")
            else:
                st.info("🔄 Price is within the bands")
        
        # Volatility analysis
        st.markdown("#### Volatility Analysis")
        
        # Calculate recent bandwidth trend
        recent_bandwidth = [(upper_band.iloc[i] - lower_band.iloc[i]) / middle_band.iloc[i] * 100 
                          for i in range(-10, 0)]
        
        bandwidth_trend = "increasing" if recent_bandwidth[-1] > recent_bandwidth[0] else "decreasing"
        
        st.write(f"Volatility is **{bandwidth_trend}** based on recent Bollinger Bandwidth trend.")
        
        if bandwidth_trend == "decreasing" and bandwidth < 20:
            st.write("📊 Low and decreasing bandwidth suggests a potential breakout may be coming soon.")
        elif bandwidth_trend == "increasing" and bandwidth > 40:
            st.write("📊 High and increasing bandwidth indicates strong market movement and trend continuation.")
    else:
        st.info("Insufficient data for Bollinger Bands analysis.")

with tab3:
    st.markdown("### Relative Strength Index (RSI) Analysis")
    
    # Calculate RSI
    rsi = calculate_rsi(filtered_data)
    
    if len(rsi) > 0:
        current_rsi = rsi.iloc[-1]
        
        # RSI conditions
        if current_rsi > 70:
            condition = "Overbought"
            description = "The stock may be overbought and could be due for a pullback."
            signal = "Potential sell signal"
        elif current_rsi < 30:
            condition = "Oversold"
            description = "The stock may be oversold and could be due for a bounce."
            signal = "Potential buy signal"
        else:
            condition = "Neutral"
            description = "RSI is in the neutral zone."
            signal = "No clear signal"
        
        # Create metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Current RSI", f"{current_rsi:.2f}")
            st.metric("Condition", condition)
        
        with col2:
            st.metric("Signal", signal)
            
            # RSI trend
            rsi_5days_ago = rsi.iloc[-6] if len(rsi) > 5 else rsi.iloc[0]
            rsi_diff = current_rsi - rsi_5days_ago
            
            if abs(rsi_diff) > 0.1:
                trend = "Rising" if rsi_diff > 0 else "Falling"
                st.metric("5-Day RSI Trend", trend, f"{rsi_diff:.2f}")
            else:
                st.metric("5-Day RSI Trend", "Flat", f"{rsi_diff:.2f}")
        
        st.write(description)
        
        # RSI divergence analysis
        st.markdown("#### RSI Divergence Analysis")
        
        # Check for bullish and bearish divergences
        price_lows = []
        rsi_lows = []
        price_highs = []
        rsi_highs = []
        
        # Find local minima and maxima
        for i in range(5, len(rsi) - 5):
            # Check for price local minimum
            if all(filtered_data['Low'].iloc[i] <= filtered_data['Low'].iloc[i-j] for j in range(1, 6)) and \
               all(filtered_data['Low'].iloc[i] <= filtered_data['Low'].iloc[i+j] for j in range(1, 6)):
                price_lows.append((filtered_data.index[i], filtered_data['Low'].iloc[i], rsi.iloc[i]))
            
            # Check for RSI local minimum
            if all(rsi.iloc[i] <= rsi.iloc[i-j] for j in range(1, 6)) and \
               all(rsi.iloc[i] <= rsi.iloc[i+j] for j in range(1, 6)):
                rsi_lows.append((filtered_data.index[i], filtered_data['Low'].iloc[i], rsi.iloc[i]))
            
            # Check for price local maximum
            if all(filtered_data['High'].iloc[i] >= filtered_data['High'].iloc[i-j] for j in range(1, 6)) and \
               all(filtered_data['High'].iloc[i] >= filtered_data['High'].iloc[i+j] for j in range(1, 6)):
                price_highs.append((filtered_data.index[i], filtered_data['High'].iloc[i], rsi.iloc[i]))
            
            # Check for RSI local maximum
            if all(rsi.iloc[i] >= rsi.iloc[i-j] for j in range(1, 6)) and \
               all(rsi.iloc[i] >= rsi.iloc[i+j] for j in range(1, 6)):
                rsi_highs.append((filtered_data.index[i], filtered_data['High'].iloc[i], rsi.iloc[i]))
        
        # Check for bullish divergence (price makes lower low, RSI makes higher low)
        bullish_divergences = []
        if len(price_lows) >= 2 and len(rsi_lows) >= 2:
            for i in range(len(price_lows) - 1):
                if price_lows[i][1] > price_lows[i+1][1] and price_lows[i][2] < price_lows[i+1][2]:
                    bullish_divergences.append((price_lows[i+1][0], "Bullish Divergence"))
        
        # Check for bearish divergence (price makes higher high, RSI makes lower high)
        bearish_divergences = []
        if len(price_highs) >= 2 and len(rsi_highs) >= 2:
            for i in range(len(price_highs) - 1):
                if price_highs[i][1] < price_highs[i+1][1] and price_highs[i][2] > price_highs[i+1][2]:
                    bearish_divergences.append((price_highs[i+1][0], "Bearish Divergence"))
        
        # Display divergences
        if bullish_divergences or bearish_divergences:
            divergence_data = []
            
            for date, div_type in bullish_divergences + bearish_divergences:
                divergence_data.append({
                    "Date": date.strftime('%Y-%m-%d'),
                    "Type": div_type,
                    "Signal": "Potential bullish reversal" if div_type == "Bullish Divergence" else "Potential bearish reversal"
                })
            
            st.table(pd.DataFrame(divergence_data))
        else:
            st.info("No clear RSI divergences detected in the selected time range.")
    else:
        st.info("Insufficient data for RSI analysis.")

with tab4:
    st.markdown("### MACD Analysis")
    
    # Calculate MACD
    macd_line, signal_line, histogram = calculate_macd(filtered_data)
    
    if len(macd_line) > 0 and len(signal_line) > 0:
        current_macd = macd_line.iloc[-1]
        current_signal = signal_line.iloc[-1]
        current_histogram = histogram.iloc[-1]
        
        # Determine MACD status
        if current_macd > current_signal:
            if current_macd > 0:
                status = "Strong Bullish"
                description = "MACD is above signal line and zero line, indicating strong bullish momentum."
            else:
                status = "Weak Bullish"
                description = "MACD is above signal line but below zero line, indicating improving momentum but still negative."
        else:
            if current_macd < 0:
                status = "Strong Bearish"
                description = "MACD is below signal line and zero line, indicating strong bearish momentum."
            else:
                status = "Weak Bearish"
                description = "MACD is below signal line but above zero line, indicating weakening momentum but still positive."
        
        # Check for recent crossovers
        crossovers = []
        for i in range(1, len(macd_line)):
            if macd_line.iloc[i-1] < signal_line.iloc[i-1] and macd_line.iloc[i] >= signal_line.iloc[i]:
                crossovers.append((macd_line.index[i], "Bullish Crossover"))
            elif macd_line.iloc[i-1] > signal_line.iloc[i-1] and macd_line.iloc[i] <= signal_line.iloc[i]:
                crossovers.append((macd_line.index[i], "Bearish Crossover"))
        
        # Create metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("MACD Line", f"{current_macd:.4f}")
            st.metric("Signal Line", f"{current_signal:.4f}")
            st.metric("Histogram", f"{current_histogram:.4f}")
        
        with col2:
            st.metric("Status", status)
            
            # Histogram trend
            if len(histogram) > 5:
                histogram_5days_ago = histogram.iloc[-6]
                histogram_diff = current_histogram - histogram_5days_ago
                
                if histogram_diff > 0:
                    hist_trend = "Strengthening" if current_histogram > 0 else "Improving"
                else:
                    hist_trend = "Weakening" if current_histogram > 0 else "Worsening"
                
                st.metric("Momentum Trend", hist_trend, f"{histogram_diff:.4f}")
            else:
                st.metric("Momentum Trend", "Insufficient data")
        
        st.write(description)
        
        # Display recent crossovers
        st.markdown("#### Recent MACD Crossovers")
        
        if crossovers:
            crossover_data = []
            
            for date, cross_type in crossovers:
                crossover_data.append({
                    "Date": date.strftime('%Y-%m-%d'),
                    "Type": cross_type,
                    "Signal": "Buy signal" if cross_type == "Bullish Crossover" else "Sell signal"
                })
            
            st.table(pd.DataFrame(crossover_data).tail(5))
        else:
            st.info("No MACD crossovers detected in the selected time range.")
    else:
        st.info("Insufficient data for MACD analysis.")

with tab5:
    st.markdown("### Support & Resistance Analysis")
    
    # Calculate support and resistance levels
    support_levels, resistance_levels = calculate_support_resistance(filtered_data)
    
    if support_levels or resistance_levels:
        # Sort levels by price
        support_levels.sort(key=lambda x: x[1])
        resistance_levels.sort(key=lambda x: x[1])
        
        # Get current price
        current_price = filtered_data['Close'].iloc[-1]
        
        # Find nearest support and resistance
        nearest_support = None
        for date, level in reversed(support_levels):
            if level < current_price:
                nearest_support = (date, level)
                break
        
        nearest_resistance = None
        for date, level in support_levels:
            if level > current_price:
                nearest_resistance = (date, level)
                break
        
        # Create columns for display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Support Levels")
            
            if support_levels:
                support_data = []
                
                for date, level in support_levels:
                    distance = ((level / current_price) - 1) * 100
                    strength = "Strong" if abs(distance) < 5 else "Moderate"
                    
                    support_data.append({
                        "Price": f"${level:.2f}",
                        "Distance": f"{distance:.2f}%",
                        "Strength": strength
                    })
                
                st.table(pd.DataFrame(support_data))
            else:
                st.info("No support levels detected.")
        
        with col2:
            st.markdown("#### Resistance Levels")
            
            if resistance_levels:
                resistance_data = []
                
                for date, level in resistance_levels:
                    distance = ((level / current_price) - 1) * 100
                    strength = "Strong" if abs(distance) < 5 else "Moderate"
                    
                    resistance_data.append({
                        "Price": f"${level:.2f}",
                        "Distance": f"{distance:.2f}%",
                        "Strength": strength
                    })
                
                st.table(pd.DataFrame(resistance_data))
            else:
                st.info("No resistance levels detected.")
        
        # Display analysis insights
        st.markdown("#### Price Position Analysis")
        
        if nearest_support and nearest_resistance:
            # Calculate distance to nearest support and resistance
            support_distance = ((current_price / nearest_support[1]) - 1) * 100
            resistance_distance = ((nearest_resistance[1] / current_price) - 1) * 100
            
            # Calculate relative position between support and resistance
            range_size = nearest_resistance[1] - nearest_support[1]
            position_in_range = (current_price - nearest_support[1]) / range_size if range_size > 0 else 0.5
            
            # Display metrics
            st.metric("Position in Range", f"{position_in_range:.2f} (0=support, 1=resistance)")
            
            # Trading range analysis
            if position_in_range < 0.3:
                st.info("📈 Price is near support level, potential buying zone.")
            elif position_in_range > 0.7:
                st.info("📉 Price is near resistance level, potential selling/caution zone.")
            else:
                st.info("🔄 Price is in the middle of the range, no clear edge.")
        else:
            if nearest_support:
                support_distance = ((current_price / nearest_support[1]) - 1) * 100
                st.info(f"📊 No clear resistance detected. Nearest support is ${nearest_support[1]:.2f} ({support_distance:.2f}% below current price).")
            elif nearest_resistance:
                resistance_distance = ((nearest_resistance[1] / current_price) - 1) * 100
                st.info(f"📊 No clear support detected. Nearest resistance is ${nearest_resistance[1]:.2f} ({resistance_distance:.2f}% above current price).")
            else:
                st.info("📊 No clear support or resistance levels detected.")
    else:
        st.info("Insufficient data to calculate support and resistance levels.")
