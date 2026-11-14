import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from irrigation_logic import irrigation_recommendation

st.set_page_config(
    page_title="Smart Irrigation 3D Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Smart Irrigation & Water Usage Optimization")
st.caption("Interactive 3D farm analytics dashboard powered by MongoDB, Python and Plotly.")

@st.cache_data(ttl=30)
def load_data():
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    collection = client["SmartIrrigationDB"]["FarmData"]
    records = list(collection.find({}, {"_id": 0}))
    client.close()
    return pd.DataFrame(records)

try:
    df = load_data()
except ServerSelectionTimeoutError:
    st.error("Cannot connect to MongoDB. Start the MongoDB Server service, then refresh this page.")
    st.stop()
except Exception as exc:
    st.error(f"Could not load data: {exc}")
    st.stop()

if df.empty:
    st.warning("No farm records found. Run `python database.py` in the project folder first.")
    st.stop()

required_columns = {
    "farm_id", "farm_name", "location", "crop", "soil_moisture",
    "temperature", "humidity", "rainfall", "water_usage", "irrigation_status"
}
missing = required_columns - set(df.columns)
if missing:
    st.error(f"Missing required MongoDB fields: {', '.join(sorted(missing))}")
    st.stop()

df["recommendation"] = df.apply(
    lambda row: irrigation_recommendation(row["soil_moisture"], row["rainfall"]),
    axis=1
)

# Sidebar filters
st.sidebar.header("Dashboard Filters")
locations = ["All"] + sorted(df["location"].dropna().unique().tolist())
selected_location = st.sidebar.selectbox("Farm location", locations)
crops = ["All"] + sorted(df["crop"].dropna().unique().tolist())
selected_crop = st.sidebar.selectbox("Crop type", crops)

filtered = df.copy()
if selected_location != "All":
    filtered = filtered[filtered["location"] == selected_location]
if selected_crop != "All":
    filtered = filtered[filtered["crop"] == selected_crop]

if filtered.empty:
    st.warning("No farms match the selected filters. Choose another filter.")
    st.stop()

st.subheader("Farm overview")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Farms shown", len(filtered))
m2.metric("Average soil moisture", f"{filtered['soil_moisture'].mean():.1f}%")
m3.metric("Average temperature", f"{filtered['temperature'].mean():.1f} °C")
m4.metric("Recorded water usage", f"{filtered['water_usage'].sum():,.0f} L")

st.divider()
st.subheader("🌐 3D Farm Condition Explorer")
st.write("Each point represents one farm. Rotate, zoom, and hover over points to inspect farm conditions.")
fig_3d = px.scatter_3d(
    filtered,
    x="soil_moisture",
    y="temperature",
    z="rainfall",
    color="irrigation_status",
    symbol="crop",
    size="water_usage",
    hover_name="farm_name",
    hover_data=["location", "humidity", "water_usage", "recommendation"],
    labels={
        "soil_moisture": "Soil moisture (%)",
        "temperature": "Temperature (°C)",
        "rainfall": "Rainfall (mm)",
        "irrigation_status": "Recorded irrigation status"
    },
    title="3D Relationship: Soil Moisture, Temperature and Rainfall"
)
fig_3d.update_layout(height=650, margin=dict(l=0, r=0, b=0, t=55))
st.plotly_chart(fig_3d, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("3D Water Usage by Farm")
    fig_water = px.scatter_3d(
        filtered,
        x="soil_moisture",
        y="rainfall",
        z="water_usage",
        color="crop",
        size="temperature",
        hover_name="farm_name",
        hover_data=["location", "irrigation_status"],
        labels={
            "soil_moisture": "Soil moisture (%)",
            "rainfall": "Rainfall (mm)",
            "water_usage": "Water usage (L)"
        },
        title="Water Usage vs Soil Moisture and Rainfall"
    )
    fig_water.update_layout(height=520, margin=dict(l=0, r=0, b=0, t=55))
    st.plotly_chart(fig_water, use_container_width=True)

with right:
    st.subheader("Irrigation Recommendation Summary")
    counts = filtered["recommendation"].value_counts().rename_axis("Recommendation").reset_index(name="Farms")
    fig_pie = px.pie(
        counts, names="Recommendation", values="Farms", hole=0.35,
        title="Farm Count by Recommendation"
    )
    fig_pie.update_layout(height=520, margin=dict(l=0, r=0, b=0, t=55))
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Farm records")
st.dataframe(filtered, use_container_width=True, hide_index=True)

st.info(
    "Learning-project note: the sample records and irrigation thresholds are illustrative, "
    "not validated agricultural advice. Real recommendations need crop, soil, growth-stage, "
    "root-depth and local weather calibration."
)

if st.button("Refresh dashboard data"):
    st.cache_data.clear()
    st.rerun()
