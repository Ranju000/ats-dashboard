import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# Load CSV (No MySQL)
# ------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/Nov_Month_Submission.csv")
    # Fill empty with 0 for numerical columns
    df = df.fillna(0)
    return df

# ------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------
st.title("📊 Monthly Submissions Dashboard")
st.write("Dashboard generated from CSV file (Nov Month Submission)")

df = load_data()

# ------------------------------------------------------------
# Filters
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# Show filtered data
# ------------------------------------------------------------
st.subheader("📋 Filtered Data")
st.dataframe(filtered)

# ------------------------------------------------------------
# Daily Hours Chart
# ------------------------------------------------------------
if not filtered.empty:
    st.subheader("📈 Daily Submission (Nov 2025)")

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

# ------------------------------------------------------------
# Weekly Total Chart
# ------------------------------------------------------------
st.subheader("📅 Monthly Total Submissions")

if "weekly_total" in filtered.columns:
    fig2 = px.bar(
        filtered,
        x="week",
        y="weekly_total",
        color="name",
        title="Monthly Total Submissions"
    )
    st.plotly_chart(fig2)
else:
    st.warning("⚠ 'weekly_total' column not found in CSV")

# ------------------------------------------------------------
# Export filtered data
# ------------------------------------------------------------
st.subheader("⬇ Export Data")

st.download_button(
    label="Download as CSV",
    data=filtered.to_csv(index=False),
    file_name="filtered_hours.csv",
    mime="text/csv"
)
