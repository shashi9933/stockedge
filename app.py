import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_fetcher import get_stock_data, get_available_markets
import plotly.graph_objects as go
import plotly.express as px
from utils.ui_helpers import premium_css

# Set page configuration
st.set_page_config(
    page_title="StockSense - Professional Stock Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global theme
premium_css()

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
    """Create the premium sidebar navigation."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <h1>📈 StockSense</h1>
                <p>Professional Stock Analysis</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-title">Stock Finder</div>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            market = st.selectbox(
                "Market",
                ["US", "NSE", "BSE"],
                key="sidebar_market",
                label_visibility="collapsed",
            )
        with col2:
            symbol = (
                st.text_input(
                    "Symbol",
                    value=st.session_state.selected_symbol,
                    key="sidebar_symbol",
                    label_visibility="collapsed",
                    placeholder="AAPL / RELIANCE.NS",
                )
                .strip()
                .upper()
            )

        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=365),
            key="sidebar_start_date",
            label_visibility="collapsed",
        )

        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            key="sidebar_end_date",
            label_visibility="collapsed",
        )

        if st.button("🔍 Fetch Stock Data", use_container_width=True, key="fetch_btn"):
            st.session_state.selected_symbol = symbol or st.session_state.selected_symbol
            st.session_state.selected_market = market
            st.session_state.page = "chart_analysis"
            if symbol and symbol not in st.session_state.recent_stocks:
                st.session_state.recent_stocks.insert(0, symbol)
                st.session_state.recent_stocks = st.session_state.recent_stocks[:5]
            st.rerun()

        st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)

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

        if st.session_state.recent_stocks:
            st.markdown('<div class="sidebar-title">Recent Stocks</div>', unsafe_allow_html=True)
            for stock in st.session_state.recent_stocks:
                if st.button(f"📌 {stock}", use_container_width=True, key=f"recent_{stock}"):
                    st.session_state.selected_symbol = stock
                    st.session_state.page = "chart_analysis"
                    st.rerun()

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def show_dashboard():
    """Premium dashboard view."""

    # Search + hero
    st.markdown(
        """
        <div class="glass-card" style="margin-bottom: 14px;">
            <div class="section-title" style="margin-bottom: 6px;">Welcome to StockEdge</div>
            <p class="section-subtitle">Your destination for stock market analysis and insights</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_col, search_btn = st.columns([4, 1])
    with search_col:
        hero_symbol = (
            st.text_input(
                "",
                key="hero_search",
                label_visibility="collapsed",
                placeholder="Enter a stock symbol... e.g., AAPL, RELIANCE.NS",
            )
            .strip()
            .upper()
        )
    with search_btn:
        if st.button("Search", use_container_width=True):
            if hero_symbol:
                st.session_state.selected_symbol = hero_symbol
                st.session_state.selected_market = "NSE" if hero_symbol.endswith(".NS") else "US"
                st.session_state.page = "chart_analysis"
                if hero_symbol not in st.session_state.recent_stocks:
                    st.session_state.recent_stocks.insert(0, hero_symbol)
                    st.session_state.recent_stocks = st.session_state.recent_stocks[:5]
                st.rerun()

    hero_col, right_col = st.columns([2.2, 1])

    with hero_col:
        st.markdown(
            """
            <div class="hero-card">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
                    <div>
                        <div class="pill">Market Ready · Realtime & Historical</div>
                        <h2 style="margin:10px 0 6px; font-size:28px;">Welcome to StockEdge</h2>
                        <p style="color:#9fb1d5; margin:0;">Explore stock data, charts, indicators, predictions, alerts, and more.</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Stock Data →", use_container_width=True, key="explore_cta"):
            st.session_state.page = "chart_analysis"
            st.rerun()

        st.markdown("<div class='section-title' style='margin-top:18px;'>Quick Start Examples</div>", unsafe_allow_html=True)
        col_g, col_i = st.columns(2)

        global_examples = [
            ("AAPL", "Apple"),
            ("MSFT", "Microsoft"),
            ("GOOGL", "Google"),
            ("TSLA", "Tesla"),
            ("AMZN", "Amazon"),
        ]
        indian_examples = [
            ("RELIANCE.NS", "Reliance"),
            ("TCS.NS", "Tata Consultancy"),
            ("INFY.NS", "Infosys"),
            ("HDFCBANK.NS", "HDFC Bank"),
            ("AMZN", "Amazon"),
        ]

        def render_example(col, items, market):
            with col:
                for symbol, name in items:
                    if st.button(f"{symbol}", key=f"quick_{symbol}", use_container_width=True):
                        st.session_state.selected_symbol = symbol
                        st.session_state.selected_market = market
                        st.session_state.page = "chart_analysis"
                        if symbol not in st.session_state.recent_stocks:
                            st.session_state.recent_stocks.insert(0, symbol)
                            st.session_state.recent_stocks = st.session_state.recent_stocks[:5]
                        st.rerun()
                    st.caption(name)

        render_example(col_g, global_examples, "US")
        render_example(col_i, indian_examples, "NSE")

        st.markdown("<div class='section-title' style='margin-top:18px;'>How It Works</div>", unsafe_allow_html=True)
        steps = [
            ("Select Market", "Global, NSE (India), or BSE (India)"),
            ("Enter Symbol", "Type the stock symbol or search"),
            ("Set Dates", "Pick your analysis period"),
            ("Fetch Data", "Click Fetch to load the data"),
            ("Explore", "Navigate to other pages for insights"),
        ]
        for idx, (title, desc) in enumerate(steps, 1):
            st.markdown(
                f"""
                <div class="mini-metric" style="margin-bottom:10px;">
                    <div class="pill" style="margin:0;">{idx}</div>
                    <div style="flex:1; margin-left:10px;">
                        <div style="color:#dbe8ff; font-weight:700;">{title}</div>
                        <div style="color:#8fa0c5; font-size:13px;">{desc}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right_col:
        st.markdown(
            """
            <div class="glass-card">
                <div class="section-title" style="margin-bottom:4px;">Stock Finder</div>
                <p class="section-subtitle" style="margin-bottom:12px;">Fetch data quickly</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        finder_market = st.radio(
            "Market",
            ["Global", "NSE", "BSE"],
            index=0 if st.session_state.selected_market == "US" else 1,
            horizontal=True,
        )
        finder_symbol = (
            st.text_input(
                "Enter symbol",
                value=st.session_state.selected_symbol,
                key="finder_symbol",
                placeholder="AAPL / RELIANCE.NS",
            )
            .strip()
            .upper()
        )
        c1, c2 = st.columns(2)
        with c1:
            finder_start = st.date_input("Start", datetime.now() - timedelta(days=90), key="finder_start")
        with c2:
            finder_end = st.date_input("End", datetime.now(), key="finder_end")

        if st.button("Fetch Stock Data", use_container_width=True, key="finder_fetch"):
            st.session_state.selected_symbol = finder_symbol or st.session_state.selected_symbol
            st.session_state.selected_market = "US" if finder_market == "Global" else finder_market
            st.session_state.page = "chart_analysis"
            if finder_symbol and finder_symbol not in st.session_state.recent_stocks:
                st.session_state.recent_stocks.insert(0, finder_symbol)
                st.session_state.recent_stocks = st.session_state.recent_stocks[:5]
            st.rerun()

        st.markdown(
            """
            <div class="glass-card" style="margin-top:12px;">
                <div class="section-title" style="margin-bottom:8px;">Recent Activity</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        recent_list = [
            ("AAPL", "+1.83%", True),
            ("MSFT", "+1.24%", True),
            ("GOOGL", "-0.83%", False),
            ("TCS.NS", "+1.57%", True),
            ("HDFCBANK.NS", "+1.05%", True),
            ("INFY.NS", "+1.05%", True),
        ]
        for sym, change, positive in recent_list:
            st.markdown(
                f"""
                <div class="list-card item">
                    <div>
                        <div class="label">{sym}</div>
                    </div>
                    <div class="{'positive' if positive else 'negative'}">{change}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="glass-card" style="margin-top:14px;">
                <div class="section-title" style="margin-bottom:4px;">Market Overview</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.metric("SENSEX", "72,426.64", "+0.57%")

        st.markdown(
            """
            <div class="glass-card" style="margin-top:14px;">
                <div class="section-title" style="margin-bottom:8px;">Watchlist</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        watchlist = [("TCS", "₹3,012.20", "+1.38%"), ("RELIANCE.NS", "₹3,012.20", "+1.38%")]
        for sym, price, pct in watchlist:
            st.markdown(
                f"""
                <div class="mini-metric" style="margin-bottom:8px;">
                    <div>
                        <div style="color:#dbe8ff; font-weight:700;">{sym}</div>
                        <div style="color:#9fb1d5; font-size:12px;">{price}</div>
                    </div>
                    <div style="color:#6ce2a0; font-weight:700;">{pct}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

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
