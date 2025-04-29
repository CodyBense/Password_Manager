import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.title("Add login")
    website = st.text_input("Website")
    username = st.text_input("Username")
    password = st.text_input("Password")
    st.button("Add Login...")

if __name__ == "__main__":
    main()
