import pandas as pd
from sklearn.ensemble import RandomForestRegressor
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
    # Data preprocessing
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
    data = data.ffill()

    X = data.drop(columns=[analyze, 'adj_price', 'next_quarter'])
    y = data[analyze]

    # Train/test split
    X_train, y_train = X[:-months_ahead], y[:-months_ahead]

    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    last_known_date = X.index[-1]
    future_dates = pd.date_range(last_known_date, periods=months_ahead + 1, freq='ME')[1:]
    future_data = X.loc[last_known_date:last_known_date].reindex(future_dates)

    future_predictions = model.predict(future_data)

    return future_predictions, model.score(X_train, y_train)

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

