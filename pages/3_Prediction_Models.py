import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.prediction_models import (
    linear_regression_prediction,
    quadratic_regression_prediction,
    fourier_transform_prediction,
    time_series_prediction,
    arima_model_prediction,
    ensemble_prediction,
    plot_predictions,
    plot_ensemble_weights
)
from utils.market_regime import (
    detect_market_regime,
    get_regime_description,
    get_recommended_settings,
    plot_market_regime,
    get_preferred_models_for_regime
)
from utils.ui_helpers import page_header, premium_css

# Set page configuration
st.set_page_config(
    page_title="Prediction Models - StockSense",
    page_icon="🤖",
    layout="wide"
)

premium_css()
page_header("Prediction Models", "AI-powered price forecasting", "🤖")

st.title("Prediction Models")
st.markdown("Stock price prediction using multiple models with market regime detection and ensemble approach.")

# Check if stock data exists in session state
if 'stock_data' not in st.session_state or st.session_state.stock_data is None:
    st.warning("Please select a stock from the home page first.")
    st.stop()

# Get stock data from session state
stock_data = st.session_state.stock_data
stock_symbol = st.session_state.selected_stock

# Detect market regime
try:
    regime_info = detect_market_regime(stock_data)
    current_regime = regime_info['regime']
    regime_confidence = regime_info['confidence']
    regime_duration = regime_info['duration']
    regime_change = regime_info['regime_change']
except Exception as e:
    st.error(f"Error detecting market regime: {str(e)}")
    current_regime = "Unknown"
    regime_confidence = 0.0
    regime_duration = 0
    regime_change = False

# Market Regime Detection Section
st.subheader("Market Regime Detection")

col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

with col1:
    # Display current regime with context-sensitive highlighting
    regime_colors = {
        "Trending Up": "green",
        "Trending Down": "red",
        "Range-Bound": "orange",
        "Unknown": "gray"
    }
    
    st.markdown(f"""
    <div style="padding: 10px; border-radius: 5px; background-color: {regime_colors.get(current_regime, 'gray')}20; 
         border: 1px solid {regime_colors.get(current_regime, 'gray')};">
        <h3 style="color: {regime_colors.get(current_regime, 'gray')}; margin:0;">
            Current Market Regime: {current_regime}
        </h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.metric("Regime Confidence", f"{regime_confidence:.2f}")

with col3:
    st.metric("Duration (days)", f"{regime_duration}")

with col4:
    if regime_change:
        st.metric("Regime Change", "Recent")
    else:
        st.metric("Regime Change", "Stable")

# Show market regime description
with st.expander("Market Regime Details", expanded=False):
    st.markdown(get_regime_description(current_regime))
    
    # Display regime plot
    regime_plot = plot_market_regime(stock_data, regime_info)
    st.plotly_chart(regime_plot, use_container_width=True)
    
    st.markdown(f"""
    ### Preferred Models for Current Regime
    
    The following models are typically more accurate in a **{current_regime}** market regime:
    """)
    
    preferred_models = get_preferred_models_for_regime(current_regime)
    for model in preferred_models:
        st.markdown(f"- **{model}**")

# Get recommended settings based on market regime
recommended_settings = get_recommended_settings(current_regime)
recommended_prediction_days = recommended_settings['prediction_days']
recommended_weights = recommended_settings['model_weights']

# Sidebar controls
st.sidebar.header("Prediction Settings")

# Prediction days selection
prediction_days = st.sidebar.slider(
    "Prediction Days", 
    min_value=5, 
    max_value=60, 
    value=recommended_prediction_days,
    step=5
)

# Adapt based on regime
st.sidebar.markdown(f"""
**Recommended for {current_regime} regime:** {recommended_prediction_days} days
""")

# Model selection
st.sidebar.subheader("Select Models")
show_linear = st.sidebar.checkbox("Linear Regression", value=True)
show_quadratic = st.sidebar.checkbox("Quadratic Regression", value=True)
show_fourier = st.sidebar.checkbox("Fourier Transform", value=True)
show_time_series = st.sidebar.checkbox("Time Series Analysis", value=True)
show_arima = st.sidebar.checkbox("ARIMA", value=True)
show_ensemble = st.sidebar.checkbox("Ensemble Model", value=True)

# Training period selection
training_period = st.sidebar.selectbox(
    "Training Data Period",
    ["Full History", "1 Year", "6 Months", "3 Months"]
)

# Use regime-aware predictions
use_regime_aware = st.sidebar.checkbox(
    "Use Regime-Aware Weighting", 
    value=True,
    help="Adjust model weights based on detected market regime (recommended)"
)

# Filter data based on selected training period
end_date = stock_data.index[-1]
if training_period == "1 Year":
    start_date = end_date - timedelta(days=365)
    training_data = stock_data[stock_data.index >= start_date]
elif training_period == "6 Months":
    start_date = end_date - timedelta(days=180)
    training_data = stock_data[stock_data.index >= start_date]
elif training_period == "3 Months":
    start_date = end_date - timedelta(days=90)
    training_data = stock_data[stock_data.index >= start_date]
else:
    training_data = stock_data.copy()

# Calculate predictions based on selected models
predictions = {}
confidence = {}

try:
    if show_linear:
        with st.spinner("Calculating Linear Regression predictions..."):
            linear_preds, linear_conf = linear_regression_prediction(training_data, prediction_days)
            predictions["Linear Regression"] = linear_preds
            confidence["Linear Regression"] = linear_conf

    if show_quadratic:
        with st.spinner("Calculating Quadratic Regression predictions..."):
            quad_preds, quad_conf = quadratic_regression_prediction(training_data, prediction_days)
            predictions["Quadratic Regression"] = quad_preds
            confidence["Quadratic Regression"] = quad_conf

    if show_fourier:
        with st.spinner("Calculating Fourier Transform predictions..."):
            fourier_preds, fourier_conf = fourier_transform_prediction(training_data, prediction_days)
            predictions["Fourier Transform"] = fourier_preds
            confidence["Fourier Transform"] = fourier_conf

    if show_time_series:
        with st.spinner("Calculating Time Series predictions..."):
            time_series_preds, time_series_conf = time_series_prediction(training_data, prediction_days)
            predictions["Time Series"] = time_series_preds
            confidence["Time Series"] = time_series_conf
            
    if show_arima:
        with st.spinner("Calculating ARIMA predictions..."):
            arima_preds, arima_conf = arima_model_prediction(training_data, prediction_days)
            predictions["ARIMA"] = arima_preds
            confidence["ARIMA"] = arima_conf

    if show_ensemble:
        with st.spinner("Calculating Regime-Aware Ensemble predictions..."):
            # If using regime-aware predictions, pass the recommended weights
            if use_regime_aware:
                ensemble_preds, ensemble_conf, model_weights = ensemble_prediction(
                    training_data, 
                    prediction_days,
                    recommended_weights if use_regime_aware else None
                )
            else:
                ensemble_preds, ensemble_conf, model_weights = ensemble_prediction(
                    training_data, 
                    prediction_days
                )
                
            predictions["Ensemble"] = ensemble_preds
            confidence["Ensemble"] = ensemble_conf
            
except Exception as e:
    st.error(f"Error calculating predictions: {str(e)}")
    st.stop()

# Create tabs for different prediction views
if predictions:
    tab1, tab2, tab3 = st.tabs(["Predictions Chart", "Model Comparison", "Prediction Analysis"])
    
    with tab1:
        # Select which model to display
        if len(predictions) > 1:
            # Highlight preferred models based on current regime
            preferred_models = get_preferred_models_for_regime(current_regime)
            model_options = list(predictions.keys())
            
            # Add indicators for regime-preferred models
            model_labels = [
                f"{model} ✓" if model in preferred_models else model 
                for model in model_options
            ]
            
            # Create a mapping from displayed label to actual model name
            model_mapping = {label: model for label, model in zip(model_labels, model_options)}
            
            # Use the enhanced labels for the selectbox
            selected_model_label = st.selectbox(
                "Select Model to Display",
                model_labels,
                index=model_labels.index(f"Ensemble ✓") if "Ensemble ✓" in model_labels else 0
            )
            
            # Get the actual model name from the mapping
            selected_model = model_mapping[selected_model_label]
        else:
            selected_model = list(predictions.keys())[0]
        
        # Plot the selected model's predictions
        fig = plot_predictions(
            training_data, 
            predictions[selected_model], 
            confidence[selected_model],
            prediction_days
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display prediction metrics
        st.subheader("Prediction Metrics")
        
        # Calculate key metrics
        current_price = training_data['Close'].iloc[-1]
        prediction_end_price = predictions[selected_model][-1]
        price_change = prediction_end_price - current_price
        price_change_pct = (price_change / current_price) * 100
        
        # Create columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Current Price", 
                f"${current_price:.2f}"
            )
            st.metric(
                f"Predicted Price ({prediction_days} days)", 
                f"${prediction_end_price:.2f}",
                f"{price_change_pct:.2f}%"
            )
        
        with col2:
            avg_confidence = sum(confidence[selected_model]) / len(confidence[selected_model])
            st.metric("Average Confidence", f"{avg_confidence:.2f}")
            
            # Confidence trend
            conf_trend = confidence[selected_model][-1] - confidence[selected_model][0]
            st.metric("Confidence Trend", f"{conf_trend:.4f}")
        
        with col3:
            # Calculate predicted volatility
            if len(predictions[selected_model]) > 1:
                pred_returns = [
                    (predictions[selected_model][i+1] / predictions[selected_model][i]) - 1 
                    for i in range(len(predictions[selected_model])-1)
                ]
                pred_volatility = np.std(pred_returns) * 100
                st.metric("Predicted Volatility", f"{pred_volatility:.2f}%")
            
            # Signal strength based on confidence, price change, and regime
            # Adjust signal thresholds based on market regime
            if current_regime == "Trending Up":
                # More bullish bias in uptrend
                signal = "Strong Buy" if price_change_pct > 3 and avg_confidence > 0.5 else \
                        "Buy" if price_change_pct > 0 and avg_confidence > 0.4 else \
                        "Strong Sell" if price_change_pct < -5 and avg_confidence > 0.6 else \
                        "Sell" if price_change_pct < 0 and avg_confidence > 0.5 else \
                        "Hold"
            elif current_regime == "Trending Down":
                # More bearish bias in downtrend
                signal = "Strong Buy" if price_change_pct > 7 and avg_confidence > 0.7 else \
                        "Buy" if price_change_pct > 2 and avg_confidence > 0.6 else \
                        "Strong Sell" if price_change_pct < -3 and avg_confidence > 0.5 else \
                        "Sell" if price_change_pct < 0 and avg_confidence > 0.4 else \
                        "Hold"
            elif current_regime == "Range-Bound":
                # Mean reversion bias in range-bound markets
                signal = "Strong Buy" if price_change_pct > 5 and avg_confidence > 0.6 else \
                        "Buy" if price_change_pct > 0 and price_change_pct < 3 and avg_confidence > 0.5 else \
                        "Strong Sell" if price_change_pct < -5 and avg_confidence > 0.6 else \
                        "Sell" if price_change_pct < 0 and price_change_pct > -3 and avg_confidence > 0.5 else \
                        "Hold"
            else:
                # Standard thresholds for unknown regime
                signal = "Strong Buy" if price_change_pct > 5 and avg_confidence > 0.6 else \
                        "Buy" if price_change_pct > 0 and avg_confidence > 0.5 else \
                        "Strong Sell" if price_change_pct < -5 and avg_confidence > 0.6 else \
                        "Sell" if price_change_pct < 0 and avg_confidence > 0.5 else \
                        "Hold"
            
            # Apply color-coding based on signal
            signal_colors = {
                "Strong Buy": "green",
                "Buy": "lightgreen",
                "Hold": "gray",
                "Sell": "pink",
                "Strong Sell": "red"
            }
            
            signal_color = signal_colors.get(signal, "gray")
            st.markdown(f"""
            <div style="background-color: {signal_color}20; padding: 10px; border-radius: 5px; 
                 border: 1px solid {signal_color}; text-align: center;">
                <h3 style="margin: 0; color: {signal_color};">{signal}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        if len(predictions) > 1:
            # Create a plot comparing all models
            fig = go.Figure()
            
            # Add historical price
            fig.add_trace(
                go.Scatter(
                    x=training_data.index,
                    y=training_data['Close'],
                    mode='lines',
                    name='Historical Price',
                    line=dict(color='blue')
                )
            )
            
            # Create date range for predictions
            last_date = training_data.index[-1]
            future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=prediction_days)
            
            # Add predictions for each model
            colors = ['red', 'green', 'purple', 'orange', 'cyan', 'brown']
            
            # Get preferred models for current regime
            preferred_models = get_preferred_models_for_regime(current_regime)
            
            for i, (model_name, preds) in enumerate(predictions.items()):
                color_idx = i % len(colors)
                
                # Use thicker lines for preferred models in current regime
                line_width = 3 if model_name in preferred_models else 1.5
                
                fig.add_trace(
                    go.Scatter(
                        x=future_dates,
                        y=preds,
                        mode='lines',
                        name=model_name + (" ✓" if model_name in preferred_models else ""),
                        line=dict(color=colors[color_idx], width=line_width, dash='dash')
                    )
                )
            
            # Update layout
            fig.update_layout(
                title=f'Model Comparison (Market Regime: {current_regime})',
                xaxis_title='Date',
                yaxis_title='Price',
                template='plotly_white',
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display prediction comparison table
            st.subheader("Prediction Comparison")
            
            # Add a note about preferred models
            st.markdown(f"""
            ✓ = Model recommended for current market regime ({current_regime})
            """)
            
            comparison_data = []
            current_price = training_data['Close'].iloc[-1]
            
            for model_name, preds in predictions.items():
                final_pred = preds[-1]
                pred_change = ((final_pred / current_price) - 1) * 100
                avg_conf = sum(confidence[model_name]) / len(confidence[model_name])
                
                # Mark preferred models
                display_name = f"{model_name} ✓" if model_name in preferred_models else model_name
                
                comparison_data.append({
                    "Model": display_name,
                    f"Price in {prediction_days} days": f"${final_pred:.2f}",
                    "Change": f"{pred_change:.2f}%",
                    "Confidence": f"{avg_conf:.2f}"
                })
            
            st.table(pd.DataFrame(comparison_data))
            
            # Display ensemble weights if available
            if show_ensemble and 'model_weights' in locals():
                st.subheader("Ensemble Model Weights")
                weights_fig = plot_ensemble_weights(model_weights, prediction_days)
                st.plotly_chart(weights_fig, use_container_width=True)
                
                if use_regime_aware:
                    st.markdown("""
                    The chart above shows how each model's contribution is weighted in the ensemble prediction.
                    Weights are determined by a blend of:
                    
                    1. Market regime recommendations (which models work best in current market conditions)
                    2. Individual model confidence for each prediction day
                    3. Time horizon adjustments (some models are better for short-term vs. long-term predictions)
                    """)
                else:
                    st.markdown("""
                    The chart above shows how each model's contribution is weighted in the ensemble prediction.
                    Models with higher confidence for specific prediction days receive higher weights.
                    """)
        else:
            st.info("Please select multiple models for comparison.")
            
    with tab3:
        st.subheader("Prediction Window Analysis")
        
        # Select model for window analysis
        if len(predictions) > 1:
            window_model = st.selectbox(
                "Select Model for Analysis",
                list(predictions.keys()),
                index=list(predictions.keys()).index("Ensemble") if "Ensemble" in predictions else 0,
                key="window_model"
            )
        else:
            window_model = list(predictions.keys())[0]
        
        # Divide the prediction window into segments
        short_term = min(prediction_days // 3, 10)
        medium_term = min(prediction_days // 2, 20)
        
        selected_preds = predictions[window_model]
        current_price = training_data['Close'].iloc[-1]
        
        # Calculate metrics for different time windows
        st.markdown("### Prediction by Time Horizon")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            short_term_price = selected_preds[short_term-1]
            short_term_change = ((short_term_price / current_price) - 1) * 100
            
            st.markdown(f"**Short-term ({short_term} days)**")
            st.metric(
                "Predicted Price", 
                f"${short_term_price:.2f}",
                f"{short_term_change:.2f}%"
            )
            
            # Short-term signal
            short_term_signal = "Strong Buy" if short_term_change > 3 else \
                                "Buy" if short_term_change > 0 else \
                                "Strong Sell" if short_term_change < -3 else \
                                "Sell" if short_term_change < 0 else \
                                "Hold"
            
            st.markdown(f"Signal: **{short_term_signal}**")
            
        with col2:
            medium_term_price = selected_preds[medium_term-1]
            medium_term_change = ((medium_term_price / current_price) - 1) * 100
            
            st.markdown(f"**Medium-term ({medium_term} days)**")
            st.metric(
                "Predicted Price", 
                f"${medium_term_price:.2f}",
                f"{medium_term_change:.2f}%"
            )
            
            # Medium-term signal
            medium_term_signal = "Strong Buy" if medium_term_change > 5 else \
                                "Buy" if medium_term_change > 0 else \
                                "Strong Sell" if medium_term_change < -5 else \
                                "Sell" if medium_term_change < 0 else \
                                "Hold"
                                
            st.markdown(f"Signal: **{medium_term_signal}**")
            
        with col3:
            long_term_price = selected_preds[-1]
            long_term_change = ((long_term_price / current_price) - 1) * 100
            
            st.markdown(f"**Long-term ({prediction_days} days)**")
            st.metric(
                "Predicted Price", 
                f"${long_term_price:.2f}",
                f"{long_term_change:.2f}%"
            )
            
            # Long-term signal
            long_term_signal = "Strong Buy" if long_term_change > 7 else \
                                "Buy" if long_term_change > 0 else \
                                "Strong Sell" if long_term_change < -7 else \
                                "Sell" if long_term_change < 0 else \
                                "Hold"
                                
            st.markdown(f"Signal: **{long_term_signal}**")
        
        # Trajectory analysis
        st.markdown("### Price Trajectory Analysis")
        
        # Calculate pattern type
        if short_term_change > 0 and medium_term_change > 0 and long_term_change > 0:
            if short_term_change < medium_term_change and medium_term_change < long_term_change:
                pattern = "Accelerating Uptrend"
                description = "Price is predicted to rise at an increasing rate."
            elif short_term_change > medium_term_change and medium_term_change > long_term_change:
                pattern = "Decelerating Uptrend"
                description = "Price is predicted to rise but at a decreasing rate."
            else:
                pattern = "Variable Uptrend"
                description = "Price is predicted to rise with variable momentum."
        elif short_term_change < 0 and medium_term_change < 0 and long_term_change < 0:
            if short_term_change > medium_term_change and medium_term_change > long_term_change:
                pattern = "Accelerating Downtrend"
                description = "Price is predicted to fall at an increasing rate."
            elif short_term_change < medium_term_change and medium_term_change < long_term_change:
                pattern = "Decelerating Downtrend"
                description = "Price is predicted to fall but at a decreasing rate."
            else:
                pattern = "Variable Downtrend"
                description = "Price is predicted to fall with variable momentum."
        elif short_term_change > 0 and long_term_change < 0:
            pattern = "Peak Formation"
            description = "Price is predicted to rise in the short term but decline over the long term."
        elif short_term_change < 0 and long_term_change > 0:
            pattern = "Bottoming Pattern"
            description = "Price is predicted to decline in the short term but recover over the long term."
        else:
            pattern = "Mixed Pattern"
            description = "No clear trajectory pattern detected in the predictions."
        
        # Display pattern analysis
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"**Pattern:**")
            st.markdown(f"### {pattern}")
        
        with col2:
            st.markdown(f"**Description:**")
            st.markdown(description)
            
            # Add context based on market regime
            st.markdown(f"""
            **Market Context:**
            This pattern is occurring in a **{current_regime}** market regime, which 
            {"reinforces the pattern signal." if 
             (("Uptrend" in pattern and current_regime == "Trending Up") or 
              ("Downtrend" in pattern and current_regime == "Trending Down") or
              ("Mixed" in pattern and current_regime == "Range-Bound"))
             else "contradicts the current market regime, suggesting a potential regime change."}
            """)
else:
    st.warning("Please select at least one prediction model from the sidebar.")

# Prediction methodology explanation
with st.expander("Prediction Methodology", expanded=False):
    st.markdown("""
    ### How the Prediction Models Work

    1. **Linear Regression**: Fits a straight line to price trend and technical indicators
       - Good for: Capturing general trend direction
       - Limitations: Cannot capture curve patterns
       - Best in: Trending markets with consistent direction
       
    2. **Quadratic Regression**: Fits a curved polynomial to price data
       - Good for: Capturing curved price trends and accelerations
       - Limitations: May overfit or project extreme values
       - Best in: Trending markets with acceleration or deceleration
       
    3. **Fourier Transform**: Decomposes price into frequency components
       - Good for: Identifying cyclical patterns and seasonality
       - Limitations: Requires longer history for best results
       - Best in: Range-bound markets with oscillation patterns
       
    4. **Time Series Analysis**: Statistical approach to analyze time-dependent data
       - Good for: Capturing sequential dependencies in price movements
       - Limitations: More sensitive to recent data
       - Best in: Markets with strong autocorrelation patterns

    5. **ARIMA (AutoRegressive Integrated Moving Average)**: Time series forecasting model
       - Good for: Capturing short-term momentum and seasonality
       - Limitations: Can struggle with long-term forecasts
       - Best in: Both trending and range-bound markets for short horizons
       
    6. **Ensemble Approach**: Combines all models, weighting by confidence and market regime
       - Good for: Balancing strengths and weaknesses of individual models
       - Advantage: Usually more robust than any single model
       - Feature: Adjusts weights based on current market regime for optimal predictions
    """)

    st.markdown("""
    ### Market Regime Detection

    Our system automatically detects the current market regime, which affects how predictions are made:

    1. **Trending Up**: Markets making higher highs and higher lows.
       - Favors: Linear Regression, Time Series, ARIMA

    2. **Trending Down**: Markets making lower highs and lower lows.
       - Favors: Linear/Quadratic Regression, ARIMA

    3. **Range-Bound**: Markets oscillating between support and resistance.
       - Favors: Fourier Transform, Quadratic Regression

    The ensemble model automatically adjusts weights to favor models that historically perform better in the current regime.
    """)

    st.markdown("""
    ### Important Notes

    - These predictions are based on technical analysis and historical patterns
    - Predictions become less reliable as the time horizon extends
    - Unexpected events (earnings, news, market shocks) can invalidate predictions
    - Use these predictions as one tool in your decision-making process, not as definitive forecasts
    """)

# Display training data information
st.sidebar.subheader("Training Data Information")
st.sidebar.info(f"""
Data points: {len(training_data)}
Date range: {training_data.index[0].strftime('%Y-%m-%d')} to {training_data.index[-1].strftime('%Y-%m-%d')}
""")
