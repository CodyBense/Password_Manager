"""
    TODO:
        * fix insert query
"""
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def add_login(website, username, password):
    try:
        #Gets the info from the .env file.
        load_dotenv()
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        db = os.getenv("DB_NAME")

        # Connects to the database.
        engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}:{port}/{db}")

        # Queries the database to add the login info.
        query = f"INSERT INTO login_info (website, email, password) VALUES ('{website}', '{username}', '{password}'); "
    except Exception as e:
        print(f'failed adding data: {e}')

def main():
    st.title("Add login")
    website = st.text_input("Website")
    username = st.text_input("Username")
    password = st.text_input("Password")
    st.button("Add Login...", on_click=add_login, args=(website,username,password))

if __name__ == "__main__":
    main()
