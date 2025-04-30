'''
    TODO:
        * Implement delete query
'''
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

def delete_login(website_ti):
    try:
        print(website_ti)
    except Exception as e:
        print(f'failed deleting data: {e}')

def main():
    st.title('Delete Login')
    st.write('Enter the website of the login you want to delete!')
    website_ti = st.text_input('Website')
    if st.button('Delete', on_click=delete_login, args=(website_ti)):
        st.write('Deleting login...')
    


if __name__ == '__main__':
    main()
