import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def generate_forecast(df, target_year):
    """Uses Linear Regression to project volumes for a future year."""
    forecast_results = []
    regions = df['Region'].unique()
    
    for region in regions:
        region_data = df[df['Region'] == region].copy()
        
        if len(region_data) < 2:
            continue
            
        # Machine Learning Logic
        X = region_data['Year'].values.reshape(-1, 1)
        y = region_data['Production_Volume'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict for the specific slider-selected year
        prediction = model.predict([[target_year]])[0]
        
        forecast_results.append({
            'Region': region,
            'Selected_Year': target_year,
            'Projected_Production': max(0, prediction)
        })
        
    return pd.DataFrame(forecast_results)