import streamlit as st
from db_utils import register_user

st.title("🆕 Register Page")

username = st.text_input("Choose a username")
password = st.text_input("Choose a password", type="password")

if st.button("Register"):
    ok, message = register_user(username, password)

    if ok:
        st.success(message)
    else:
        st.error(message)
