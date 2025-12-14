import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# ---------------------------
# AUTHENTICATION CHECK
# ---------------------------
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("You must log in first.")
    st.stop()


# -----------------------------------------
# FIXED DB PATH
# -----------------------------------------
DB_PATH = Path(__file__).resolve().parents[2] / "DATA" / "intelligence_platform.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

# -----------------------------------------
# PAGE SETTINGS
# -----------------------------------------
st.set_page_config(page_title="Cyber Incidents", layout="wide")

st.title("🛡️ Cyber Incidents Overview")
st.write("Explore all recorded cybersecurity incidents from the platform database.")

conn = get_conn()

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)

if df.empty:
    st.info("No cyber incident data found in the database.")
else:

    # -----------------------------------------
    # FILTERS
    # -----------------------------------------
    st.subheader("🔍 Filters")
    col1, col2 = st.columns(2)

    severity_filter = col1.selectbox("Filter by Severity", ["All"] + sorted(df["severity"].unique()))
    status_filter = col2.selectbox("Filter by Status", ["All"] + sorted(df["status"].unique()))

    filtered_df = df.copy()
    if severity_filter != "All":
        filtered_df = filtered_df[filtered_df["severity"] == severity_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]

    # -----------------------------------------
    # DISPLAY TABLE
    # -----------------------------------------
    st.subheader("📄 Cyber Incident Records")
    st.dataframe(filtered_df, use_container_width=True)

    # -----------------------------------------
    # CHART — Incidents by Severity
    # -----------------------------------------
    st.subheader("📊 Incidents by Severity")

    severity_counts = df["severity"].value_counts()
    st.bar_chart(severity_counts)

    # -----------------------------------------
    # CHART — Incidents by Status
    # -----------------------------------------
    st.subheader("📈 Incidents by Status")

    status_counts = df["status"].value_counts()
    st.bar_chart(status_counts)
