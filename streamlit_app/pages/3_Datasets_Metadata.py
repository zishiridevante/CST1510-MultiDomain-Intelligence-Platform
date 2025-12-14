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
# FIXED DATABASE PATH FOR PAGES
# -----------------------------------------
DB_PATH = Path(__file__).resolve().parents[2] / "DATA" / "intelligence_platform.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

# -----------------------------------------
# PAGE SETTINGS
# -----------------------------------------
st.set_page_config(page_title="Datasets Overview", layout="wide")

st.title("📂 Dataset Metadata Overview")
st.write("Explore information about all datasets stored in the platform.")

conn = get_conn()

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)

if df.empty:
    st.info("No dataset metadata found in the database.")
    st.stop()

# -----------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------
st.sidebar.header("Filters")

uploader_filter = st.sidebar.multiselect(
    "Filter by Uploaded By:",
    options=sorted(df["uploaded_by"].unique()),
    default=sorted(df["uploaded_by"].unique())
)

df_filtered = df[df["uploaded_by"].isin(uploader_filter)]

# -----------------------------------------
# SUMMARY METRICS
# -----------------------------------------
st.subheader("📌 Summary Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Datasets", len(df))
col2.metric("Filtered Datasets", len(df_filtered))
col3.metric("Largest Dataset (Rows)", df["rows"].max())

# -----------------------------------------
# CHART — Dataset Sizes
# -----------------------------------------
st.subheader("📊 Dataset Sizes (Rows)")

chart_df = df_filtered.set_index("name")["rows"]
st.bar_chart(chart_df)

# -----------------------------------------
# TABLE — Full Metadata
# -----------------------------------------
st.subheader("📄 Dataset Metadata Table")
st.dataframe(df_filtered, use_container_width=True)
