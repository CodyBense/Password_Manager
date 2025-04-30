'''
    TODO:
        * follow sqlalchemy documentation to do insert statement
'''
import streamlit as st
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

def add_login(website_ti, username_ti, password_ti):
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
        new_login = Login(website=website_ti, email=username_ti, password=password_ti)
        session.add(new_login)
        session.commit()
    except Exception as e:
        print(f'failed adding data: {e}')

def main():
    st.title("Add login")
    st.write("Enter the login info you want ot add!")
    website_ti = st.text_input("Website")
    username_ti = st.text_input("Username")
    password_ti = st.text_input("Password")
    if st.button("Add Login...", on_click=add_login, args=(website_ti,username_ti,password_ti)):
        st.write("Adding login!")

if __name__ == "__main__":
    main()
