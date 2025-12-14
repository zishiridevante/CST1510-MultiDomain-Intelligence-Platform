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
st.set_page_config(page_title="IT Tickets", layout="wide")

st.title("💼 IT Support Tickets")
st.write("View and analyze IT helpdesk tickets stored in the system.")

conn = get_conn()

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
df = pd.read_sql_query("SELECT * FROM it_tickets", conn)

if df.empty:
    st.info("No IT ticket data found in the database.")
else:

    # -----------------------------------------
    # FILTERS
    # -----------------------------------------
    st.subheader("🔍 Filters")
    col1, col2 = st.columns(2)

    priority_filter = col1.selectbox("Filter by Priority", ["All"] + sorted(df["priority"].unique()))
    status_filter = col2.selectbox("Filter by Status", ["All"] + sorted(df["status"].unique()))

    filtered_df = df.copy()
    if priority_filter != "All":
        filtered_df = filtered_df[filtered_df["priority"] == priority_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]

    # -----------------------------------------
    # DISPLAY TABLE
    # -----------------------------------------
    st.subheader("📄 IT Ticket Records")
    st.dataframe(filtered_df, use_container_width=True)

    # -----------------------------------------
    # CHART — Tickets by Status
    # -----------------------------------------
    st.subheader("📈 Tickets by Status")

    status_counts = df["status"].value_counts()
    st.bar_chart(status_counts)

    # -----------------------------------------
    # CHART — Ticket Priority Levels
    # -----------------------------------------
    st.subheader("📊 Tickets by Priority")

    priority_counts = df["priority"].value_counts()
    st.bar_chart(priority_counts)
