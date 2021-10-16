from textwrap import indent
import pandas as pd
import streamlit as st
import glob
import base64
import os
import datetime
import time
import json


def app():

    path ='/Users/abhishekpanigrahi/python_venv/Dev/spain/pine_python'
    
    
    position = pd.read_csv(f'{path}/IB/position.csv',index_col=[0])

    account_details = pd.read_csv(f'{path}/IB/acc_summary.csv',index_col=[0])
    account_details = account_details[['Tag','Value']]
    
    col1,col2 = st.columns([1,0.5])
    with col1:
        st.header("Position")
        st.dataframe(position)
    with col2:
        st.header("Account Details")
        st.dataframe(account_details)
        