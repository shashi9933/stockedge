import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Shareholding Pattern - StockSense",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .shareholding-card {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .shareholding-value {
        font-size: 28px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .shareholding-label {
        font-size: 13px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .trend-up {
        color: #10B981;
        font-size: 14px;
        margin-top: 5px;
    }
    
    .trend-down {
        color: #EF4444;
        font-size: 14px;
        margin-top: 5px;
    }
    
    .section-header {
        color: #8B5CF6;
        border-bottom: 3px solid #8B5CF6;
        padding-bottom: 10px;
        margin: 30px 0 20px 0;
    }
    
    .info-box {
        background: rgba(139, 92, 246, 0.1);
        padding: 15px;
        border-left: 4px solid #8B5CF6;
        border-radius: 4px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("👥 Shareholding Pattern Analysis")

with st.sidebar:
    st.header("Configuration")
    stock_symbol = st.text_input(
        "Enter Stock Symbol",
        value="RELIANCE.NS",
        help="e.g., RELIANCE.NS, TCS.NS, INFY.NS"
    ).strip().upper()
    
    view_type = st.radio(
        "View Type",
        ["Current Holdings", "Quarterly Trends", "Insider Tracking"]
    )

if stock_symbol:
    # ==================== CURRENT HOLDINGS ====================
    if view_type == "Current Holdings":
        st.markdown('<div class="section-header"><h2>Current Shareholding Pattern</h2></div>', 
                   unsafe_allow_html=True)
        
        # Sample data structure for shareholding (in real app, would fetch from API)
        shareholding_data = {
            'Promoters': 58.2,
            'FII/Foreign': 23.5,
            'DII/Domestic': 12.1,
            'Public/Others': 6.2
        }
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="shareholding-card">
                <div class="shareholding-label">Promoters</div>
                <div class="shareholding-value">{shareholding_data['Promoters']:.1f}%</div>
                <div class="trend-up">↑ +0.5% (QoQ)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="shareholding-card">
                <div class="shareholding-label">FII/Foreign</div>
                <div class="shareholding-value">{shareholding_data['FII/Foreign']:.1f}%</div>
                <div class="trend-down">↓ -1.2% (QoQ)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="shareholding-card">
                <div class="shareholding-label">DII/Domestic</div>
                <div class="shareholding-value">{shareholding_data['DII/Domestic']:.1f}%</div>
                <div class="trend-up">↑ +0.8% (QoQ)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="shareholding-card">
                <div class="shareholding-label">Public/Others</div>
                <div class="shareholding-value">{shareholding_data['Public/Others']:.1f}%</div>
                <div class="trend-down">↓ -0.1% (QoQ)</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Pie chart
        st.markdown('<div class="section-header"><h3>Shareholding Distribution</h3></div>', 
                   unsafe_allow_html=True)
        
        colors = ['#8B5CF6', '#EC4899', '#F59E0B', '#10B981']
        fig = go.Figure(data=[go.Pie(
            labels=list(shareholding_data.keys()),
            values=list(shareholding_data.values()),
            marker=dict(colors=colors),
            textposition='inside',
            textinfo='label+percent'
        )])
        
        fig.update_layout(
            title="Current Shareholding Composition",
            template="plotly_dark",
            height=500,
            showlegend=True,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed breakdown
        st.markdown('<div class="section-header"><h3>Detailed Breakdown</h3></div>', 
                   unsafe_allow_html=True)
        
        breakdown_data = {
            'Category': ['Promoters - Individuals', 'Promoters - Corporate', 'FIIs', 'DIIs', 'Public', 'Others'],
            'Holdings %': [35.5, 22.7, 23.5, 12.1, 5.2, 1.0],
            'Shares (Millions)': [450.2, 288.5, 298.2, 153.5, 66.0, 12.7],
            'Value (₹ Crores)': [15850, 10125, 10465, 5384, 2316, 445]
        }
        
        df = pd.DataFrame(breakdown_data)
        st.dataframe(df.set_index('Category'), use_container_width=True)
        
        # Key insights
        st.markdown('<div class="section-header"><h3>Key Insights</h3></div>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box">
            <strong>📊 Promoter Holding Analysis</strong><br>
            • Strong promoter holding of 58.2%<br>
            • Indicates management confidence<br>
            • Low probability of hostile takeover<br>
            • Stable long-term direction
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
            <strong>🌍 Foreign Investment Trend</strong><br>
            • FII holdings at 23.5% (slightly reduced)<br>
            • Recent outflows amid rate hikes<br>
            • Still represents major institutional interest<br>
            • Monitor for global market sentiment
            </div>
            """, unsafe_allow_html=True)
    
    # ==================== QUARTERLY TRENDS ====================
    elif view_type == "Quarterly Trends":
        st.markdown('<div class="section-header"><h2>Shareholding Trends (Quarterly)</h2></div>', 
                   unsafe_allow_html=True)
        
        # Sample quarterly data
        quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
        
        trends_data = {
            'Quarter': quarters,
            'Promoters': [57.8, 58.0, 58.1, 58.2, 58.3, 58.2, 58.2, 58.2],
            'FII/Foreign': [24.8, 24.5, 24.0, 23.8, 23.7, 23.5, 23.5, 23.5],
            'DII/Domestic': [11.2, 11.3, 11.5, 11.6, 11.8, 12.0, 12.1, 12.1],
            'Public': [6.2, 6.2, 6.4, 6.4, 6.2, 6.3, 6.2, 6.2]
        }
        
        df_trends = pd.DataFrame(trends_data)
        
        # Line chart showing trends
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_trends['Quarter'],
            y=df_trends['Promoters'],
            name='Promoters',
            line=dict(color='#8B5CF6', width=3),
            mode='lines+markers',
            fill='tozeroy'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_trends['Quarter'],
            y=df_trends['FII/Foreign'],
            name='FII/Foreign',
            line=dict(color='#EC4899', width=3),
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_trends['Quarter'],
            y=df_trends['DII/Domestic'],
            name='DII/Domestic',
            line=dict(color='#F59E0B', width=3),
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_trends['Quarter'],
            y=df_trends['Public'],
            name='Public',
            line=dict(color='#10B981', width=3),
            mode='lines+markers'
        ))
        
        fig.update_layout(
            title="Shareholding Pattern - 2 Year Trend",
            xaxis_title="Quarter",
            yaxis_title="Shareholding %",
            template="plotly_dark",
            height=500,
            hovermode='x unified',
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Trend analysis table
        st.markdown('<div class="section-header"><h3>Trend Analysis (Last 8 Quarters)</h3></div>', 
                   unsafe_allow_html=True)
        
        analysis_data = {
            'Category': ['Promoters', 'FII/Foreign', 'DII/Domestic', 'Public'],
            'Current %': [58.2, 23.5, 12.1, 6.2],
            '2Q Change': [+0.0, +0.0, +0.1, -0.1],
            '4Q Change': [+0.2, -0.3, +0.5, -0.4],
            '8Q Change': [+0.4, -1.3, +0.9, 0.0],
            'Trend': ['→ Stable', '↓ Declining', '↑ Rising', '→ Stable']
        }
        
        df_analysis = pd.DataFrame(analysis_data)
        st.dataframe(df_analysis.set_index('Category'), use_container_width=True)
        
        # Interpretation
        st.markdown("""
        <div class="info-box">
        <strong>📈 Trend Interpretation</strong><br>
        <br>
        <strong>Promoters (Stable):</strong> Consistent holding shows management confidence and commitment to long-term value creation.
        <br><br>
        <strong>FII (Declining):</strong> Gradual reduction possibly due to rising US interest rates and currency appreciation concerns. Remain cautious on global flows.
        <br><br>
        <strong>DII (Rising):</strong> Increasing domestic institutional interest reflects strong domestic institutional confidence in company fundamentals.
        <br><br>
        <strong>Public (Stable):</strong> Minimal movement in retail investor holdings.
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== INSIDER TRACKING ====================
    else:
        st.markdown('<div class="section-header"><h2>Insider Transactions</h2></div>', 
                   unsafe_allow_html=True)
        
        # Sample insider transaction data
        insider_data = {
            'Date': ['2024-01-15', '2024-01-10', '2024-01-08', '2024-01-05', '2024-01-02'],
            'Insider Name': ['Mukesh Ambani', 'Nita Ambani', 'Board of Directors', 'Management', 'Reliance Industries'],
            'Position': ['Chairman', 'Director', 'Board Member', 'Executive', 'Promoter'],
            'Action': ['BUY', 'HOLD', 'GRANT', 'BUY', 'OPEN MARKET PURCHASE'],
            'Shares': [50000, 0, 100000, 25000, 500000],
            'Value (₹ Cr)': [175.5, 0, 350.5, 87.5, 1752.5],
            'Sentiment': ['BULLISH', 'NEUTRAL', 'BULLISH', 'BULLISH', 'BULLISH']
        }
        
        df_insider = pd.DataFrame(insider_data)
        
        # Format and display
        st.dataframe(
            df_insider.set_index('Date'),
            use_container_width=True
        )
        
        # Transaction sentiment summary
        st.markdown('<div class="section-header"><h3>Insider Activity Summary</h3></div>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Insider Buys",
                "₹2,915.5 Cr",
                "+5 transactions this month"
            )
        
        with col2:
            st.metric(
                "Sentiment Score",
                "VERY BULLISH",
                "+85/100 (5-star)"
            )
        
        with col3:
            st.metric(
                "Confidence Level",
                "HIGH",
                "Recent large purchases by promoters"
            )
        
        # Key insights
        st.markdown("""
        <div class="info-box">
        <strong>🔍 Insider Activity Analysis</strong><br>
        <br>
        ✅ <strong>Positive Signals:</strong><br>
        • Consistent insider buying over past month<br>
        • Large share purchases by promoters (bullish signal)<br>
        • No significant insider selling activity<br>
        • Management showing confidence in company future
        <br><br>
        ⚠️ <strong>Monitor:</strong><br>
        • Watch for unusual selling patterns<br>
        • Large option exercises (might indicate exit)<br>
        • Changes in shareholding structure
        <br><br>
        💡 <strong>Investment Implication:</strong><br>
        Recent insider buying is a strong bullish indicator. Management confidence suggests positive outlook for company growth and stock performance.
        </div>
        """, unsafe_allow_html=True)
        
        # Recent news related to shareholding
        st.markdown('<div class="section-header"><h3>Related News & Events</h3></div>', 
                   unsafe_allow_html=True)
        
        news_items = [
            ("Jan 15, 2024", "Promoters increase stake by 0.2%", "Positive"),
            ("Jan 10, 2024", "Board approves share buyback program", "Positive"),
            ("Jan 5, 2024", "FII reduces holding amid global uncertainty", "Neutral"),
            ("Dec 28, 2023", "Annual shareholders meeting scheduled", "Neutral")
        ]
        
        for date, event, sentiment in news_items:
            sentiment_color = "🟢" if sentiment == "Positive" else "🟡"
            st.write(f"{sentiment_color} **{date}:** {event}")
