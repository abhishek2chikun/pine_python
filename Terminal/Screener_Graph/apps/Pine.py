from textwrap import indent
import pandas as pd
import streamlit as st
import glob
import base64
import os
import datetime
import time
import json
import convert_pine_to_python

def app():

    path ='/Users/abhishekpanigrahi/python_venv/Dev/spain/pine_python'
    
    def save_uploadedfile(uploadedfile):
        with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
            f.write(uploadedfile.getbuffer())
        return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

    position = pd.read_csv(f'{path}/IB/position.csv',index_col=[0])

    account_details = pd.read_csv(f'{path}/IB/acc_summary.csv',index_col=[0])
    account_details = account_details[['Tag','Value']]
    
    pine = st.file_uploader("Upload Pine Script")
    if pine is not None:
        save_uploadedfile(pine)
        col1,col2= st.columns([1,1])
        with col1:
            st.subheader("Pine Script")
            with open(f'./tempDir/{pine.name}','r') as file:
                Code =  file.read()
            
            # st.code(Code, language='python')
            st.code(Code,language ='text')
        with col2:
            st.subheader("Python Script")
            convert_pine_to_python.Convert(f'./tempDir/{pine.name}')
            with open('./tempDir/python_script.py','r') as file:
                Code =  file.read()
            
            st.code(Code, language='python')
            