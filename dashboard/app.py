import streamlit as st
import pandas as pd
from kafka import KafkaConsumer
import json
import os

# =============================
# Page config
# =============================
st.set_page_config(
    page_title="Smart Grid Monitoring",
    layout="wide"
)

st.title("⚡ Smart Grid Anomaly Detection Dashboard")
st.caption("Real-time Monitoring • Dynamic Threshold • Health Score")

# =============================
# Kafka Consumer
# =============================
consumer = KafkaConsumer(
    "alerts",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest"
)

alerts = []
placeholder = st.empty()
LOG_PATH = "logs/anomalies_log.csv"

st.markdown(
    """
    <style>
    .status-normal { color: #1f7a1f; font-weight: bold; }
    .status-warning { color: #d9822b; font-weight: bold; }
    .status-fault { color: #b30000; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

st.info("🟢 System running — waiting for alerts from villages...")

# =============================
# Stream processing
# =============================
for message in consumer:

    alert = message.value
    alerts.append(alert)
    df = pd.DataFrame(alerts)

    # Log anomalies
    if alert["anomaly"]:
        os.makedirs("logs", exist_ok=True)
        pd.DataFrame([alert]).to_csv(
            LOG_PATH,
            mode="a",
            header=not os.path.exists(LOG_PATH),
            index=False
        )

    with placeholder.container():

        # =============================
        # Health Status Overview
        # =============================
        st.subheader("🩺 Network Health Overview")

        villages = sorted(df["village"].unique())
        cols = st.columns(len(villages))

        for i, v in enumerate(villages):
            last = df[df["village"] == v].iloc[-1]
            score = int(last["health_score"])

            if score >= 80:
                status = "Normal"
                css = "status-normal"
            elif score >= 60:
                status = "Warning"
                css = "status-warning"
            else:
                status = "Fault"
                css = "status-fault"

            cols[i].markdown(
                f"""
                <div class="{css}">
                <h4>{v}</h4>
                <p>{status}</p>
                <p>{score}/100</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # =============================
        # Live Alerts Table
        # =============================
        st.markdown("---")
        st.subheader("📋 Live Alerts Stream")
        st.dataframe(df, use_container_width=True)

        # =============================
        # Measurements
        # =============================
        st.markdown("---")
        st.subheader("📈 Electrical Measurements")

        for v in villages:
            st.markdown(f"### 🔌 {v}")
            v_df = df[df["village"] == v]
            st.line_chart(v_df[["voltage", "current"]])
