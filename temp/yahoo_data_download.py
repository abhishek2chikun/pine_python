#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 02:25:16 2021

@author: abhishek
"""
import pandas_datareader.data as web

from pandas_datareader.yahoo.headers import DEFAULT_HEADERS

import datetime
import requests_cache
import pandas as pd
import glob
import os
import time

path = '/Users/abhishekpanigrahi/python_venv/Dev/spain/pine_python'
def Find_symbols(path):
    files = glob.glob(path+'/OTC_data/*')
    files_list = []
    for i in files:
        files_list.append(datetime.datetime.strptime(os.path.basename(i).split('.csv')[0].replace('_',':'), '%Y-%m-%d %X'))

    file = max(files_list)
    file_name = str(file).replace(':',"_")
    df = pd.read_csv(f'{path}/OTC_data/{file_name}.csv',index_col=None)
    Symbols = list(df.symbol)
    return Symbols
Symbols = Find_symbols(path)
expire_after = datetime.timedelta(days=3)

session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)

session.headers = DEFAULT_HEADERS

start = datetime.datetime(2020, 1, 1)
 
end = datetime.datetime.now().date()
for symbol in Symbols[180:]:
    try:
        f = web.DataReader(symbol, 'yahoo', start, end, session=session)
    except Exception as e:
        print(e)
        continue
    f.to_pickle(f'{path}/Yahoo_data/{symbol}.pkl')
    time.sleep(2)
