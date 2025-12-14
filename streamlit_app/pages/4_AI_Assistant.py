import streamlit as st
import sqlite3
from pathlib import Path
from openai import OpenAI

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(page_title="AI Assistant", layout="wide")

# ----------------------------------
# LOGOUT BUTTON
# ----------------------------------
st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.clear())

# ----------------------------------
# AUTH CHECK
# ----------------------------------
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("You must log in first.")
    st.stop()

# ----------------------------------
# OPENAI CLIENT (SECURE)
# ----------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ----------------------------------
# DATABASE CONNECTION
# ----------------------------------
DB_PATH = Path(__file__).resolve().parents[2] / "DATA" / "intelligence_platform.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

# ----------------------------------
# UI
# ----------------------------------
st.title("🤖 AI Intelligence Assistant")
st.write(
    "Ask questions about cyber incidents, IT tickets, datasets, "
    "or request analytical insights from the platform data."
)

question = st.text_area("Ask a question:", height=120)

# ----------------------------------
# AI QUERY
# ----------------------------------
if st.button("Ask AI", use_container_width=True):

    if question.strip() == "":
        st.error("Please enter a question.")
        st.stop()

    conn = get_conn()

    cyber_data = conn.execute("SELECT * FROM cyber_incidents").fetchall()
    it_data = conn.execute("SELECT * FROM it_tickets").fetchall()
    dataset_meta = conn.execute("SELECT * FROM datasets_metadata").fetchall()

    cyber_text = "\n".join(str(row) for row in cyber_data)
    it_text = "\n".join(str(row) for row in it_data)
    dataset_text = "\n".join(str(row) for row in dataset_meta)

    system_message = f"""
You are an AI Assistant for a Multi-Domain Intelligence Platform.

You have access to the following datasets:

[CYBER INCIDENTS]
{cyber_text if cyber_text else "No cyber incident records available."}

[IT TICKETS]
{it_text if it_text else "No IT ticket records available."}

[DATASET METADATA]
{dataset_text if dataset_text else "No dataset metadata records available."}

Your task:
- Analyze the available data
- Answer the user's question clearly and concisely
- If data is missing, explain that clearly
- Provide cybersecurity-relevant insights where possible
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question},
            ]
        )

        answer = response.choices[0].message.content

        st.success("AI Response:")
        st.write(answer)

    except Exception as e:
        st.error(f"AI Error: {e}")
