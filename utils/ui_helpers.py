"""
Utility functions for consistent page styling and headers
"""
import streamlit as st

def page_header(title: str, subtitle: str, icon: str = "📈"):
    """
    Create a consistent premium page header across all pages
    
    Args:
        title: Main page title
        subtitle: Subtitle/description
        icon: Emoji icon for the page
    """
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1F2E 0%, #253549 100%); 
                border-bottom: 1px solid #2D3748; padding: 30px; 
                border-radius: 12px; margin-bottom: 30px;">
        <h1 style="margin: 0 0 8px 0; color: #E5E7EB; font-size: 28px;">
            {icon} {title}
        </h1>
        <p style="margin: 0; color: #9CA3AF; font-size: 14px;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)

def premium_metric(label: str, value: str, change: str = None, is_negative: bool = False):
    """
    Create a premium metric display
    
    Args:
        label: Metric label
        value: Metric value
        change: Optional change percentage
        is_negative: Whether the change is negative
    """
    change_html = ""
    if change:
        color = "#EF4444" if is_negative else "#10B981"
        sign = "" if is_negative else "+"
        change_html = f'<p style="color: {color}; margin: 8px 0 0 0; font-size: 13px; font-weight: 600;">{sign}{change}</p>'
    
    st.markdown(f"""
    <div style="background-color: #1A1F2E; border: 1px solid #2D3748; 
                padding: 20px; border-radius: 10px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <p style="color: #9CA3AF; margin: 0 0 8px 0; font-size: 12px; 
                  text-transform: uppercase; font-weight: 600;">
            {label}
        </p>
        <p style="color: #E5E7EB; margin: 0; font-size: 24px; font-weight: 700;">
            {value}
        </p>
        {change_html}
    </div>
    """, unsafe_allow_html=True)

def premium_css():
    """Apply premium styling to all pages"""
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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
        }
        
        /* Inputs */
        input, select, textarea {
            background-color: var(--card-bg) !important;
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
            padding: 10px 12px !important;
        }
        
        input:focus, select:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
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
        
        /* Metric Container */
        [data-testid="metric-container"] {
            background-color: var(--card-bg);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
