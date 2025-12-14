import streamlit as st
import bcrypt
import sqlite3
from pathlib import Path

# -----------------------------------------
# DATABASE SETUP
# -----------------------------------------
DB_PATH = Path(__file__).resolve().parents[1] / "DATA" / "intelligence_platform.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

# -----------------------------------------
# PAGE SETTINGS
# -----------------------------------------
st.set_page_config(page_title="Register", page_icon="📝")

st.title("📝 Create a New Account")
st.write("Fill out the information below to register a new user.")

# -----------------------------------------
# INPUT FIELDS
# -----------------------------------------
username = st.text_input("Username")

password = st.text_input("Password", type="password")

role = st.selectbox(
    "Select user role:",
    ["user", "admin", "cyber_analyst", "data_analyst"]
)

register_button = st.button("Register", use_container_width=True)

# -----------------------------------------
# HANDLE REGISTRATION
# -----------------------------------------
if register_button:

    if username.strip() == "" or password.strip() == "":
        st.error("Username and password are required.")
    else:
        conn = get_conn()
        cursor = conn.cursor()

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        try:
            cursor.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (username, hashed_pw, role))

            conn.commit()
            st.success(f"User '{username}' created successfully as '{role}'!")
            st.info("Go back to the Login page to continue.")

        except sqlite3.IntegrityError:
            st.error("That username already exists. Try another.")
