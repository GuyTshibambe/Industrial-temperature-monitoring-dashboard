import streamlit as st
import pandas as pd
from pathlib import Path

from db_utils import (
    get_all_readings,
    get_summary_stats,
    get_overheat_count,
    get_machine_ids,
)

st.set_page_config(
    page_title = "Industrial Temperature Monitor",
    layout="wide"
)

st.title("Industrial Temperature Monitoring Dashboard")
st.write("Project 02 - Built on  top of Industrial Data Project 01")

#Sidebar controls
st.sidebar.header("Controls")

threhold = st.sidebar.slider(
    "Overheat threhold (oC)",
    min_value=30.0,
    max_value=50.0,
    value=38.0,
    step=0.5,
)

machine_filter = st.sidebar.selectbox(
    "Filter by machine",
    options=["ALL"] + get_machine_ids()
)

refresh = st.sidebar.button("Refresh data")

#Load data
df = get_all_readings()
df["timestamp"] = pd.to_datetime(df["timestamp"])

if machine_filter != "ALL":
    df = df[df["machine_id"] == machine_filter] 

summary = get_summary_stats()
overheat_count = get_overheat_count(threhold=threhold)

#Top metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total readings", summary["total_readings"])
col2.metric("Min temp (oC)", f"{summary['min_temp']:.2f}")
col3.metric("Max temp (oC)", f"{summary['max_temp']:.2f}")
col4.metric("Avg temp (oC)", f"{summary['avg_temp']:.2f}")

st.subheader("Temperature Over Time")

df_sorted = df.sort_values("timestamp")
st.line_chart(
    df_sorted.set_index("timestamp")["temperature_c"],
    height=400
)

#Overheat table
st.subheader(f"Overheat Event (temperature > {threhold}oC)")
overheat_df = df[df["temperature_c"] >threhold]

st.write(f"Total overheat events: **{len(overheat_df)}**")

if not overheat_df.empty:
    st.dataframe(
        overheat_df[["timestamp","machine_id","temperature_c"]]
        .sort_values("temperature_c", ascending=False)
        .reset_index(drop=True)
    )
else:
    st.info("No overheat events detected at this threshold.")

st.markdown("---")
st.caption("Industrial Data Project 02 - Powered by Python,SQLite, Streamlit.")