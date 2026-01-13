import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_fetcher import get_stock_data, get_available_markets
import plotly.graph_objects as go
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="StockSense - Stock Market Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Zerodha/Grow style design
custom_css = """
<style>
    /* Main color scheme - Blue inspired by Zerodha */
    :root {
        --primary: #3B82F6;
        --primary-dark: #1E40AF;
        --primary-light: #60A5FA;
        --success: #10B981;
        --danger: #EF4444;
        --warning: #F59E0B;
        --dark-bg: #0F1419;
        --card-bg: #1A1F2E;
        --border-color: #2D3748;
        --text-primary: #E5E7EB;
        --text-secondary: #9CA3AF;
    }
    
    /* Custom metric styling */
    [data-testid="metric-container"] {
        background-color: var(--card-bg);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    [data-testid="metric-container"] > div:first-child {
        color: var(--text-secondary);
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="metric-container"] > div:last-child {
        color: var(--text-primary) !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--dark-bg);
    }
    
    /* Button styling */
    button[kind="primary"] {
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="primary"]:hover {
        background-color: var(--primary-light) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Input styling */
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input,
    input[type="text"],
    input[type="number"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }
    
    input::placeholder {
        color: var(--text-secondary) !important;
    }
    
    /* Select box styling */
    [data-testid="stSelectbox"] > div {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: var(--text-primary) !important;
    }
    
    /* Container styling */
    .element-container {
        border-radius: 8px;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 8px;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 8px;
    }
    
    .stInfo {
        background-color: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 8px;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        background-color: var(--card-bg);
        border-radius: 8px;
    }
    
    /* Chart styling */
    .plotly {
        background-color: transparent;
    }
    
    /* Tabs styling */
    [data-testid="stTabs"] button {
        color: var(--text-secondary) !important;
    }
    
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom-color: var(--primary) !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = None
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None
if 'active_alerts' not in st.session_state:
    st.session_state.active_alerts = []

# Header with branding
st.markdown("""
<div style="text-align: center; padding: 20px 0; border-bottom: 1px solid #2D3748;">
    <h1 style="margin: 0; color: #E5E7EB;">📈 StockSense</h1>
    <p style="color: #9CA3AF; margin: 5px 0; font-size: 14px;">Professional Stock Market Analysis Platform</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# Sidebar for global settings
st.sidebar.markdown("## 🔍 Stock Finder")

# Market selection (Global, NSE, BSE)
markets = get_available_markets()
selected_market = st.sidebar.selectbox(
    "Select Market",
    markets,
    help="Choose between Global stocks, NSE (India), or BSE (India)"
)

# Stock symbol input
stock_input = st.sidebar.text_input(
    "Stock Symbol",
    placeholder="e.g., AAPL or RELIANCE.NS",
    help="For NSE stocks, add .NS suffix (e.g., RELIANCE.NS). For BSE stocks, add .BO suffix."
)

# Date range selection
st.sidebar.markdown("### 📅 Date Range")
col1, col2 = st.sidebar.columns(2)
with col1:
    end_date = datetime.now().date()
    start_date = st.date_input(
        "Start Date",
        end_date - timedelta(days=365),
        max_value=end_date,
        label_visibility="collapsed"
    )

with col2:
    end_date = st.date_input(
        "End Date",
        datetime.now().date(),
        min_value=start_date,
        max_value=datetime.now().date(),
        label_visibility="collapsed"
    )

# Fetch data button - prominent styling
st.sidebar.markdown("")
fetch_data = st.sidebar.button(
    "🚀 Fetch Stock Data",
    use_container_width=True,
    key="fetch_button"
)

# Main content
if fetch_data and stock_input:
    try:
        with st.spinner(f"📊 Fetching data for {stock_input}..."):
            stock_data = get_stock_data(stock_input, start_date, end_date)
            st.session_state.stock_data = stock_data
            st.session_state.selected_stock = stock_input
            
            # Display stock information
            if not stock_data.empty:
                current_price = stock_data['Close'].iloc[-1]
                previous_price = stock_data['Close'].iloc[-2] if len(stock_data) > 1 else current_price
                price_change = current_price - previous_price
                price_change_pct = (price_change / previous_price) * 100 if previous_price != 0 else 0
                
                # Modern metrics display
                st.markdown(f"### {stock_input} - Stock Overview")
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    delta_color = "normal" if price_change >= 0 else "inverse"
                    st.metric(
                        "Current Price",
                        f"${current_price:.2f}",
                        delta=f"{price_change:.2f} ({price_change_pct:.2f}%)",
                        delta_color=delta_color
                    )
                
                with metric_col2:
                    st.metric(
                        "Day High",
                        f"${stock_data['High'].iloc[-1]:.2f}"
                    )
                
                with metric_col3:
                    st.metric(
                        "Day Low",
                        f"${stock_data['Low'].iloc[-1]:.2f}"
                    )
                
                with metric_col4:
                    st.metric(
                        "Volume",
                        f"{stock_data['Volume'].iloc[-1]:,.0f}"
                    )
                
                st.markdown("")
                
                # Display candlestick chart with professional styling
                fig = go.Figure(data=[go.Candlestick(
                    x=stock_data.index,
                    open=stock_data['Open'],
                    high=stock_data['High'],
                    low=stock_data['Low'],
                    close=stock_data['Close'],
                    increasing_line_color='#10B981',  # Green
                    decreasing_line_color='#EF4444'   # Red
                )])
                
                fig.update_layout(
                    title=f"{stock_input} - Price Chart",
                    xaxis_title="Date",
                    yaxis_title="Price ($)",
                    height=500,
                    template="plotly_dark",
                    hovermode='x unified',
                    margin=dict(l=0, r=0, t=40, b=0),
                    paper_bgcolor='rgba(26, 31, 46, 1)',
                    plot_bgcolor='rgba(26, 31, 46, 1)',
                    font=dict(color='#E5E7EB', size=12)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Additional statistics in tabs
                tab1, tab2 = st.tabs(["📊 Statistics", "📈 Performance"])
                
                with tab1:
                    stat_col1, stat_col2, stat_col3 = st.columns(3)
                    with stat_col1:
                        st.metric("52-Week High", f"${stock_data['High'].max():.2f}")
                    with stat_col2:
                        st.metric("52-Week Low", f"${stock_data['Low'].min():.2f}")
                    with stat_col3:
                        avg_volume = stock_data['Volume'].mean()
                        st.metric("Avg Volume", f"{avg_volume:,.0f}")
                
                with tab2:
                    period_returns = ((stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[0]) - 1) * 100
                    daily_returns = stock_data['Close'].pct_change() * 100
                    volatility = daily_returns.std()
                    
                    perf_col1, perf_col2, perf_col3 = st.columns(3)
                    with perf_col1:
                        st.metric("Period Return", f"{period_returns:.2f}%")
                    with perf_col2:
                        st.metric("Volatility", f"{volatility:.2f}%")
                    with perf_col3:
                        st.metric("Avg Daily Return", f"{daily_returns.mean():.4f}%")
                
                st.markdown("---")
                st.markdown("### 📋 Recent Price Data")
                
                # Format dataframe nicely
                display_data = stock_data.tail(10).copy()
                st.dataframe(
                    display_data.style.format({
                        'Open': '${:,.2f}',
                        'High': '${:,.2f}',
                        'Low': '${:,.2f}',
                        'Close': '${:,.2f}',
                        'Volume': '{:,.0f}'
                    }),
                    use_container_width=True
                )
                
                st.success(f"✅ Successfully loaded {len(stock_data)} days of data for {stock_input}")
            else:
                st.error("❌ No data returned for the selected stock and date range.")
    except Exception as e:
        error_msg = str(e)
        
        # Detect error type
        is_rate_limit = "rate limit" in error_msg.lower() or "too many requests" in error_msg.lower()
        is_symbol_error = "symbol not found" in error_msg.lower() or "no data" in error_msg.lower()
        is_cooldown = "cooldown" in error_msg.lower()
        
        if is_cooldown:
            st.error("❌ Too Many Attempts - Temporary Cooldown Active")
            st.error(error_msg)
        elif is_rate_limit:
            st.error("❌ API Rate Limit Exceeded")
            st.error(error_msg)
        elif is_symbol_error:
            st.error("❌ Stock Symbol Issue")
            st.error(error_msg)
        else:
            st.error(f"❌ Error fetching stock data")
            st.error(f"Details: {error_msg}")
        
        # Show action items
        if is_rate_limit or is_cooldown:
            st.markdown("""
            ---
            ### ⏳ Next Steps
            
            **Right now:**
            - Try a different stock (AAPL, MSFT, GOOGL, RELIANCE.NS)
            - Browse your previously loaded data
            
            **In a few minutes:**
            - Come back and try the same stock again
            - The API limit will have reset by then
            """)
        elif is_symbol_error:
            st.markdown("""
            ---
            ### 💡 Quick Tips
            - Use working examples above
            - Indian stocks need .NS (NSE) or .BO (BSE) suffix
            - Check spelling carefully
            """)
        else:
            st.markdown("""
            ---
            ### 💡 Troubleshooting
            - Refresh and try again
            - Check your internet connection
            - Try a different stock symbol
            """)
        
elif fetch_data and not stock_input:
    st.warning("⚠️ Please enter a stock symbol in the sidebar first")

elif st.session_state.stock_data is not None:
    # Display previously loaded data
    stock_input = st.session_state.selected_stock
    stock_data = st.session_state.stock_data
    
    current_price = stock_data['Close'].iloc[-1]
    previous_price = stock_data['Close'].iloc[-2] if len(stock_data) > 1 else current_price
    price_change = current_price - previous_price
    price_change_pct = (price_change / previous_price) * 100 if previous_price != 0 else 0
    
    st.markdown(f"### {stock_input} - Stock Overview")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        delta_color = "normal" if price_change >= 0 else "inverse"
        st.metric(
            "Current Price",
            f"${current_price:.2f}",
            delta=f"{price_change:.2f} ({price_change_pct:.2f}%)",
            delta_color=delta_color
        )
    
    with metric_col2:
        st.metric("Day High", f"${stock_data['High'].iloc[-1]:.2f}")
    
    with metric_col3:
        st.metric("Day Low", f"${stock_data['Low'].iloc[-1]:.2f}")
    
    with metric_col4:
        st.metric("Volume", f"{stock_data['Volume'].iloc[-1]:,.0f}")
    
    st.markdown("")
    
    fig = go.Figure(data=[go.Candlestick(
        x=stock_data.index,
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        increasing_line_color='#10B981',
        decreasing_line_color='#EF4444'
    )])
    
    fig.update_layout(
        title=f"{stock_input} - Price Chart",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        height=500,
        template="plotly_dark",
        hovermode='x unified',
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor='rgba(26, 31, 46, 1)',
        plot_bgcolor='rgba(26, 31, 46, 1)',
        font=dict(color='#E5E7EB', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Recent Price Data")
    
    display_data = stock_data.tail(10).copy()
    st.dataframe(
        display_data.style.format({
            'Open': '${:,.2f}',
            'High': '${:,.2f}',
            'Low': '${:,.2f}',
            'Close': '${:,.2f}',
            'Volume': '{:,.0f}'
        }),
        use_container_width=True
    )

else:
    # Welcome screen with instructions
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <h2 style="color: #E5E7EB;">Welcome to StockSense</h2>
        <p style="color: #9CA3AF; font-size: 16px;">
            Your professional stock market analysis platform<br>
            <strong>Get started by entering a stock symbol →</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Example stocks section
    st.markdown("### 🎯 Quick Start Examples")
    
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        st.markdown("""
        **Global Stocks**
        - AAPL (Apple)
        - MSFT (Microsoft)
        - GOOGL (Google)
        - TSLA (Tesla)
        - AMZN (Amazon)
        """)
    
    with example_col2:
        st.markdown("""
        **Indian Stocks (NSE)**
        - RELIANCE.NS (Reliance)
        - TCS.NS (Tata Consultancy)
        - INFY.NS (Infosys)
        - HDFCBANK.NS (HDFC Bank)
        - BHARTIARTL.NS (Bharti Airtel)
        """)
    
    with example_col3:
        st.markdown("""
        **Available Features**
        - 📊 Interactive charts
        - 📈 Technical indicators
        - 🤖 ML predictions
        - 🔔 Price alerts
        - 📋 Historical data
        """)
    
    st.markdown("---")
    
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. **Select Market**: Choose Global, NSE (India), or BSE (India)
    2. **Enter Symbol**: Type the stock symbol (e.g., AAPL)
    3. **Set Dates**: Pick your analysis period
    4. **Fetch Data**: Click the Fetch button to load the data
    5. **Explore**: Navigate to other pages for analysis & predictions
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
### ℹ️ About
**StockSense** combines real-time market data with advanced analytics and machine learning to provide professional-grade stock analysis.

**Data Source:** YFinance API  
**Markets:** Global (US), NSE (India), BSE (India)  
**Features:** Technical Analysis, ML Predictions, Price Alerts

*Last updated: January 13, 2026*
""")
