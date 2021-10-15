from textwrap import indent
import pandas as pd
import streamlit as st
import glob
import base64
import os
import datetime
import time
import streamlit.components.v1 as components
st.set_page_config(layout="wide")
def app():

    #alert = pd.read_csv('./alert.csv')
    alert = pd.DataFrame()
    path ='/Users/abhishekpanigrahi/python_venv/Dev/spain/pine_python'



    files = glob.glob(path+'/OTC_data/*')
    files_list = []
    print(files)

    for i in files:
        files_list.append(datetime.datetime.strptime(os.path.basename(i).split('.csv')[0].replace('_',':'), '%Y-%m-%d %X'))
    #file = max(files_list)
    #st.title("Market Screener")

    st_file = st.sidebar.selectbox("Select Date",sorted(files_list,reverse=True))
    st_file = str(st_file).replace(':',"_")
    df = pd.read_csv(f'{path}/OTC_data/{st_file}.csv',index_col=None)


    cols = [ 'symbol', 'securityName','industry', 'volumeChange','price']
    st_col = st.sidebar.multiselect("Columns", df.columns.tolist(), default=cols)


    st_price = st.sidebar.slider("Price range", float(df.price.min()), float(df.price.max()), (0.,100.))

    st.dataframe(df[(df.price > st_price[0]) & (df.price < st_price[1])][st_col],width=1000,height=680)
    def get_table_download_link_csv(df):
        #csv = df.to_csv(index=False)
        csv = df.to_csv().encode()
        #b64 = base64.b64encode(csv.encode()).decode() 
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="captura.csv" target="_blank">Download csv file</a>'
        return href
    m_df = df[(df.price > st_price[0]) & (df.price < st_price[1])][st_col]
    st.markdown(get_table_download_link_csv(m_df), unsafe_allow_html=True)
    st.sidebar.header("Custom Alert")

    Symbol = st.sidebar.text_input('Symbol')
    Price = st.sidebar.number_input('Price, x')
    g_or_l = st.sidebar.selectbox('price > x or price < x ',['Greater then','Less then'])
    if st.sidebar.button("Set Alert"):
        st.sidebar.write(f"Alert Set for symbol:{Symbol}")
        print([Symbol,Price,g_or_l] )
        alert.loc[len(alert.index)] = [Symbol,Price,g_or_l] 
        alert.to_csv('alert.csv',index=False)
