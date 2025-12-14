import streamlit as st
from db_utils import verify_user, register_user

# Initialize login state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

st.set_page_config(page_title="Login", layout="centered")

st.title("🔐 Intelligence Platform Login")

# If already logged in, redirect to Home
if st.session_state.get("authenticated"):
    st.switch_page("pages/Home.py")

# -------------------------
# Select Mode (Login / Register)
# -------------------------
mode = st.radio("Select an option:", ["Login", "Register"])


# -------------------------
# LOGIN MODE
# -------------------------
if mode == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, result = verify_user(username, password)

        if success:
            user = dict(result)

            st.session_state["authenticated"] = True
            st.session_state["username"] = user["username"]
            st.session_state["role"] = user["role"]  # ← STORE ROLE FOR RBAC

            st.success("Login successful! Redirecting...")
            st.switch_page("pages/Home.py")

        else:
            st.error(result)


# -------------------------
# REGISTER MODE
# -------------------------
else:
    st.subheader("Create a New Account")

    new_user = st.text_input("Choose a username")
    new_pass = st.text_input("Choose a password", type="password")

    # Use readable role names (match RBAC)
    role = st.selectbox(
        "Select Role",
        ["admin", "cyber analyst", "data analyst"]
    )

    if st.button("Register"):
        success, msg = register_user(new_user, new_pass, role)

        if success:
            st.success("Account created! Please return to Login.")
        else:
            st.error(msg)
