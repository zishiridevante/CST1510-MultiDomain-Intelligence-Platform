import streamlit as st

def require_login():
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("You must log in first.")
        st.stop()

def require_role(*allowed_roles):
    """Ensure logged-in user has a required role."""
    require_login()

    user_role = st.session_state.get("role", None)

    if user_role not in allowed_roles:
        st.error(f"Access denied. This page requires one of: {', '.join(allowed_roles)}")
        st.stop()
