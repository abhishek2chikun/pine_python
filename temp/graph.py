
import python_script
import pandas as pd
import glob
import os
import mplfinance as mpf

path = '/Users/abhishekpanigrahi/python_venv/Dev/spain/pine_python'
files = glob.glob(f'{path}/Yahoo_Data/*')

#Symbols = yahoo_data_download.Find_symbols(path)
for file in files[:1]:
	Data = pd.read_pickle(file)
print(Data.head)
a = [mpf.make_addplot(Data.Volume,type='bar',panel=1),
	 mpf.make_addplot(Data['Adj Close'],type='line',panel=1)]
mpf.plot(Data,addplot=a)
