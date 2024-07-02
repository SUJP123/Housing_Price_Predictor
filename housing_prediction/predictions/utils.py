import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import seaborn as sns
import base64
from io import BytesIO
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message=".*GUI is implemented.*")

def preprocess_data(data):
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values('date')
    data = data.ffill()
    return data

def create_features(data):
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year
    return data[['interest', 'vacancy', 'cpi', 'month', 'year']], data['price']

def train_and_predict(data, months_ahead, analyze):
    try:
        # Data preprocessing
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date')
        data = data.ffill()  # Forward fill missing values

        # Feature engineering
        data['month'] = data.index.month
        data['quarter'] = data.index.quarter
        data['year'] = data.index.year

        # Define features and target
        X = data.drop(columns=[analyze, 'adj_price', 'next_quarter'])
        y = data[analyze]

        # Train/test split
        X_train, y_train = X[:-months_ahead], y[:-months_ahead]

        # Model training with cross-validation
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        tscv = TimeSeriesSplit(n_splits=5)
        cv_scores = cross_val_score(model, X_train, y_train, cv=tscv, scoring='r2')
        model.fit(X_train, y_train)

        # Generate future data for prediction
        last_known_date = X.index[-1]
        future_dates = pd.date_range(last_known_date, periods=months_ahead + 1, freq='MS')[1:]

        # Create future data with the same structure as training data
        future_data = pd.DataFrame(index=future_dates)
        future_data['month'] = future_data.index.month
        future_data['quarter'] = future_data.index.quarter
        future_data['year'] = future_data.index.year

        # Initialize other columns with the last known values
        for col in X.columns:
            if col not in ['month', 'quarter', 'year']:
                future_data[col] = X[col].iloc[-1]

        # Ensure the future_data has the same columns as X_train in the same order
        future_data = future_data[X_train.columns]

        # Make predictions
        future_predictions = model.predict(future_data)

        return future_predictions, cv_scores.mean()

    except Exception as e:
        # Log the error for debugging
        print(f"Error in train_and_predict: {e}")
        return None, None

def generate_analysis(data, analysis_field):
    # Filter data for the analysis field
    analysis_data = data[analysis_field].dropna()
    
    # Generate descriptive statistics
    description = analysis_data.describe().to_dict()
    
    # Generate the plot
    plt.figure(figsize=(7, 4))
    sns.histplot(analysis_data, kde=True)
    plt.title(f'Distribution of {analysis_field}')
    plt.xlabel(analysis_field)
    plt.ylabel('Frequency')
    
    # Save plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Convert plot to base64
    plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    
    return {
        'description': description,
        'plot': plot_base64
    }

def generateOverTimePlot(data, analysis_field):
    analysis_data = data[analysis_field].dropna()
    dates = data['date']

    plt.figure(figsize=(7, 4))
    plt.plot(dates, analysis_data)
    plt.xlabel('Year')
    plt.ylabel(analysis_field)
    plt.title(f"Plot of {analysis_field} over time")

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Convert plot to base64
    plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return {
        'plot1': plot_base64
    }

