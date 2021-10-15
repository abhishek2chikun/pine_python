import pandas as pd
import re
import json
from urllib.request import urlopen
from datetime import datetime
import os
import glob



url = 'https://www.otcmarkets.com/research/stock-screener/api?pageSize=17500'
path = '/Users/abhishekpanigrahi/python_venv/Dev/spain/pine_python'

response = urlopen(url)
Json = json.loads(response.read())

patter = re.compile('{"count":[0-9]+,"pages":[0-9]+,')
x=patter.split(Json)[1]

s = json.loads("{"+x)

df = pd.DataFrame.from_dict(s['stocks'])

df.reportDate[0]

datetime_object = datetime.strptime(df.reportDate[0], '%b %d, %Y %X %p')

files = glob.glob(path+'/OTC_data/*')
files_list = []
for i in files:
    files_list.append(os.path.basename(i).split('.csv')[0])
if str(datetime_object) not in files_list:
    print("New File!!, Saving..........")
    Date = str(datetime_object).replace(':',"_")
    df.to_csv(f'{path}/OTC_data/{Date}.csv',index =False)
# =============================================================================
#     graph = pd.read_csv(f'{path}/Data/Graph/graph.csv')
#     if str(datetime_object) not in list(graph.columns):
#         graph[datetime_object] = df.price
#         graph.to_csv(f'{path}/Data/Graph/graph.csv',index=False)
#         print("Done")
# =============================================================================

