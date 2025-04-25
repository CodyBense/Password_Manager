import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def setup_page():
    st.title('Password Manager')
    st.checkbox('Show Passwords')

def fetch_data():
    try:
        load_dotenv()
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        db = os.getenv("DB_NAME")

        engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}:{port}/{db}")

        query = "SELECT * FROM login_info;"
        df = pd.read_sql(query, engine)
        st.write(df)
    except Exception as e:
        print(f'failed fetching data: {e}')

def main():
    setup_page()
    fetch_data()

if __name__ == "__main__":
    main()
