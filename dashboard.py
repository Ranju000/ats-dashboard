import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# ---------------------------
# MySQL connection
# ---------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rockstar@000",
        database="ranjudb"
    )

# ---------------------------
# Load data from DB
# ---------------------------
@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM `nov submissions 2025_2025`", conn)
    conn.close()

    # Replace NULL with 0 for calculations
    df = df.fillna(0)
    return df

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("📊 Monthly Submissions Dashboard")
st.write("Dashboard generated from MySQL attendance table")

df = load_data()

# ---------------------------
# Filters
# ---------------------------
st.sidebar.header("Filters")

all_employees = df["name"].unique()
selected_employee = st.sidebar.selectbox("Select Employee", ["All"] + list(all_employees))

all_weeks = df["week"].unique()
selected_week = st.sidebar.selectbox("Select Week", ["All"] + list(all_weeks))

filtered = df.copy()

if selected_employee != "All":
    filtered = filtered[filtered["name"] == selected_employee]

if selected_week != "All":
    filtered = filtered[filtered["week"] == selected_week]

# ---------------------------
# Data Preview
# ---------------------------
st.subheader("📋 Filtered Data")
st.dataframe(filtered)

# ---------------------------
# Daily Hours Chart
# ---------------------------
if not filtered.empty:
    st.subheader("📈 November_Submission_2025")

    daily_df = filtered.melt(
        id_vars=["name", "week"],
        value_vars=["mon", "tue", "wed", "thu", "fri"],
        var_name="day",
        value_name="hours"
    )

    fig = px.bar(
        daily_df,
        x="day",
        y="hours",
        color="week",
        title="Daily Hours Per Week"
    )
    st.plotly_chart(fig)

# ---------------------------
# Weekly Total Chart
# ---------------------------
st.subheader("📅 November_Submission_2025")

fig2 = px.bar(
    filtered,
    x="week",
    y="weekly_total",
    color="name",
    title="Weekly Total Submissions"
)
st.plotly_chart(fig2)

# ---------------------------
# Export filtered data
# ---------------------------
st.subheader("⬇ Export Data")

st.download_button(
    label="Download as CSV",
    data=filtered.to_csv(index=False),
    file_name="filtered_hours.csv",
    mime="text/csv"
)
