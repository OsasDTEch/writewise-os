# main.py
import streamlit as st

st.title("Appwrite AI Assistant")
user_input = st.text_input("Ask about Appwrite:")

if user_input:
    # For now, just echo back
    st.write(f"You asked: {user_input}")