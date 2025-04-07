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
    ensemble_prediction,
    plot_predictions,
    plot_ensemble_weights
)

# Set page configuration
st.set_page_config(
    page_title="Prediction Models - Stock Market Analysis Platform",
    page_icon="📈",
    layout="wide"
)

st.title("Prediction Models")
st.markdown("Stock price prediction using multiple models and ensemble approach.")

# Check if stock data exists in session state
if 'stock_data' not in st.session_state or st.session_state.stock_data is None:
    st.warning("Please select a stock from the home page first.")
    st.stop()

# Get stock data from session state
stock_data = st.session_state.stock_data
stock_symbol = st.session_state.selected_stock

# Sidebar controls
st.sidebar.header("Prediction Settings")

# Prediction days selection
prediction_days = st.sidebar.slider(
    "Prediction Days", 
    min_value=5, 
    max_value=60, 
    value=30,
    step=5
)

# Model selection
st.sidebar.subheader("Select Models")
show_linear = st.sidebar.checkbox("Linear Regression", value=True)
show_quadratic = st.sidebar.checkbox("Quadratic Regression", value=True)
show_fourier = st.sidebar.checkbox("Fourier Transform", value=True)
show_time_series = st.sidebar.checkbox("Time Series Analysis", value=True)
show_ensemble = st.sidebar.checkbox("Ensemble Model", value=True)

# Training period selection
training_period = st.sidebar.selectbox(
    "Training Data Period",
    ["Full History", "1 Year", "6 Months", "3 Months"]
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

    if show_ensemble:
        with st.spinner("Calculating Ensemble predictions..."):
            ensemble_preds, ensemble_conf, model_weights = ensemble_prediction(training_data, prediction_days)
            predictions["Ensemble"] = ensemble_preds
            confidence["Ensemble"] = ensemble_conf
            
except Exception as e:
    st.error(f"Error calculating predictions: {str(e)}")
    st.stop()

# Create tabs for different prediction views
if predictions:
    tab1, tab2 = st.tabs(["Predictions Chart", "Model Comparison"])
    
    with tab1:
        # Select which model to display
        if len(predictions) > 1:
            selected_model = st.selectbox(
                "Select Model to Display",
                list(predictions.keys())
            )
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
            
            # Signal strength based on confidence and price change
            signal_strength = abs(price_change_pct) * avg_confidence
            signal = "Strong Buy" if price_change_pct > 5 and avg_confidence > 0.6 else \
                    "Buy" if price_change_pct > 0 and avg_confidence > 0.5 else \
                    "Strong Sell" if price_change_pct < -5 and avg_confidence > 0.6 else \
                    "Sell" if price_change_pct < 0 and avg_confidence > 0.5 else \
                    "Hold"
            
            st.metric("Signal", signal)
    
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
            colors = ['red', 'green', 'purple', 'orange', 'cyan']
            
            for i, (model_name, preds) in enumerate(predictions.items()):
                color_idx = i % len(colors)
                
                fig.add_trace(
                    go.Scatter(
                        x=future_dates,
                        y=preds,
                        mode='lines',
                        name=model_name,
                        line=dict(color=colors[color_idx], dash='dash')
                    )
                )
            
            # Update layout
            fig.update_layout(
                title='Model Comparison',
                xaxis_title='Date',
                yaxis_title='Price',
                template='plotly_white',
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display prediction comparison table
            st.subheader("Prediction Comparison")
            
            comparison_data = []
            current_price = training_data['Close'].iloc[-1]
            
            for model_name, preds in predictions.items():
                final_pred = preds[-1]
                pred_change = ((final_pred / current_price) - 1) * 100
                avg_conf = sum(confidence[model_name]) / len(confidence[model_name])
                
                comparison_data.append({
                    "Model": model_name,
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
                
                st.markdown("""
                The chart above shows how each model's contribution is weighted in the ensemble prediction.
                Models with higher confidence for specific prediction days receive higher weights.
                """)
        else:
            st.info("Please select multiple models for comparison.")
else:
    st.warning("Please select at least one prediction model from the sidebar.")

# Prediction methodology explanation
st.subheader("Prediction Methodology")

st.markdown("""
### How the Prediction Models Work

1. **Linear Regression**: Fits a straight line to price trend and technical indicators
   - Good for: Capturing general trend direction
   - Limitations: Cannot capture curve patterns
   
2. **Quadratic Regression**: Fits a curved polynomial to price data
   - Good for: Capturing curved price trends and accelerations
   - Limitations: May overfit or project extreme values
   
3. **Fourier Transform**: Decomposes price into frequency components
   - Good for: Identifying cyclical patterns and seasonality
   - Limitations: Requires longer history for best results
   
4. **Time Series Analysis**: Statistical approach to analyze time-dependent data
   - Good for: Capturing sequential dependencies in price movements
   - Limitations: More sensitive to recent data

5. **Ensemble Approach**: Combines all models, weighting by confidence
   - Good for: Balancing strengths and weaknesses of individual models
   - Advantage: Usually more robust than any single model
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
