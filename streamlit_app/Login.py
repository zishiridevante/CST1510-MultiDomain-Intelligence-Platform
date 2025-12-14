import streamlit as st
from db_utils import verify_user

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

st.title("🔐 Login Page")
st.write("Enter your credentials to access the Intelligence Platform.")

# -----------------------------
# USER INPUT
# -----------------------------
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# -----------------------------
# LOGIN LOGIC
# -----------------------------
if st.button("Login", use_container_width=True):
    success, result = verify_user(username, password)

    if success:
        # Store session variables
        st.session_state["authenticated"] = True
        st.session_state["user"] = dict(result)

        st.success("Login successful! Redirecting...")

        # Redirect to dashboard Home page
        st.switch_page("pages/Home.py")

    else:
        st.error(result)
