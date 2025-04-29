"""
    TODO:
        * fix insert query
"""
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

Base = declarative_base()

class Login(Base):
    __tablename__ = 'login_info'

    id = Column(Integer, primary_key=True)
    website = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))

def add_login(website_tb, username_tb, password_tb):
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
        Session = sessionmaker(bind=engine)
        session = Session()

        # Queries the database to add the login info.
        new_login = Login(website=website_tb, email=username_tb, password=password_tb)
        session.add(new_login)
        session.commit()
        query = f"INSERT INTO login_info (website, email, password) VALUES ('{website}', '{username}', '{password}'); "
    except Exception as e:
        print(f'failed adding data: {e}')

def main():
    st.title("Add login")
    website_tb = st.text_input("Website")
    username_tb = st.text_input("Username")
    password_tb = st.text_input("Password")
    if st.button("Add Login...", on_click=add_login, args=(website_tb,username_tb,password_tb)):
        st.write("Adding login!")

if __name__ == "__main__":
    main()
