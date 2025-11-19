import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from database.service import DatabaseService

st.set_page_config(page_title="Audit Dashboard", layout="wide")

db = DatabaseService()

st.title("🔍 Audit & Activity Dashboard")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    days = st.selectbox("Time Range", [1, 7, 30, 90], index=1)
with col2:
    action_filter = st.multiselect("Action Type", ["CREATE", "UPDATE", "DELETE", "LOGIN", "EXPORT"])
with col3:
    user_filter = st.text_input("User Filter")

# Fetch audit logs
start_date = datetime.now() - timedelta(days=days)
logs = db.get_audit_logs(start_date=start_date, actions=action_filter, user=user_filter)

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Actions", len(logs))
col2.metric("Unique Users", logs['user'].nunique() if len(logs) > 0 else 0)
col3.metric("Failed Actions", len(logs[logs['status'] == 'FAILED']) if len(logs) > 0 else 0)
col4.metric("Success Rate", f"{(len(logs[logs['status'] == 'SUCCESS']) / len(logs) * 100):.1f}%" if len(logs) > 0 else "0%")

# Activity Timeline
st.subheader("Activity Timeline")
if len(logs) > 0:
    timeline = logs.groupby(logs['timestamp'].dt.date).size().reset_index(name='count')
    fig = px.line(timeline, x='timestamp', y='count', title="Daily Activity")
    st.plotly_chart(fig, use_container_width=True)

# Action Distribution
col1, col2 = st.columns(2)
with col1:
    st.subheader("Actions by Type")
    if len(logs) > 0:
        action_dist = logs['action'].value_counts()
        fig = px.pie(values=action_dist.values, names=action_dist.index)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Users")
    if len(logs) > 0:
        user_dist = logs['user'].value_counts().head(10)
        fig = px.bar(x=user_dist.index, y=user_dist.values)
        st.plotly_chart(fig, use_container_width=True)

# Recent Activity Table
st.subheader("Recent Activity")
if len(logs) > 0:
    display_logs = logs[['timestamp', 'user', 'action', 'resource', 'status', 'ip_address']].head(50)
    st.dataframe(display_logs, use_container_width=True)
else:
    st.info("No audit logs found for the selected filters")

# Export
if st.button("Export Audit Logs"):
    csv = logs.to_csv(index=False)
    st.download_button("Download CSV", csv, "audit_logs.csv", "text/csv")
