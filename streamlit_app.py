import streamlit as st
import plotly.express as px
import pandas as pd

from src.data_pipeline import fetch_and_clean_eia_data
from src.forecasting import generate_forecast
from src.ai_agent import get_ai_investment_brief, chatbot_response

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Energy Intelligence", layout="wide")

# ---------------- API KEY ----------------
api_key = st.secrets.get("EIA_API_KEY")

if not api_key:
    st.error("API key missing")
    st.stop()

# ---------------- TITLE ----------------
st.title("⚡ Energy Intelligence System")
st.caption("AI-Powered Oil & Gas Investment Decision Platform")

# ---------------- YEAR ----------------
year = st.slider("Select Forecast Year", 2024, 2035, 2027)

# ---------------- DATA ----------------
df = fetch_and_clean_eia_data(api_key)

if df.empty:
    st.error("No data available")
    st.stop()

forecast_df = generate_forecast(df, year)

# ---------------- MAP DATA ----------------
PADD_COORDS = {
    "East Coast": (40.0, -75.0),
    "Midwest": (41.5, -93.0),
    "Texas & Gulf Coast": (29.0, -95.0),
    "Rocky Mountains": (39.0, -107.0),
    "West Coast": (36.0, -120.0)
}

# Add coordinates
forecast_df["lat"] = forecast_df["Region"].map(lambda x: PADD_COORDS.get(x, (0,0))[0])
forecast_df["lon"] = forecast_df["Region"].map(lambda x: PADD_COORDS.get(x, (0,0))[1])

# ---------------- KPI ----------------
top = forecast_df.loc[forecast_df['Projected_Production'].idxmax()]
avg = forecast_df['Projected_Production'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("🏆 Best Region", top['Region'])
col2.metric("📊 Avg Production", f"{int(avg):,}")
col3.metric("📅 Year", year)

# ---------------- MAP ----------------
st.subheader("🗺️ Regional Production Map")

fig_map = px.scatter_mapbox(
    forecast_df,
    lat="lat",
    lon="lon",
    size="Projected_Production",
    color="Projected_Production",
    hover_name="Region",
    zoom=3,
    height=500
)

fig_map.update_layout(mapbox_style="open-street-map")

selected = st.plotly_chart(fig_map, use_container_width=True)

# ---------------- CHART ----------------
st.subheader("📊 Production by Region")

fig = px.bar(
    forecast_df.sort_values("Projected_Production", ascending=False),
    x="Region",
    y="Projected_Production",
    color="Projected_Production"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- TABLE ----------------
st.subheader("📋 Detailed Data")

st.dataframe(forecast_df, use_container_width=True)

# ---------------- AI INSIGHT ----------------
st.subheader("🤖 Investment Insight")

st.markdown(get_ai_investment_brief(forecast_df, year))

# ---------------- CHATBOT ----------------
st.subheader("💬 Ask the System")

question = st.text_input("Ask about regions, growth, risk, etc.")

if question:
    response = chatbot_response(question, forecast_df, year)
    st.success(response)