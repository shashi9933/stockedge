import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from utils.data_fetcher import (get_stock_data, get_stock_info, 
                                 get_income_statement, get_balance_sheet, 
                                 get_cash_flow, get_company_overview, get_earnings)
from utils.ui_helpers import page_header, premium_css

st.set_page_config(
    page_title="Financial Metrics - StockSense",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

premium_css()
page_header("Financial Metrics", "Detailed financial analysis & statements", "💰")

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 12px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-change {
        font-size: 14px;
        margin-top: 8px;
    }
    
    .positive {
        color: #10B981;
    }
    
    .negative {
        color: #EF4444;
    }
    
    .financial-table {
        font-size: 13px;
    }
    
    .section-header {
        color: #3B82F6;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 10px;
        margin: 30px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Financial Metrics & Analysis")

# Sidebar for stock selection
with st.sidebar:
    st.header("Stock Selection")
    stock_symbol = st.text_input(
        "Enter Stock Symbol",
        value="AAPL",
        help="e.g., AAPL, RELIANCE.NS, INFY.NS"
    ).strip().upper()
    
    analysis_type = st.radio(
        "Analysis Type",
        ["Key Metrics", "Financial Statements", "Ratios", "Growth Analysis"]
    )

# Fetch data
@st.cache_data(ttl=3600)
def fetch_financial_data(symbol):
    try:
        # Get stock info
        ticker_info = get_stock_info(symbol)
        
        # Get historical data for analysis
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*2)
        historical_data = get_stock_data(symbol, start_date, end_date)
        
        return ticker_info, historical_data
    except Exception as e:
        return None, None

if stock_symbol:
    ticker_info, hist_data = fetch_financial_data(stock_symbol)
    
    if ticker_info is None:
        st.error(f"❌ Could not fetch data for {stock_symbol}. Please try another symbol.")
    else:
        # ==================== KEY METRICS TAB ====================
        if analysis_type == "Key Metrics":
            st.markdown('<div class="section-header"><h2>Key Financial Metrics</h2></div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            # Get current price
            current_price = ticker_info.get('currentPrice', ticker_info.get('regularMarketPrice', 'N/A'))
            market_cap = ticker_info.get('marketCap', 'N/A')
            pe_ratio = ticker_info.get('trailingPE', 'N/A')
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Current Price</div>
                    <div class="metric-value">₹{current_price if current_price != 'N/A' else 'N/A'}</div>
                    <div class="metric-change positive">↑ Updated</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Market Cap</div>
                    <div class="metric-value">{market_cap if market_cap != 'N/A' else 'N/A'}</div>
                    <div class="metric-change">Crores</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Stock P/E</div>
                    <div class="metric-value">{pe_ratio if pe_ratio != 'N/A' else 'N/A'}</div>
                    <div class="metric-change">Trailing</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                dividend_yield = ticker_info.get('dividendYield', 'N/A')
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Dividend Yield</div>
                    <div class="metric-value">{f"{dividend_yield*100:.2f}%" if dividend_yield != 'N/A' else 'N/A'}</div>
                    <div class="metric-change">Annual</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Additional metrics
            st.markdown('<div class="section-header"><h3>Additional Metrics</h3></div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                book_value = ticker_info.get('bookValue', 'N/A')
                st.metric("Book Value", f"₹{book_value}" if book_value != 'N/A' else 'N/A')
            
            with col2:
                roe = ticker_info.get('returnOnEquity', 'N/A')
                st.metric("ROE", f"{roe*100:.2f}%" if roe != 'N/A' else 'N/A')
            
            with col3:
                beta = ticker_info.get('beta', 'N/A')
                st.metric("Beta", f"{beta:.2f}" if beta != 'N/A' else 'N/A')
            
            with col4:
                debt_to_equity = ticker_info.get('debtToEquity', 'N/A')
                st.metric("Debt/Equity", f"{debt_to_equity:.2f}" if debt_to_equity != 'N/A' else 'N/A')
            
            # 52-week range
            st.markdown('<div class="section-header"><h3>52-Week Range</h3></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                high_52w = ticker_info.get('fiftyTwoWeekHigh', 'N/A')
                st.metric("52-Week High", f"₹{high_52w}" if high_52w != 'N/A' else 'N/A')
            
            with col2:
                low_52w = ticker_info.get('fiftyTwoWeekLow', 'N/A')
                st.metric("52-Week Low", f"₹{low_52w}" if low_52w != 'N/A' else 'N/A')
        
        # ==================== FINANCIAL STATEMENTS TAB ====================
        elif analysis_type == "Financial Statements":
            st.markdown('<div class="section-header"><h2>Financial Statements</h2></div>', unsafe_allow_html=True)
            
            statement_type = st.radio(
                "Select Statement",
                ["Income Statement", "Balance Sheet", "Cash Flow"]
            )
            
            period = st.radio("Period", ["Annual", "Quarterly"], key="period_select")
            
            if statement_type == "Income Statement":
                st.subheader("💰 Income Statement (P&L)")
                
                income_data = get_income_statement(stock_symbol)
                
                if income_data:
                    statements = income_data['annual'] if period == "Annual" else income_data['quarterly']
                    
                    if statements:
                        # Create dataframe from statements
                        display_items = ['fiscalDateEnding', 'totalRevenue', 'costOfRevenue', 
                                       'grossProfit', 'operatingIncome', 'netIncome']
                        
                        df_display = []
                        for stmt in statements[:4]:  # Show last 4 periods
                            row = {
                                'Period': stmt.get('fiscalDateEnding', 'N/A'),
                                'Revenue': int(stmt.get('totalRevenue', 0)) or 0,
                                'COGS': int(stmt.get('costOfRevenue', 0)) or 0,
                                'Gross Profit': int(stmt.get('grossProfit', 0)) or 0,
                                'Operating Income': int(stmt.get('operatingIncome', 0)) or 0,
                                'Net Income': int(stmt.get('netIncome', 0)) or 0
                            }
                            df_display.append(row)
                        
                        df = pd.DataFrame(df_display)
                        
                        # Display as formatted table
                        st.dataframe(df.style.format({'Revenue': '${:,.0f}', 'COGS': '${:,.0f}', 
                                                       'Gross Profit': '${:,.0f}', 'Operating Income': '${:,.0f}',
                                                       'Net Income': '${:,.0f}'}), use_container_width=True)
                        
                        # Calculate margins
                        if df_display:
                            latest = df_display[0]
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if latest['Revenue'] > 0:
                                    gm = (latest['Gross Profit'] / latest['Revenue']) * 100
                                    st.metric("Gross Margin", f"{gm:.1f}%")
                            with col2:
                                if latest['Revenue'] > 0:
                                    om = (latest['Operating Income'] / latest['Revenue']) * 100
                                    st.metric("Operating Margin", f"{om:.1f}%")
                            with col3:
                                if latest['Revenue'] > 0:
                                    nm = (latest['Net Income'] / latest['Revenue']) * 100
                                    st.metric("Net Margin", f"{nm:.1f}%")
                    else:
                        st.warning("No income statement data available for this period.")
                else:
                    st.warning("⚠️ Enable Alpha Vantage API to view income statements. Add your API key to `.env` file.")
            
            elif statement_type == "Balance Sheet":
                st.subheader("📊 Balance Sheet")
                
                balance_data = get_balance_sheet(stock_symbol)
                
                if balance_data:
                    statements = balance_data['annual'] if period == "Annual" else balance_data['quarterly']
                    
                    if statements:
                        df_display = []
                        for stmt in statements[:4]:  # Show last 4 periods
                            row = {
                                'Period': stmt.get('reportedDate', 'N/A'),
                                'Total Assets': int(stmt.get('totalAssets', 0)) or 0,
                                'Current Assets': int(stmt.get('totalCurrentAssets', 0)) or 0,
                                'Current Liabilities': int(stmt.get('totalCurrentLiabilities', 0)) or 0,
                                'Total Liabilities': int(stmt.get('totalLiabilities', 0)) or 0,
                                'Shareholders Equity': int(stmt.get('totalShareholderEquity', 0)) or 0
                            }
                            df_display.append(row)
                        
                        df = pd.DataFrame(df_display)
                        
                        st.dataframe(df.style.format({'Total Assets': '${:,.0f}', 'Current Assets': '${:,.0f}',
                                                       'Current Liabilities': '${:,.0f}', 'Total Liabilities': '${:,.0f}',
                                                       'Shareholders Equity': '${:,.0f}'}), use_container_width=True)
                        
                        # Key ratios
                        if df_display:
                            latest = df_display[0]
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if latest['Current Liabilities'] > 0:
                                    cr = latest['Current Assets'] / latest['Current Liabilities']
                                    st.metric("Current Ratio", f"{cr:.2f}")
                            with col2:
                                if latest['Total Assets'] > 0:
                                    adr = (latest['Total Liabilities'] / latest['Total Assets']) * 100
                                    st.metric("Debt Ratio", f"{adr:.1f}%")
                            with col3:
                                if latest['Shareholders Equity'] > 0:
                                    roe_calc = (latest.get('Net Income', 0) / latest['Shareholders Equity']) * 100 if 'Net Income' in latest else 0
                                    st.metric("Equity Ratio", f"{(latest['Shareholders Equity']/latest['Total Assets']*100):.1f}%")
                    else:
                        st.warning("No balance sheet data available for this period.")
                else:
                    st.warning("⚠️ Enable Alpha Vantage API to view balance sheets. Add your API key to `.env` file.")
            
            else:  # Cash Flow
                st.subheader("💵 Cash Flow Statement")
                
                cf_data = get_cash_flow(stock_symbol)
                
                if cf_data:
                    statements = cf_data['annual'] if period == "Annual" else cf_data['quarterly']
                    
                    if statements:
                        df_display = []
                        for stmt in statements[:4]:  # Show last 4 periods
                            row = {
                                'Period': stmt.get('fiscalDateEnding', 'N/A'),
                                'Operating CF': int(stmt.get('operatingCashflow', 0)) or 0,
                                'Investing CF': int(stmt.get('capitalExpenditures', 0)) or 0,
                                'Financing CF': int(stmt.get('dividendsPaid', 0)) or 0,
                                'Free Cash Flow': (int(stmt.get('operatingCashflow', 0)) or 0) - (int(stmt.get('capitalExpenditures', 0)) or 0)
                            }
                            df_display.append(row)
                        
                        df = pd.DataFrame(df_display)
                        
                        st.dataframe(df.style.format({'Operating CF': '${:,.0f}', 'Investing CF': '${:,.0f}',
                                                       'Financing CF': '${:,.0f}', 'Free Cash Flow': '${:,.0f}'}), use_container_width=True)
                        
                        # FCF visualization
                        if df_display:
                            fig = go.Figure()
                            fig.add_trace(go.Bar(
                                name='Operating CF',
                                x=[d['Period'] for d in df_display],
                                y=[d['Operating CF'] for d in df_display],
                                marker_color='#10B981'
                            ))
                            fig.add_trace(go.Bar(
                                name='Free Cash Flow',
                                x=[d['Period'] for d in df_display],
                                y=[d['Free Cash Flow'] for d in df_display],
                                marker_color='#3B82F6'
                            ))
                            fig.update_layout(
                                title="Cash Flow Trends",
                                template="plotly_dark",
                                hovermode='x unified',
                                height=400
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No cash flow data available for this period.")
                else:
                    st.warning("⚠️ Enable Alpha Vantage API to view cash flow statements. Add your API key to `.env` file.")

        
        # ==================== RATIOS TAB ====================
        elif analysis_type == "Ratios":
            st.markdown('<div class="section-header"><h2>Financial Ratios Analysis</h2></div>', unsafe_allow_html=True)
            
            ratio_category = st.selectbox(
                "Ratio Category",
                ["Profitability", "Liquidity", "Efficiency", "Leverage", "Valuation"]
            )
            
            if ratio_category == "Profitability":
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("ROE (Return on Equity)", ticker_info.get('returnOnEquity', 'N/A'))
                with col2:
                    st.metric("ROA (Return on Assets)", "N/A", help="Coming soon")
                with col3:
                    st.metric("Net Profit Margin", "N/A", help="Coming soon")
            
            elif ratio_category == "Liquidity":
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Ratio", "N/A", help="Coming soon")
                with col2:
                    st.metric("Quick Ratio", "N/A", help="Coming soon")
                with col3:
                    st.metric("Working Capital", "N/A", help="Coming soon")
            
            elif ratio_category == "Efficiency":
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Asset Turnover", "N/A", help="Coming soon")
                with col2:
                    st.metric("Inventory Turnover", "N/A", help="Coming soon")
                with col3:
                    st.metric("Receivable Days", "N/A", help="Coming soon")
            
            elif ratio_category == "Leverage":
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Debt-to-Equity", ticker_info.get('debtToEquity', 'N/A'))
                with col2:
                    st.metric("Debt-to-Assets", "N/A", help="Coming soon")
                with col3:
                    st.metric("Interest Coverage", "N/A", help="Coming soon")
            
            else:  # Valuation
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("P/E Ratio", ticker_info.get('trailingPE', 'N/A'))
                with col2:
                    st.metric("P/B Ratio", "N/A", help="Coming soon")
                with col3:
                    st.metric("PEG Ratio", "N/A", help="Coming soon")
        
        # ==================== GROWTH ANALYSIS TAB ====================
        else:  # Growth Analysis
            st.markdown('<div class="section-header"><h2>Growth Analysis</h2></div>', unsafe_allow_html=True)
            
            growth_metrics = {
                "Revenue Growth (5Y CAGR)": "N/A",
                "Profit Growth (5Y CAGR)": "N/A",
                "Earnings Per Share Growth": "N/A",
                "Dividend Growth": ticker_info.get('fiveYearAverageDividendYield', 'N/A'),
                "Book Value Growth": "N/A",
                "Sales Growth (TTM)": "N/A"
            }
            
            growth_df = pd.DataFrame({
                "Metric": list(growth_metrics.keys()),
                "Value": list(growth_metrics.values())
            })
            
            st.dataframe(growth_df, use_container_width=True)
            
            # Growth chart
            st.markdown('<div class="section-header"><h3>Historical Growth Trend</h3></div>', unsafe_allow_html=True)
            
            if hist_data is not None and len(hist_data) > 0:
                # Calculate simple growth metric
                hist_data['MA_20'] = hist_data['Close'].rolling(window=20).mean()
                hist_data['MA_50'] = hist_data['Close'].rolling(window=50).mean()
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=hist_data.index,
                    y=hist_data['Close'],
                    name='Stock Price',
                    line=dict(color='#3B82F6', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=hist_data.index,
                    y=hist_data['MA_20'],
                    name='20-Day MA',
                    line=dict(color='#F59E0B', width=1, dash='dash')
                ))
                
                fig.add_trace(go.Scatter(
                    x=hist_data.index,
                    y=hist_data['MA_50'],
                    name='50-Day MA',
                    line=dict(color='#EF4444', width=1, dash='dash')
                ))
                
                fig.update_layout(
                    title=f"{stock_symbol} - Price Growth Trend",
                    xaxis_title="Date",
                    yaxis_title="Price (₹)",
                    hovermode='x unified',
                    template='plotly_dark',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Enter a stock symbol in the sidebar to view financial metrics")
    
    st.markdown("""
    ## 📊 Financial Metrics Dashboard
    
    This page provides comprehensive financial analysis including:
    
    ### Features:
    - **Key Metrics**: Current price, market cap, P/E ratio, dividend yield, ROE, etc.
    - **Financial Statements**: Income statement, balance sheet, cash flow
    - **Ratio Analysis**: Profitability, liquidity, efficiency, leverage, valuation ratios
    - **Growth Analysis**: Historical growth trends and CAGR calculations
    
    ### Supported Stocks:
    - US Stocks: AAPL, MSFT, GOOGL, TSLA, AMZN
    - Indian Stocks (NSE): RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, ICICIBANK.NS
    
    *More features coming soon including detailed financial statements from APIs*
    """)
