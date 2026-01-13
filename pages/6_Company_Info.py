import streamlit as st
from utils.data_fetcher import get_stock_info
from utils.ui_helpers import page_header, premium_css
import pandas as pd

st.set_page_config(
    page_title="Company Info - StockSense",
    page_icon="🏢",
    layout="wide"
)

premium_css()
page_header("Company Information", "Detailed profiles & leadership", "🏢")
    .company-section {
        background: linear-gradient(135deg, #1A1F2E 0%, #0F1419 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 4px solid #3B82F6;
        margin: 20px 0;
    }
    
    .info-header {
        color: #3B82F6;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 2px solid #3B82F6;
        padding-bottom: 10px;
    }
    
    .info-item {
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 20px;
        margin: 12px 0;
        padding: 10px 0;
        border-bottom: 1px solid #2A3142;
    }
    
    .info-label {
        color: #9CA3AF;
        font-weight: 500;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .info-value {
        color: #FFFFFF;
        font-size: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏢 Company Information")

with st.sidebar:
    st.header("Stock Selection")
    stock_symbol = st.text_input(
        "Enter Stock Symbol",
        value="AAPL",
        help="e.g., AAPL, RELIANCE.NS"
    ).strip().upper()

if stock_symbol:
    try:
        ticker_info = get_stock_info(stock_symbol)
        
        # Company Overview
        st.markdown('<div class="company-section"><div class="info-header">📌 Company Overview</div>', unsafe_allow_html=True)
        
        company_name = ticker_info.get('longName', stock_symbol)
        sector = ticker_info.get('sector', 'N/A')
        industry = ticker_info.get('industry', 'N/A')
        country = ticker_info.get('country', 'N/A')
        website = ticker_info.get('website', 'N/A')
        
        st.markdown(f"""
        <div class="info-item">
            <div class="info-label">Company Name</div>
            <div class="info-value">{company_name}</div>
        </div>
        
        <div class="info-item">
            <div class="info-label">Sector</div>
            <div class="info-value">{sector}</div>
        </div>
        
        <div class="info-item">
            <div class="info-label">Industry</div>
            <div class="info-value">{industry}</div>
        </div>
        
        <div class="info-item">
            <div class="info-label">Country</div>
            <div class="info-value">{country}</div>
        </div>
        
        <div class="info-item">
            <div class="info-label">Website</div>
            <div class="info-value">{f'<a href="{website}" target="_blank">{website}</a>' if website != 'N/A' else 'N/A'}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Business Summary
        st.markdown('<div class="company-section"><div class="info-header">📋 Business Summary</div>', unsafe_allow_html=True)
        
        long_summary = ticker_info.get('longBusinessSummary', ticker_info.get('businessSummary', 'No summary available'))
        st.markdown(f"<div class='info-value'>{long_summary}</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Key People
        st.markdown('<div class="company-section"><div class="info-header">👥 Company Leadership</div>', unsafe_allow_html=True)
        
        company_officers = ticker_info.get('companyOfficers', [])
        
        if company_officers:
            officer_data = []
            for officer in company_officers[:5]:  # Top 5 officers
                officer_data.append({
                    "Name": officer.get('name', 'N/A'),
                    "Position": officer.get('title', 'N/A'),
                    "Pay": f"${officer.get('totalPay', 'N/A'):,.0f}" if isinstance(officer.get('totalPay'), (int, float)) else 'N/A'
                })
            
            officers_df = pd.DataFrame(officer_data)
            st.dataframe(officers_df, use_container_width=True, hide_index=True)
        else:
            st.info("Leadership information not available")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Company Basics
        st.markdown('<div class="company-section"><div class="info-header">📊 Company Basics</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="info-item">
                <div class="info-label">CEO</div>
                <div class="info-value">{ticker_info.get('ceo', 'N/A')}</div>
            </div>
            
            <div class="info-item">
                <div class="info-label">Employees</div>
                <div class="info-value">{f"{ticker_info.get('fullTimeEmployees', 'N/A'):,}" if isinstance(ticker_info.get('fullTimeEmployees'), int) else 'N/A'}</div>
            </div>
            
            <div class="info-item">
                <div class="info-label">Founded</div>
                <div class="info-value">{ticker_info.get('founded', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-item">
                <div class="info-label">Headquarters</div>
                <div class="info-value">{ticker_info.get('city', 'N/A')}, {ticker_info.get('state', 'N/A')}</div>
            </div>
            
            <div class="info-item">
                <div class="info-label">Phone</div>
                <div class="info-value">{ticker_info.get('phone', 'N/A')}</div>
            </div>
            
            <div class="info-item">
                <div class="info-label">Market Cap</div>
                <div class="info-value">₹{f"{ticker_info.get('marketCap', 'N/A'):,}" if isinstance(ticker_info.get('marketCap'), (int, float)) else 'N/A'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Business Segments (if available)
        if ticker_info.get('segments'):
            st.markdown('<div class="company-section"><div class="info-header">🏭 Business Segments</div>', unsafe_allow_html=True)
            
            segments = ticker_info.get('segments', [])
            segment_data = []
            for seg in segments:
                segment_data.append({
                    "Segment": seg.get('name', 'N/A'),
                    "Revenue %": f"{seg.get('revenue_percent', 'N/A')}%"
                })
            
            if segment_data:
                seg_df = pd.DataFrame(segment_data)
                st.dataframe(seg_df, use_container_width=True, hide_index=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Related Companies
        if ticker_info.get('relatedMarkets'):
            st.markdown('<div class="company-section"><div class="info-header">🔗 Related Companies</div>', unsafe_allow_html=True)
            st.info(f"Explore {len(ticker_info.get('relatedMarkets', []))} related companies in the same sector")
            st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Could not fetch company information for {stock_symbol}")
        st.info(f"Error: {str(e)}")

else:
    st.info("👈 Enter a stock symbol to view company information")
    
    st.markdown("""
    ## 🏢 Company Information
    
    View comprehensive company details including:
    - Company overview and business summary
    - Leadership team and executives
    - Sector and industry classification
    - Company basics (founded, employees, headquarters)
    - Business segments and revenue breakdown
    - Related companies and competitors
    """)
