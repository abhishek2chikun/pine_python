import pandas as pd
import streamlit as st
import glob
import base64
import os
import datetime
import mpld3
import time
import streamlit.components.v1 as components
# st.set_page_config(layout="wide")
def app():
    import talib 
    import numpy as np
    import datetime
    import matplotlib.pyplot as plt

    import pandas as pd
    import mplfinance as mpf
    import glob
    import os

    path = '/Users/abhishekpanigrahi/python_venv/Dev/spain/pine_python/Yahoo_data'
    Symbols = glob.glob(f'{path}/*')
    symbol_list = []
    for symbol in Symbols:
        symbol_list.append(os.path.basename(symbol).split('.pkl')[0])
    a,b,c = st.columns([1,1,1])
    with b:
        Symbol = st.selectbox("Search Symbols", symbol_list)
        
        Type = st.selectbox("Type",['BUY','SELL'])
        Quantity= st.number_input('Quantity',0,10000,1,1,'%d')
        Order_type = st.selectbox('Order Type',['Market','Limit'])

        if Order_type == 'Limit':
            Limit_price = st.number_input("Enter Limit price")
            market = False
        else:
            market = True
            Limit_price = None
        Place_order =st.button("Place Order")
        if Symbol is not None and Type is not None and Quantity is not None and Order_type is not None and Place_order is not None:
            print(Symbol,Type,Quantity,Order_type,market,Limit_price)

