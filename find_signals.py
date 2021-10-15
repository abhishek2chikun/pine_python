import python_script
import yahoo_data_download
import pandas as pd
import glob
import os
path = '/Users/abhishekpanigrahi/python_venv/Dev/spain/pine_python'
files = glob.glob(f'{path}/Yahoo_Data/*')

#Symbols = yahoo_data_download.Find_symbols(path)
for file in files:
	Data = pd.read_pickle(file)
	try:
		python_script.Find_signals(Data,os.path.basename(file).split('.pkl')[0])
	except:
		continue