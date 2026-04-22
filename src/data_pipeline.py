import pandas as pd
import requests
import streamlit as st

@st.cache_data
def fetch_and_clean_eia_data(api_key):
    url = f"https://api.eia.gov/v2/petroleum/crd/crpdn/data/?api_key={api_key}&frequency=annual&data[0]=value"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or 'response' not in data:
        return pd.DataFrame()

    records = data['response'].get('data', [])
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    area_col = 'area-name' if 'area-name' in df.columns else 'areaName'

    df = df[['period', area_col, 'value']].copy()
    df.columns = ['Year', 'Region', 'Production_Volume']

    df['Year'] = df['Year'].astype(int)
    df['Production_Volume'] = pd.to_numeric(df['Production_Volume']).fillna(0)

    df = df[~df['Region'].isin(['U.S.', 'United States', 'U.S. Total'])]

    return df