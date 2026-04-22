import streamlit as st
import plotly.express as px
from src.data_pipeline import fetch_and_clean_eia_data
from src.forecasting import generate_forecast
from src.ai_agent import get_ai_investment_brief

st.set_page_config(page_title="Energy Intelligence", layout="wide")

# API Key from secrets
api_key = st.secrets.get("EIA_API_KEY", None)

if not api_key:
    st.error("API key missing. Add to secrets.toml")
    st.stop()

st.title("⚡ Energy Intelligence System")
st.caption("Oil & Gas Investment Decision Platform")

year = st.slider("Select Forecast Year", 2024, 2035, 2026)

df = fetch_and_clean_eia_data(api_key)

if df.empty:
    st.error("No data fetched")
    st.stop()

forecast_df = generate_forecast(df, year)

# KPI
top = forecast_df.loc[forecast_df['Projected_Production'].idxmax()]
avg = forecast_df['Projected_Production'].mean()

c1, c2, c3 = st.columns(3)
c1.metric("Top Region", top['Region'])
c2.metric("Avg Production", f"{int(avg):,}")
c3.metric("Year", year)

# Chart
fig = px.bar(forecast_df, x="Region", y="Projected_Production", color="Projected_Production")
st.plotly_chart(fig, use_container_width=True)

# AI Insight
st.subheader("🤖 Investment Insight")
st.markdown(get_ai_investment_brief(forecast_df, year))