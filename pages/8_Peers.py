import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.ui_helpers import page_header, premium_css

st.set_page_config(
    page_title="Peer Comparison - StockSense",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

premium_css()
page_header("Peer Comparison", "Benchmark against industry competitors", "🔗")
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .peer-metric {
        font-size: 20px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .peer-label {
        font-size: 12px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-rank {
        font-size: 13px;
        margin-top: 8px;
        padding: 5px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
    
    .section-header {
        color: #06B6D4;
        border-bottom: 3px solid #06B6D4;
        padding-bottom: 10px;
        margin: 30px 0 20px 0;
    }
    
    .comparison-table {
        font-size: 13px;
    }
    
    .good {
        color: #10B981;
        font-weight: bold;
    }
    
    .poor {
        color: #EF4444;
        font-weight: bold;
    }
    
    .average {
        color: #F59E0B;
        font-weight: bold;
    }
    
    .info-card {
        background: rgba(6, 182, 212, 0.1);
        padding: 15px;
        border-left: 4px solid #06B6D4;
        border-radius: 4px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Peer Comparison Analysis")

with st.sidebar:
    st.header("Comparison Settings")
    primary_stock = st.text_input(
        "Primary Stock",
        value="TCS.NS",
        help="e.g., TCS.NS, INFY.NS, WIPRO.NS"
    ).strip().upper()
    
    peers = st.multiselect(
        "Select Peer Companies",
        ["INFY.NS", "WIPRO.NS", "COFORGE.NS", "LT.NS", "HDFC.NS"],
        default=["INFY.NS", "WIPRO.NS"],
        help="Choose up to 4 peers for comparison"
    )
    
    comparison_type = st.radio(
        "Comparison Type",
        ["Valuation Metrics", "Profitability Ratios", "Growth Trends", "Efficiency Metrics"]
    )

if primary_stock and peers:
    # Prepare comparison data
    peer_list = [primary_stock] + list(peers)
    
    # Sample comparison data
    comparison_data = {
        'Stock': ['TCS.NS', 'INFY.NS', 'WIPRO.NS', 'COFORGE.NS'],
        'Price': [3850.50, 1620.30, 480.75, 7250.25],
        'Market Cap (₹Cr)': [2450000, 1850000, 445000, 85000],
        'P/E Ratio': [28.5, 32.2, 24.8, 42.1],
        'P/B Ratio': [8.5, 10.2, 6.8, 15.3],
        'ROE %': [29.8, 31.2, 27.5, 36.1],
        'Net Margin %': [21.2, 20.8, 19.5, 18.2],
        'Revenue Growth %': [12.5, 14.2, 9.8, 18.5],
        'EPS (₹)': [135.2, 50.3, 19.4, 172.5],
        'Debt/Equity': [0.15, 0.22, 0.18, 0.35]
    }
    
    df_peers = pd.DataFrame(comparison_data)
    
    # ==================== VALUATION METRICS ====================
    if comparison_type == "Valuation Metrics":
        st.markdown('<div class="section-header"><h2>Valuation Comparison</h2></div>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        for idx, stock in enumerate(peer_list[:4]):
            data_idx = list(df_peers['Stock']).index(stock) if stock in df_peers['Stock'].values else 0
            
            with [col1, col2, col3, col4][idx]:
                pe = df_peers.loc[data_idx, 'P/E Ratio']
                pb = df_peers.loc[data_idx, 'P/B Ratio']
                
                pe_class = "good" if pe < 25 else ("poor" if pe > 35 else "average")
                
                st.markdown(f"""
                <div class="peer-card">
                    <div class="peer-label">{stock}</div>
                    <div class="peer-metric">₹{df_peers.loc[data_idx, 'Price']:.2f}</div>
                    <div style="font-size: 12px; opacity: 0.8;">Current Price</div>
                    <hr style="margin: 10px 0; opacity: 0.3;">
                    <div class="metric-rank">
                        <span class="{pe_class}">P/E: {pe:.1f}x</span><br>
                        P/B: {pb:.1f}x
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Valuation metrics table
        st.markdown('<div class="section-header"><h3>Valuation Metrics Comparison</h3></div>', 
                   unsafe_allow_html=True)
        
        val_df = df_peers[['Stock', 'Price', 'Market Cap (₹Cr)', 'P/E Ratio', 'P/B Ratio', 'EPS (₹)']].copy()
        val_df['Valuation'] = val_df['P/E Ratio'].apply(
            lambda x: "🟢 Undervalued" if x < 25 else ("🔴 Expensive" if x > 35 else "🟡 Fair")
        )
        
        st.dataframe(val_df.set_index('Stock'), use_container_width=True)
        
        # P/E vs P/B scatter
        st.markdown('<div class="section-header"><h3>P/E vs P/B Positioning</h3></div>', 
                   unsafe_follow_html=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_peers['P/E Ratio'],
            y=df_peers['P/B Ratio'],
            mode='markers+text',
            text=df_peers['Stock'],
            textposition="top center",
            marker=dict(
                size=15,
                color=df_peers['P/E Ratio'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="P/E Ratio")
            ),
            textfont=dict(size=10)
        ))
        
        fig.update_layout(
            title="Valuation Positioning: P/E vs P/B",
            xaxis_title="P/E Ratio",
            yaxis_title="P/B Ratio",
            template="plotly_dark",
            height=500,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.markdown("""
        <div class="info-card">
        <strong>📈 Valuation Analysis</strong><br>
        <br>
        <strong>TCS.NS (Your Stock):</strong><br>
        • P/E of 28.5x is slightly above peers average<br>
        • Fair valuation given strong growth<br>
        • Lowest P/B ratio suggests value relative to equity<br>
        <br>
        <strong>Peer Comparison:</strong><br>
        • WIPRO: Most attractive valuation (P/E 24.8x)<br>
        • COFORGE: Most expensive (P/E 42.1x)<br>
        • INFY: Premium valuation reflects quality
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== PROFITABILITY RATIOS ====================
    elif comparison_type == "Profitability Ratios":
        st.markdown('<div class="section-header"><h2>Profitability Comparison</h2></div>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        for idx, stock in enumerate(peer_list[:4]):
            data_idx = list(df_peers['Stock']).index(stock) if stock in df_peers['Stock'].values else 0
            roe = df_peers.loc[data_idx, 'ROE %']
            
            roe_class = "good" if roe > 30 else ("average" if roe > 20 else "poor")
            
            with [col1, col2, col3, col4][idx]:
                st.markdown(f"""
                <div class="peer-card">
                    <div class="peer-label">{stock}</div>
                    <div class="peer-metric">{df_peers.loc[data_idx, 'ROE %']:.1f}%</div>
                    <div style="font-size: 12px; opacity: 0.8;">Return on Equity</div>
                    <hr style="margin: 10px 0; opacity: 0.3;">
                    <div class="metric-rank">
                        <span class="{roe_class}">Net Margin: {df_peers.loc[data_idx, 'Net Margin %']:.1f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Profitability comparison
        st.markdown('<div class="section-header"><h3>Profitability Metrics</h3></div>', 
                   unsafe_allow_html=True)
        
        profit_df = df_peers[['Stock', 'ROE %', 'Net Margin %', 'Revenue Growth %']].copy()
        profit_df['Profitability Score'] = (
            (profit_df['ROE %'] / 40 * 33) + 
            (profit_df['Net Margin %'] / 25 * 33) + 
            (profit_df['Revenue Growth %'] / 20 * 34)
        ).round(1)
        
        st.dataframe(profit_df.set_index('Stock'), use_container_width=True)
        
        # ROE & Net Margin comparison bar chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=df_peers['Stock'], y=df_peers['ROE %'], name='ROE %',
                   marker_color='#06B6D4'),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=df_peers['Stock'], y=df_peers['Net Margin %'], name='Net Margin %',
                      mode='lines+markers', marker=dict(size=10), line=dict(width=3, color='#10B981')),
            secondary_y=True
        )
        
        fig.update_layout(
            title="Profitability Metrics Comparison",
            template="plotly_dark",
            height=500,
            hovermode='x unified'
        )
        
        fig.update_yaxes(title_text="ROE %", secondary_y=False)
        fig.update_yaxes(title_text="Net Margin %", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analysis
        st.markdown("""
        <div class="info-card">
        <strong>🎯 Profitability Analysis</strong><br>
        <br>
        <strong>TCS.NS (Your Stock):</strong><br>
        • Excellent ROE of 29.8% shows strong earnings quality<br>
        • Net margin of 21.2% is among the highest<br>
        • Consistent profitability across business segments<br>
        <br>
        <strong>Competitive Position:</strong><br>
        • TCS leads in net margin efficiency<br>
        • COFORGE shows highest growth but lower margins<br>
        • All peers are profitable with healthy margins
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== GROWTH TRENDS ====================
    elif comparison_type == "Growth Trends":
        st.markdown('<div class="section-header"><h2>Growth Analysis</h2></div>', 
                   unsafe_allow_html=True)
        
        # Growth data for multiple years
        growth_years = ['2022-23', '2023-24', '2024-25E', '2025-26E']
        growth_data = {
            'Year': growth_years,
            'TCS.NS': [16.2, 12.5, 14.2, 15.8],
            'INFY.NS': [18.5, 14.2, 16.5, 17.2],
            'WIPRO.NS': [5.2, 9.8, 12.5, 14.1],
            'COFORGE.NS': [22.5, 18.5, 20.1, 19.5]
        }
        
        fig = go.Figure()
        
        colors = ['#06B6D4', '#EC4899', '#F59E0B', '#10B981']
        for stock, color in zip(['TCS.NS', 'INFY.NS', 'WIPRO.NS', 'COFORGE.NS'], colors):
            fig.add_trace(go.Scatter(
                x=growth_data['Year'],
                y=growth_data[stock],
                name=stock,
                mode='lines+markers',
                line=dict(width=3, color=color),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="Revenue Growth Trends",
            xaxis_title="Year",
            yaxis_title="Growth %",
            template="plotly_dark",
            height=500,
            hovermode='x unified',
            yaxis=dict(range=[0, 25])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Growth metrics table
        st.markdown('<div class="section-header"><h3>Growth Metrics</h3></div>', 
                   unsafe_allow_html=True)
        
        growth_metrics = {
            'Stock': ['TCS.NS', 'INFY.NS', 'WIPRO.NS', 'COFORGE.NS'],
            'Revenue Growth (FY24)': [12.5, 14.2, 9.8, 18.5],
            'EPS Growth 3Y CAGR': [15.2, 16.8, 8.5, 22.3],
            'Projected Growth (FY25)': [14.2, 16.5, 12.5, 20.1],
            'Growth Momentum': ['Stable', 'Accelerating', 'Accelerating', 'Slowing']
        }
        
        df_growth = pd.DataFrame(growth_metrics)
        st.dataframe(df_growth.set_index('Stock'), use_container_width=True)
        
        # Analysis
        st.markdown("""
        <div class="info-card">
        <strong>📈 Growth Trajectory</strong><br>
        <br>
        <strong>TCS.NS (Your Stock):</strong><br>
        • Stable growth of 12-15% range<br>
        • Mature company with consistent expansion<br>
        • Expected to continue healthy growth<br>
        <br>
        <strong>Peers Comparison:</strong><br>
        • COFORGE: Highest growth but decelerating (cyclical)<br>
        • WIPRO: Turnaround story with accelerating growth<br>
        • INFY: Strong organic growth trajectory<br>
        • TCS: Most stable and predictable growth
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== EFFICIENCY METRICS ====================
    else:
        st.markdown('<div class="section-header"><h2>Operational Efficiency</h2></div>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        for idx, stock in enumerate(peer_list[:4]):
            data_idx = list(df_peers['Stock']).index(stock) if stock in df_peers['Stock'].values else 0
            debt = df_peers.loc[data_idx, 'Debt/Equity']
            
            debt_class = "good" if debt < 0.3 else ("average" if debt < 0.5 else "poor")
            
            with [col1, col2, col3, col4][idx]:
                st.markdown(f"""
                <div class="peer-card">
                    <div class="peer-label">{stock}</div>
                    <div class="peer-metric">{debt:.2f}x</div>
                    <div style="font-size: 12px; opacity: 0.8;">Debt/Equity Ratio</div>
                    <hr style="margin: 10px 0; opacity: 0.3;">
                    <div class="metric-rank">
                        <span class="{debt_class}">{'Low Leverage' if debt < 0.3 else ('Moderate' if debt < 0.5 else 'High')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Efficiency metrics
        st.markdown('<div class="section-header"><h3>Efficiency Metrics Comparison</h3></div>', 
                   unsafe_allow_html=True)
        
        efficiency_df = df_peers[['Stock', 'Debt/Equity', 'Net Margin %', 'ROE %']].copy()
        efficiency_df['Financial Health'] = efficiency_df['Debt/Equity'].apply(
            lambda x: "🟢 Excellent" if x < 0.2 else ("🟡 Good" if x < 0.4 else "🔴 Caution")
        )
        
        st.dataframe(efficiency_df.set_index('Stock'), use_container_width=True)
        
        # Leverage vs efficiency
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_peers['Debt/Equity'],
            y=df_peers['ROE %'],
            mode='markers+text',
            text=df_peers['Stock'],
            textposition="top center",
            marker=dict(
                size=15,
                color=df_peers['ROE %'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="ROE %")
            ),
            textfont=dict(size=10)
        ))
        
        fig.update_layout(
            title="Leverage vs Return on Equity",
            xaxis_title="Debt/Equity Ratio",
            yaxis_title="ROE %",
            template="plotly_dark",
            height=500,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analysis
        st.markdown("""
        <div class="info-card">
        <strong>⚙️ Efficiency & Financial Health</strong><br>
        <br>
        <strong>TCS.NS (Your Stock):</strong><br>
        • Lowest leverage among peers (0.15x D/E)<br>
        • Strong balance sheet provides flexibility<br>
        • Excellent return generation with minimal debt<br>
        <br>
        <strong>Financial Positions:</strong><br>
        • TCS & INFY: Fortress balance sheets<br>
        • WIPRO: Moderate leverage, improving trend<br>
        • COFORGE: Higher leverage for growth investments<br>
        <br>
        <strong>Recommendation:</strong><br>
        TCS offers the best combination of growth and financial stability among peers.
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== OVERALL SUMMARY ====================
    st.markdown('<div class="section-header"><h2>Peer Comparison Summary</h2></div>', 
               unsafe_allow_html=True)
    
    summary = pd.DataFrame({
        'Metric': ['Valuation', 'Profitability', 'Growth', 'Efficiency', 'Overall Score'],
        'TCS.NS': ['7/10', '9/10', '7/10', '9/10', '8/10'],
        'INFY.NS': ['6/10', '9/10', '8/10', '9/10', '8/10'],
        'WIPRO.NS': ['8/10', '7/10', '7/10', '8/10', '7.5/10'],
        'COFORGE.NS': ['5/10', '7/10', '9/10', '6/10', '6.75/10']
    })
    
    st.dataframe(summary.set_index('Metric'), use_container_width=True)
    
    st.markdown("""
    <div class="info-card">
    <strong>✅ Key Takeaways</strong><br>
    <br>
    <strong>Best Valuation:</strong> WIPRO.NS<br>
    <strong>Highest Growth:</strong> COFORGE.NS<br>
    <strong>Best Quality:</strong> TCS.NS & INFY.NS<br>
    <strong>Most Conservative:</strong> TCS.NS<br>
    <br>
    Your stock (TCS.NS) offers a balanced mix of quality, profitability, and reasonable valuation. Best suited for long-term investors seeking stability.
    </div>
    """, unsafe_allow_html=True)

else:
    st.warning("Please select a primary stock and at least one peer company to begin comparison.")
