import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


def fetch_data():
    """ Accesses the data from the sql database. """
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

        # Queries the database for all the login infor and prints it to the page.
        query = "SELECT * FROM login_info;"
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f'failed fetching data: {e}')
    return df


def main():
    st.title('The Vault')
    df = fetch_data()
    st.dataframe(df, use_container_width=True, hide_index=True, column_config={"id": None})


if __name__ == "__main__":
    main()
