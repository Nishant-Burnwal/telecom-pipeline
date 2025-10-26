# src/dashboard_app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db import get_data_from_mysql

# Streamlit page setup
st.set_page_config(page_title="Telecom Network Dashboard", layout="wide")

st.title("📊 Telecom Network Performance Dashboard")

# Fetch data
df = get_data_from_mysql()

if df.empty:
    st.error("❌ No data found. Check if your database and table are configured properly.")
else:
    st.success("✅ Data loaded successfully!")

    # --- Overview metrics ---
    st.subheader("📈 Overall Network KPIs")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Average Latency (ms)", f"{df['latency_ms'].mean():.2f}")
    col2.metric("Average Uptime (%)", f"{df['uptime_percent'].mean():.2f}")
    col3.metric("Avg Packet Loss (%)", f"{df['packet_loss_rate'].mean():.2f}")
    col4.metric("Total Bandwidth (MB)", f"{df['bandwidth_usage_mb'].sum():,.0f}")

    st.divider()

    # --- Region-wise performance ---
    st.subheader("🌍 Region-wise Network Performance")

    region_summary = df.groupby("region").agg({
        "latency_ms": "mean",
        "uptime_percent": "mean",
        "packet_loss_rate": "mean",
        "bandwidth_usage_mb": "sum"
    }).reset_index()

    # Plot 1 - Latency
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=region_summary, x="region", y="latency_ms", palette="viridis", ax=ax1)
    ax1.set_title("Average Latency by Region")
    ax1.set_xlabel("Region")
    ax1.set_ylabel("Latency (ms)")
    st.pyplot(fig1)

    # Plot 2 - Uptime
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=region_summary, x="region", y="uptime_percent", palette="mako", ax=ax2)
    ax2.set_title("Average Uptime by Region")
    ax2.set_xlabel("Region")
    ax2.set_ylabel("Uptime (%)")
    st.pyplot(fig2)

    st.divider()

    # --- Bandwidth usage over time ---
    st.subheader("📅 Bandwidth Usage Over Time")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    time_trend = df.groupby(df["timestamp"].dt.date)["bandwidth_usage_mb"].sum().reset_index()

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=time_trend, x="timestamp", y="bandwidth_usage_mb", marker="o", ax=ax3)
    ax3.set_title("Daily Bandwidth Usage Trend")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Bandwidth (MB)")
    st.pyplot(fig3)

    st.divider()

    # --- Top 10 customers by bandwidth ---
    st.subheader("🏆 Top 10 Customers by Bandwidth Usage")

    top_customers = df.groupby("customer_id")["bandwidth_usage_mb"].sum().sort_values(ascending=False).head(10)

    fig4, ax4 = plt.subplots(figsize=(8, 4))
    sns.barplot(x=top_customers.index, y=top_customers.values, palette="magma", ax=ax4)
    ax4.set_title("Top 10 Customers by Bandwidth")
    ax4.set_xlabel("Customer ID")
    ax4.set_ylabel("Total Bandwidth (MB)")
    st.pyplot(fig4)

    st.divider()

    # --- Raw data viewer ---
    st.subheader("📋 Raw Data Preview")
    st.dataframe(df.head(50))
