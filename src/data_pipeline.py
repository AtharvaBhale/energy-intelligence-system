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

    # Detect correct column name
    area_col = 'area-name' if 'area-name' in df.columns else 'areaName'

    # Select and rename
    df = df[['period', area_col, 'value']].copy()
    df.columns = ['Year', 'Region', 'Production_Volume']

    # 🔥 ADD PADD MAPPING HERE (CORRECT PLACE)
    PADD_MAP = {
        "PADD 1": "East Coast",
        "PADD 2": "Midwest",
        "PADD 3": "Texas & Gulf Coast",
        "PADD 4": "Rocky Mountains",
        "PADD 5": "West Coast"
    }

    df['Region'] = df['Region'].replace(PADD_MAP)

    # Convert types safely
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Production_Volume'] = pd.to_numeric(df['Production_Volume'], errors='coerce')

    # 🚨 Remove missing values
    df = df.dropna(subset=['Year', 'Region', 'Production_Volume'])

    # 🚨 Remove empty strings (just in case)
    df = df[df['Region'].str.strip() != ""]

    # 🚨 Remove national totals
    df = df[~df['Region'].isin(['U.S.', 'United States', 'U.S. Total'])]

    # 🚨 Remove duplicates
    df = df.drop_duplicates()

    # 🚨 Remove negative values
    df = df[df['Production_Volume'] >= 0]

    # Sort
    df = df.sort_values(['Region', 'Year'])

    # Remove bad data
    df = df.dropna()
    df = df[df['Production_Volume'] >= 0]

    # Remove national totals
    df = df[~df['Region'].isin(['U.S.', 'United States', 'U.S. Total'])]

    return df


def save_raw_data_to_excel(api_key):
    url = f"https://api.eia.gov/v2/petroleum/crd/crpdn/data/?api_key={api_key}&frequency=annual&data[0]=value"

    response = requests.get(url)
    data = response.json()

    records = data['response']['data']
    df = pd.DataFrame(records)

    df.to_excel("raw_eia_data.xlsx", index=False)

    return df