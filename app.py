import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_fetcher import get_stock_data, get_available_markets
import plotly.graph_objects as go
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="StockSense - Professional Stock Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium fintech CSS
custom_css = """
<style>
    /* Color Palette */
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
    
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }
    
    /* Main Container */
    .main {
        padding: 0 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0F1419 0%, #1A1F2E 100%) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    /* Navigation Sections */
    .nav-section {
        padding: 20px 15px;
        margin: 10px 0;
        border-radius: 8px;
        background-color: rgba(59, 130, 246, 0.05);
    }
    
    .nav-section-title {
        font-size: 12px;
        font-weight: 700;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
        margin-left: 5px;
    }
    
    /* Dashboard Header */
    .dashboard-header {
        background: linear-gradient(135deg, #1A1F2E 0%, #253549 100%);
        border-bottom: 1px solid var(--border-color);
        padding: 40px;
        border-radius: 12px;
        margin-bottom: 30px;
    }
    
    .dashboard-title {
        font-size: 32px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        margin-bottom: 8px;
    }
    
    .dashboard-subtitle {
        font-size: 16px;
        color: var(--text-secondary);
        margin: 0;
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #1A1F2E 0%, #253549 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: var(--primary);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        color: var(--text-primary);
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-change {
        color: var(--success);
        font-size: 13px;
        font-weight: 600;
        margin-top: 8px;
    }
    
    .metric-change.negative {
        color: var(--danger);
    }
    
    /* Example Stock Cards */
    .stock-example-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 16px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .stock-example-card:hover {
        border-color: var(--primary);
        background-color: rgba(59, 130, 246, 0.05);
    }
    
    .stock-symbol {
        font-size: 16px;
        font-weight: 700;
        color: var(--primary);
        margin: 0;
    }
    
    .stock-name {
        font-size: 12px;
        color: var(--text-secondary);
        margin: 4px 0 0 0;
    }
    
    /* Buttons */
    button[kind="primary"] {
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="primary"]:hover {
        background-color: var(--primary-light) !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    .cta-button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        color: white;
        padding: 16px 32px;
        font-size: 16px;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .cta-button:hover {
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    
    /* Input Fields */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    input[type="text"],
    input[type="number"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 14px !important;
    }
    
    input::placeholder {
        color: var(--text-secondary) !important;
    }
    
    input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Select Boxes */
    [data-testid="stSelectbox"] > div {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: var(--text-primary);
        margin-top: 30px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--primary);
    }
    
    /* How It Works Steps */
    .how-it-works-step {
        display: flex;
        gap: 16px;
        margin-bottom: 20px;
    }
    
    .step-number {
        background-color: var(--primary);
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        flex-shrink: 0;
    }
    
    .step-content h4 {
        color: var(--text-primary);
        margin: 0 0 4px 0;
        font-size: 14px;
    }
    
    .step-content p {
        color: var(--text-secondary);
        margin: 0;
        font-size: 13px;
    }
    
    /* Metric Container */
    [data-testid="metric-container"] {
        background-color: var(--card-bg);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    [data-testid="metric-container"] > div:first-child {
        color: var(--text-secondary);
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="metric-container"] > div:last-child {
        color: var(--text-primary) !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }
    
    /* Recent Activity */
    .activity-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px;
        border-bottom: 1px solid var(--border-color);
    }
    
    .activity-item:last-child {
        border-bottom: none;
    }
    
    .activity-symbol {
        font-weight: 700;
        color: var(--primary);
    }
    
    .activity-change {
        color: var(--success);
        font-weight: 600;
    }
    
    .activity-change.negative {
        color: var(--danger);
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'selected_symbol' not in st.session_state:
    st.session_state.selected_symbol = 'AAPL'
if 'selected_market' not in st.session_state:
    st.session_state.selected_market = 'US'
if 'recent_stocks' not in st.session_state:
    st.session_state.recent_stocks = []

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
def create_sidebar():
    """Create the premium sidebar navigation"""
    with st.sidebar:
        # Logo/Brand
        st.markdown("""
        <div style="padding: 20px 0; text-align: center;">
            <h1 style="font-size: 24px; margin: 0; color: #3B82F6;">📈 StockSense</h1>
            <p style="color: #9CA3AF; margin: 4px 0 0 0; font-size: 12px;">Professional Stock Analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Stock Finder - Sticky Section
        st.markdown('<div class="nav-section"><div class="nav-section-title">Quick Access</div></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            market = st.selectbox(
                "Market",
                ["US", "NSE", "BSE"],
                key="sidebar_market",
                label_visibility="collapsed"
            )
        with col2:
            symbol = st.text_input(
                "Symbol",
                value=st.session_state.selected_symbol,
                key="sidebar_symbol",
                label_visibility="collapsed",
                placeholder="e.g., AAPL"
            ).upper()
        
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=365),
            key="sidebar_start_date",
            label_visibility="collapsed"
        )
        
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            key="sidebar_end_date",
            label_visibility="collapsed"
        )
        
        if st.button("🔍 Fetch Stock Data", use_container_width=True, key="fetch_btn"):
            st.session_state.selected_symbol = symbol
            st.session_state.selected_market = market
            st.session_state.page = 'chart_analysis'
            if symbol not in st.session_state.recent_stocks:
                st.session_state.recent_stocks.insert(0, symbol)
                st.session_state.recent_stocks = st.session_state.recent_stocks[:5]
            st.rerun()
        
        st.divider()
        
        # Navigation Menu
        st.markdown('<div class="nav-section-title">Navigation</div>', unsafe_allow_html=True)
        
        nav_items = [
            ("🏠 Dashboard", "dashboard"),
            ("📊 Chart Analysis", "chart_analysis"),
            ("📈 Technical Indicators", "technical_indicators"),
            ("🤖 Prediction Models", "prediction_models"),
            ("🔔 Price Alerts", "price_alerts"),
            ("💰 Financial Metrics", "financial_metrics"),
            ("🏢 Company Info", "company_info"),
            ("👥 Shareholding", "shareholding"),
            ("🔗 Peers", "peers"),
        ]
        
        for label, page_name in nav_items:
            if st.button(label, use_container_width=True, key=f"nav_{page_name}"):
                st.session_state.page = page_name
                st.rerun()
        
        st.divider()
        
        # Recent Activity
        if st.session_state.recent_stocks:
            st.markdown('<div class="nav-section-title">Recent Stocks</div>', unsafe_allow_html=True)
            for stock in st.session_state.recent_stocks:
                if st.button(f"📌 {stock}", use_container_width=True, key=f"recent_{stock}"):
                    st.session_state.selected_symbol = stock
                    st.session_state.page = 'chart_analysis'
                    st.rerun()
        
        st.divider()
        
        # Settings
        st.markdown('<div class="nav-section-title">Settings</div>', unsafe_allow_html=True)
        if st.button("⚙️ Settings", use_container_width=True):
            st.info("Settings coming soon!")
        if st.button("📚 Help & Documentation", use_container_width=True):
            st.info("Documentation coming soon!")

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def show_dashboard():
    """Premium dashboard view"""
    
    # Header
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">Welcome Back</h1>
        <p class="dashboard-subtitle">Your destination for stock market analysis and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Section
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%); 
                    padding: 30px; border-radius: 12px; color: white;">
            <h3 style="margin: 0 0 12px 0; font-size: 20px;">Start Your Analysis</h3>
            <p style="margin: 0; color: rgba(255,255,255,0.9); font-size: 14px;">
                Search for any stock symbol, analyze charts, and get insights in seconds.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick Examples Section
    st.markdown('<h2 class="section-header">Popular Stocks</h2>', unsafe_allow_html=True)
    
    st.markdown('<h4 style="color: #9CA3AF; font-size: 13px; text-transform: uppercase; margin: 20px 0 10px 0;">Global Stocks</h4>', 
                unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    global_stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
    
    for col, stock in zip([col1, col2, col3, col4, col5], global_stocks):
        with col:
            if st.button(stock, use_container_width=True, key=f"stock_{stock}"):
                st.session_state.selected_symbol = stock
                st.session_state.selected_market = "US"
                st.session_state.page = 'chart_analysis'
                st.rerun()
            st.caption(stock.lower())
    
    st.markdown('<h4 style="color: #9CA3AF; font-size: 13px; text-transform: uppercase; margin: 20px 0 10px 0;">Indian Stocks (NSE)</h4>', 
                unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    indian_stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "WIPRO.NS"]
    
    for col, stock in zip([col1, col2, col3, col4, col5], indian_stocks):
        with col:
            if st.button(stock, use_container_width=True, key=f"stock_{stock}"):
                st.session_state.selected_symbol = stock
                st.session_state.selected_market = "NSE"
                st.session_state.page = 'chart_analysis'
                st.rerun()
            st.caption(stock.lower())
    
    st.divider()
    
    # How It Works Section
    st.markdown('<h2 class="section-header">How It Works</h2>', unsafe_allow_html=True)
    
    steps = [
        ("Select Market", "Choose between US, NSE (India National), or BSE (India Bombay) markets"),
        ("Enter Symbol", "Type the stock symbol (e.g., AAPL, RELIANCE.NS) or search from our database"),
        ("Set Date Range", "Pick your analysis timeframe—days, months, or years of historical data"),
        ("Fetch Data", "Click 'Fetch Stock Data' to retrieve real-time and historical prices"),
        ("Explore Analysis", "Dive into charts, technical indicators, predictions, and company metrics"),
    ]
    
    for i, (title, desc) in enumerate(steps, 1):
        col1, col2 = st.columns([0.08, 0.92])
        with col1:
            st.markdown(f'<div class="step-number">{i}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<h4 style="color: #E5E7EB; margin: 0 0 4px 0;">{title}</h4>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #9CA3AF; margin: 0; font-size: 14px;">{desc}</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # Market Status Section
    st.markdown('<h2 class="section-header">Market Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("US Market", "Open", "+2.5%")
    with col2:
        st.metric("NSE Index", "SENSEX", "+1.8%")
    with col3:
        st.metric("Top Gainer", "AAPL", "+5.2%")
    with col4:
        st.metric("Most Active", "RELIANCE.NS", "₹3.2M")

# ============================================================================
# MAIN APP FLOW
# ============================================================================
def main():
    create_sidebar()
    
    # Route to the selected page
    if st.session_state.page == 'dashboard':
        show_dashboard()
    elif st.session_state.page == 'chart_analysis':
        st.switch_page("pages/1_Chart_Analysis.py")
    elif st.session_state.page == 'technical_indicators':
        st.switch_page("pages/2_Technical_Indicators.py")
    elif st.session_state.page == 'prediction_models':
        st.switch_page("pages/3_Prediction_Models.py")
    elif st.session_state.page == 'price_alerts':
        st.switch_page("pages/4_Price_Alerts.py")
    elif st.session_state.page == 'financial_metrics':
        st.switch_page("pages/5_Financial_Metrics.py")
    elif st.session_state.page == 'company_info':
        st.switch_page("pages/6_Company_Info.py")
    elif st.session_state.page == 'shareholding':
        st.switch_page("pages/7_Shareholding.py")
    elif st.session_state.page == 'peers':
        st.switch_page("pages/8_Peers.py")

if __name__ == "__main__":
    main()
