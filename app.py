"""
    TODO:
        * Figure out how I want to handle masking passwords till needed
        * Make a second page for adding logins
"""
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


def setup_page():
    """ Sets up the streamlit page. """
    the_vault = st.Page("pages/the_vault.py", title="The Vault")
    add_login_page = st.Page("pages/add_login.py", title="Add Login")
    pg = st.navigation([the_vault, add_login_page])
    pg.run()

def main():
    setup_page()


if __name__ == "__main__":
    main()
