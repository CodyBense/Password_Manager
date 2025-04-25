import streamlit as st
import pandas as pd
import numpy as np
import MySQLdb

def setup_page():
    st.title('Password Manager')

def fetch_data():
    try:
        mysql_cn = MySQLdb.connect(host='192.168.1.129',
                                   port=3306,
                                   user="root",
                                   passwd="ZSe45rdx##",
                                   db="Logins"
                                   )
        query = "SELECT * FROM login_info;"
        df = pd.read_sql(query, mysql_cn)
        mysql_cn.close()
        print(df.head)
    except Exception as e:
        print(f'failed fetching data: {e}')

def main():
    setup_page()
    fetch_data()

if __name__ == "__main__":
    main()
