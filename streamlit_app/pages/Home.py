import streamlit as st
import sqlite3
from pathlib import Path
import pandas as pd

# ---------------------------
# AUTHENTICATION CHECK
# ---------------------------
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("You must log in first.")
    st.stop()

# -----------------------------------------
# FIXED DATABASE PATH (for Streamlit pages/)
# -----------------------------------------
DB_PATH = Path(__file__).resolve().parents[2] / "DATA" / "intelligence_platform.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="Intelligence Platform Dashboard",
    layout="wide"
)

st.title("📊 Intelligence Platform Dashboard")
st.write("Welcome to your central intelligence dashboard. Use the sidebar to navigate between sections.")

# -----------------------------------------
# LOAD BASIC METRICS
# -----------------------------------------
conn = get_conn()
cyber_count = conn.execute("SELECT COUNT(*) FROM cyber_incidents").fetchone()[0]
tickets_count = conn.execute("SELECT COUNT(*) FROM it_tickets").fetchone()[0]
datasets_count = conn.execute("SELECT COUNT(*) FROM datasets_metadata").fetchone()[0]

# -----------------------------------------
# SHOW METRICS
# -----------------------------------------
st.subheader("📌 Quick Stats")

col1, col2, col3 = st.columns(3)

col1.metric("Cyber Incidents", cyber_count)
col2.metric("IT Tickets", tickets_count)
col3.metric("Datasets Uploaded", datasets_count)

# -----------------------------------------
# CHART 1 — Cyber Incidents by Severity
# -----------------------------------------
st.subheader("📊 Cyber Incidents by Severity")

df_cyber = pd.read_sql_query("SELECT severity FROM cyber_incidents", conn)

if not df_cyber.empty:
    severity_counts = df_cyber["severity"].value_counts()
    st.bar_chart(severity_counts)
else:
    st.info("No cyber incident data available.")

# -----------------------------------------
# CHART 2 — IT Tickets by Status
# -----------------------------------------
st.subheader("📈 IT Tickets by Status")

df_tickets = pd.read_sql_query("SELECT status FROM it_tickets", conn)

if not df_tickets.empty:
    status_counts = df_tickets["status"].value_counts()
    st.bar_chart(status_counts)
else:
    st.info("No IT ticket data available.")

# -----------------------------------------
# CHART 3 — Dataset Sizes
# -----------------------------------------
st.subheader("📂 Dataset Size Overview (Rows)")

df_datasets = pd.read_sql_query("SELECT name, rows FROM datasets_metadata", conn)

if not df_datasets.empty:
    st.line_chart(df_datasets.set_index("name"))
else:
    st.info("No dataset metadata available.")
