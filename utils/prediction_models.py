import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import numpy.polynomial.polynomial as poly
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from scipy.fft import fft, ifft
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_features(data, window_sizes=[5, 10, 20, 30]):
    """
    Create technical features for prediction models.
    
    Args:
        data (pd.DataFrame): Stock data DataFrame
        window_sizes (list): List of window sizes for rolling features
        
    Returns:
        pd.DataFrame: DataFrame with added features
    """
    df = data.copy()
    
    # Calculate returns
    df['Returns'] = df['Close'].pct_change()
    
    # Add moving averages
    for window in window_sizes:
        df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
        df[f'EMA_{window}'] = df['Close'].ewm(span=window, adjust=False).mean()
    
    # Add rolling statistics
    for window in window_sizes:
        df[f'Std_{window}'] = df['Close'].rolling(window=window).std()
        df[f'Min_{window}'] = df['Close'].rolling(window=window).min()
        df[f'Max_{window}'] = df['Close'].rolling(window=window).max()
    
    # Add price momentum
    for window in window_sizes:
        df[f'Momentum_{window}'] = df['Close'] - df['Close'].shift(window)
    
    # Add volume features
    df['Volume_Change'] = df['Volume'].pct_change()
    for window in window_sizes:
        df[f'Volume_SMA_{window}'] = df['Volume'].rolling(window=window).mean()
    
    # Add volatility
    df['Daily_Range'] = df['High'] - df['Low']
    for window in window_sizes:
        df[f'Range_SMA_{window}'] = df['Daily_Range'].rolling(window=window).mean()
    
    # Drop rows with NaN values (from rolling calculations)
    df = df.dropna()
    
    return df

def linear_regression_prediction(data, prediction_days=30):
    """
    Linear regression prediction model.
    
    Args:
        data (pd.DataFrame): Stock data DataFrame
        prediction_days (int): Number of days to predict forward
        
    Returns:
        tuple: (predictions, confidence)
    """
    # Create features
    df = create_features(data)
    
    # Create target variable (next day's close price)
    df['Target'] = df['Close'].shift(-1)
    df = df.dropna()
    
    # Select features and target
    features = [col for col in df.columns if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'Target']]
    X = df[features]
    y = df['Target']
    
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train linear regression model
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Prepare prediction data
    last_data_point = X.iloc[-1].values.reshape(1, -1)
    last_data_point_scaled = scaler.transform(last_data_point)
    
    # Make predictions
    predictions = []
    confidence = []
    last_prediction = df['Close'].iloc[-1]
    
    for _ in range(prediction_days):
        # Update features with last prediction
        prediction_input = last_data_point_scaled.copy()
        next_pred = model.predict(prediction_input)[0]
        
        # Store prediction
        predictions.append(next_pred)
        
        # Calculate confidence based on R-squared
        confidence.append(model.score(X_scaled, y))
        
        # Update last prediction for next iteration
        last_prediction = next_pred
    
    return predictions, confidence

def quadratic_regression_prediction(data, prediction_days=30):
    """
    Quadratic regression prediction model.
    
    Args:
        data (pd.DataFrame): Stock data DataFrame
        prediction_days (int): Number of days to predict forward
        
    Returns:
        tuple: (predictions, confidence)
    """
    # Use price data for polynomial regression
    y = data['Close'].values
    x = np.arange(len(y))
    
    # Fit quadratic polynomial
    coeffs = poly.polyfit(x, y, 2)
    
    # Calculate R-squared for confidence
    model = poly.Polynomial(coeffs)
    y_pred = model(x)
    ss_tot = np.sum((y - np.mean(y))**2)
    ss_res = np.sum((y - y_pred)**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # Predict future values
    future_x = np.arange(len(y), len(y) + prediction_days)
    predictions = model(future_x)
    
    # Use R-squared as confidence
    confidence = [r_squared] * prediction_days
    
    return predictions, confidence

def fourier_transform_prediction(data, prediction_days=30, harmonics=10):
    """
    Fourier transform prediction model.
    
    Args:
        data (pd.DataFrame): Stock data DataFrame
        prediction_days (int): Number of days to predict forward
        harmonics (int): Number of harmonics to include
        
    Returns:
        tuple: (predictions, confidence)
    """
    # Get close prices
    prices = data['Close'].values
    
    # Compute FFT
    fft_result = fft(prices)
    
    # Keep only the most significant harmonics
    fft_result_filtered = np.copy(fft_result)
    fft_result_filtered[harmonics:-harmonics] = 0
    
    # Inverse FFT to get the filtered time series
    filtered_prices = ifft(fft_result_filtered).real
    
    # Calculate R-squared for confidence
    ss_tot = np.sum((prices - np.mean(prices))**2)
    ss_res = np.sum((prices - filtered_prices)**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # Extend the time series
    n = len(prices)
    extended_time = np.arange(0, n + prediction_days)
    t = np.arange(0, n)
    
    # Fit a polynomial to the filtered data
    degree = min(5, len(prices) // 10)  # Avoid overfitting
    poly_coeffs = np.polyfit(t, filtered_prices, degree)
    poly_model = np.poly1d(poly_coeffs)
    
    # Generate predictions
    predictions = poly_model(np.arange(n, n + prediction_days))
    
    # Adjust confidence based on length of prediction
    confidence = [r_squared * np.exp(-0.05 * i) for i in range(prediction_days)]
    
    return predictions, confidence

def time_series_prediction(data, prediction_days=30):
    """
    Time series prediction model (statistical approach to LSTM).
    
    Args:
        data (pd.DataFrame): Stock data DataFrame
        prediction_days (int): Number of days to predict forward
        
    Returns:
        tuple: (predictions, confidence)
    """
    # Create features
    df = create_features(data)
    
    # Create target variable (next day's close price)
    df['Target'] = df['Close'].shift(-1)
    df = df.dropna()
    
    # Select features and target
    features = [col for col in df.columns if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'Target']]
    X = df[features]
    y = df['Target']
    
    # Create lagged features to capture time series patterns
    for i in range(1, 6):
        X[f'Close_Lag_{i}'] = df['Close'].shift(i)
    
    # Drop rows with NaN values
    X = X.dropna()
    y = y.iloc[X.index]
    
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train linear regression model
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Make predictions
    predictions = []
    confidence = []
    last_x = X.iloc[-1:].copy()
    last_price = df['Close'].iloc[-1]
    
    for i in range(prediction_days):
        # Update lagged features for prediction
        for lag in range(5, 0, -1):
            if i >= lag:
                last_x[f'Close_Lag_{lag}'] = predictions[i - lag]
            elif lag > 1:
                last_x[f'Close_Lag_{lag}'] = last_x[f'Close_Lag_{lag-1}']
        
        # Scale the input
        x_scaled = scaler.transform(last_x)
        
        # Predict next value
        pred = model.predict(x_scaled)[0]
        predictions.append(pred)
        
        # Calculate declining confidence
        conf = model.score(X_scaled, y) * np.exp(-0.05 * i)
        confidence.append(conf)
    
    return predictions, confidence

def ensemble_prediction(data, prediction_days=30):
    """
    Ensemble prediction using multiple models with dynamic weighting.
    
    Args:
        data (pd.DataFrame): Stock data DataFrame
        prediction_days (int): Number of days to predict forward
        
    Returns:
        tuple: (predictions, confidence, model_weights)
    """
    # Get predictions from individual models
    linear_preds, linear_conf = linear_regression_prediction(data, prediction_days)
    quad_preds, quad_conf = quadratic_regression_prediction(data, prediction_days)
    fourier_preds, fourier_conf = fourier_transform_prediction(data, prediction_days)
    time_series_preds, time_series_conf = time_series_prediction(data, prediction_days)
    
    # Normalize confidence scores to use as weights
    model_weights = []
    predictions = []
    confidence = []
    
    for i in range(prediction_days):
        # Get confidence scores for this prediction day
        day_confs = [linear_conf[i], quad_conf[i], fourier_conf[i], time_series_conf[i]]
        
        # Normalize weights
        total_conf = sum(day_confs)
        if total_conf > 0:
            weights = [conf / total_conf for conf in day_confs]
        else:
            weights = [0.25, 0.25, 0.25, 0.25]  # Equal weights if all confidences are 0
        
        # Calculate weighted prediction
        day_preds = [linear_preds[i], quad_preds[i], fourier_preds[i], time_series_preds[i]]
        weighted_pred = sum(p * w for p, w in zip(day_preds, weights))
        
        # Store results
        predictions.append(weighted_pred)
        confidence.append(max(day_confs))  # Overall confidence is the highest of individual models
        model_weights.append(weights)
    
    return predictions, confidence, model_weights

def plot_predictions(data, predictions, confidence, prediction_days=30):
    """
    Create a plot showing historical data and predictions.
    
    Args:
        data (pd.DataFrame): Stock data DataFrame
        predictions (list): List of predicted values
        confidence (list): List of confidence values
        prediction_days (int): Number of days predicted
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure with predictions
    """
    # Create date range for predictions
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=prediction_days)
    
    # Create figure
    fig = go.Figure()
    
    # Add historical price
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Historical Price',
            line=dict(color='blue')
        )
    )
    
    # Add predictions
    fig.add_trace(
        go.Scatter(
            x=future_dates,
            y=predictions,
            mode='lines',
            name='Prediction',
            line=dict(color='red', dash='dash')
        )
    )
    
    # Add confidence interval
    upper_bound = [pred + pred * (1 - conf) * 0.2 for pred, conf in zip(predictions, confidence)]
    lower_bound = [pred - pred * (1 - conf) * 0.2 for pred, conf in zip(predictions, confidence)]
    
    fig.add_trace(
        go.Scatter(
            x=future_dates,
            y=upper_bound,
            mode='lines',
            name='Upper Bound',
            line=dict(width=0),
            showlegend=False
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=future_dates,
            y=lower_bound,
            mode='lines',
            name='Lower Bound',
            fill='tonexty',
            fillcolor='rgba(255, 0, 0, 0.1)',
            line=dict(width=0),
            showlegend=False
        )
    )
    
    # Update layout
    fig.update_layout(
        title='Stock Price Prediction',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        height=600
    )
    
    return fig

def plot_ensemble_weights(model_weights, prediction_days=30):
    """
    Create a plot showing model weights in the ensemble.
    
    Args:
        model_weights (list): List of weight distributions
        prediction_days (int): Number of days predicted
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure with model weights
    """
    # Create arrays for each model's weights
    linear_weights = [weights[0] for weights in model_weights]
    quadratic_weights = [weights[1] for weights in model_weights]
    fourier_weights = [weights[2] for weights in model_weights]
    time_series_weights = [weights[3] for weights in model_weights]
    
    # Create figure
    fig = go.Figure()
    
    # Add traces for each model's weights
    days = list(range(1, prediction_days + 1))
    
    fig.add_trace(
        go.Scatter(
            x=days,
            y=linear_weights,
            mode='lines+markers',
            name='Linear Regression',
            line=dict(width=2, color='blue')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=days,
            y=quadratic_weights,
            mode='lines+markers',
            name='Quadratic Regression',
            line=dict(width=2, color='red')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=days,
            y=fourier_weights,
            mode='lines+markers',
            name='Fourier Transform',
            line=dict(width=2, color='green')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=days,
            y=time_series_weights,
            mode='lines+markers',
            name='Time Series',
            line=dict(width=2, color='purple')
        )
    )
    
    # Update layout
    fig.update_layout(
        title='Model Weights in Ensemble Prediction',
        xaxis_title='Prediction Day',
        yaxis_title='Weight',
        template='plotly_white',
        height=400
    )
    
    return fig
