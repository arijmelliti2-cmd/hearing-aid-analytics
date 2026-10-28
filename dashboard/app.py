import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from metrics import weighted_average, weighted_percentage

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Hearing Aid Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("Hearing Aid Analytics Dashboard")
st.caption(
    "Explore synthetic hearing-aid feedback and device metrics "
    "by device model and activity."
)


# --------------------------------------------------
# Database connection
# --------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://analytics_user:local_dev_password"
    "@localhost:5432/hearing_aid",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# --------------------------------------------------
# Load analytics data
# --------------------------------------------------

@st.cache_data(ttl=60)
def load_feedback_data():
    query = text("""
        SELECT
            device_model,
            activity,
            total_events,
            avg_feedback_rating,
            low_feedback_events,
            low_battery_events,
            loud_environment_pct,
            low_feedback_in_loud_environment_pct
        FROM analytics.agg_hearing_aid_feedback
        ORDER BY device_model, activity
    """)

    with engine.connect() as connection:
        return pd.read_sql(query, connection)


try:
    data = load_feedback_data()
except SQLAlchemyError:
    st.error(
        "Could not load analytics data from PostgreSQL. "
        "Check that the database is running and the KPI table "
        "has been built successfully by dbt."
    )
    st.stop()


if data.empty:
    st.warning(
        "The KPI table is empty. Run the dbt pipeline to generate "
        "analytics data."
    )
    st.stop()


# --------------------------------------------------
# Filters
# --------------------------------------------------

st.sidebar.header("Filters")

device_options = sorted(data["device_model"].dropna().unique())
activity_options = sorted(data["activity"].dropna().unique())

selected_devices = st.sidebar.multiselect(
    "Device model",
    options=device_options,
    default=device_options,
)

selected_activities = st.sidebar.multiselect(
    "Activity",
    options=activity_options,
    default=activity_options,
)

filtered = data[
    data["device_model"].isin(selected_devices)
    & data["activity"].isin(selected_activities)
].copy()


if filtered.empty:
    st.info("No records match the selected filters.")
    st.stop()


# --------------------------------------------------
# KPI calculations
# --------------------------------------------------

total_events = int(filtered["total_events"].sum())

weighted_avg_feedback = weighted_average(
    filtered,
    "avg_feedback_rating",
)

weighted_loud_pct = weighted_percentage(
    filtered,
    "loud_environment_pct",
)

weighted_low_feedback_loud_pct = weighted_percentage(
    filtered,
    "low_feedback_in_loud_environment_pct",
)

low_feedback_events = int(filtered["low_feedback_events"].sum())
low_battery_events = int(filtered["low_battery_events"].sum())


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total events",
    f"{total_events:,}",
)

col2.metric(
    "Average feedback",
    f"{weighted_avg_feedback:.2f} / 5",
)

col3.metric(
    "Low-feedback events",
    f"{low_feedback_events:,}",
)

col4.metric(
    "Loud environments",
    f"{weighted_loud_pct:.1f}%",
)


st.divider()


# --------------------------------------------------
# Charts
# --------------------------------------------------

left, right = st.columns(2)

with left:
    st.subheader("Average feedback by device")

    device_chart = (
        filtered.assign(
            weighted_rating=(
                filtered["avg_feedback_rating"]
                * filtered["total_events"]
            )
        )
        .groupby("device_model")
        .agg(
            weighted_rating=("weighted_rating", "sum"),
            total_events=("total_events", "sum"),
        )
    )

    device_chart["average_feedback"] = (
        device_chart["weighted_rating"]
        / device_chart["total_events"]
    )

    st.bar_chart(device_chart["average_feedback"])
    st.caption("Event-weighted average feedback rating.")


with right:
    st.subheader("Average feedback by activity")

    activity_chart = (
        filtered.assign(
            weighted_rating=(
                filtered["avg_feedback_rating"]
                * filtered["total_events"]
            )
        )
        .groupby("activity")
        .agg(
            weighted_rating=("weighted_rating", "sum"),
            total_events=("total_events", "sum"),
        )
    )

    activity_chart["average_feedback"] = (
        activity_chart["weighted_rating"]
        / activity_chart["total_events"]
    )

    st.bar_chart(activity_chart["average_feedback"])
    st.caption("Event-weighted average feedback rating.")


st.divider()


# --------------------------------------------------
# Additional metrics
# --------------------------------------------------

col5, col6 = st.columns(2)

with col5:
    st.subheader("Low-battery events")
    st.metric("Events below the configured threshold", low_battery_events)

with col6:
    st.subheader("Low feedback in loud environments")
    st.metric(
        "Percentage of selected events",
        f"{weighted_low_feedback_loud_pct:.1f}%",
    )


# --------------------------------------------------
# Detailed table
# --------------------------------------------------

st.subheader("Detailed device and activity KPIs")

display_data = filtered.rename(
    columns={
        "device_model": "Device model",
        "activity": "Activity",
        "total_events": "Total events",
        "avg_feedback_rating": "Average feedback",
        "low_feedback_events": "Low-feedback events",
        "low_battery_events": "Low-battery events",
        "loud_environment_pct": "Loud environment (%)",
        "low_feedback_in_loud_environment_pct":
            "Low feedback in loud environment (%)",
    }
)

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Data is synthetic and intended for portfolio demonstration. "
    "Metrics and thresholds are illustrative, not clinical guidance."
)

if st.button("Refresh data"):
    load_feedback_data.clear()
    st.rerun()