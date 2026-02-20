"""
Source: Scraped Uber App Trip Records
Geography: USA, Sri Lanka and Pakistan
Time period: January - December 2016      
"""

from collections import defaultdict
import urllib.parse
import pandas as pd
import csv, json
import sys
import requests
import re

# Read script name and file name
filename = sys.argv[1]  
uber_data = pd.read_csv(filename)
df = pd.DataFrame(uber_data)

# Create index column and rename it as User_ID'
df.reset_index(inplace=True)
df.rename(columns={'index': 'Trip_ID'}, inplace=True)
df.Trip_ID = df.Trip_ID + 1

# Preprocess dataset
# print(df.shape)       # (1156, 8)
# print(df.describe())
df.drop(df.index[-1], inplace=True)
df = df.rename(columns=lambda x: x.replace('*', ''))
df.PURPOSE.fillna('Other', inplace=True)
df['PURPOSE'] = df.PURPOSE.str.replace('Charity ($)', 'Charity', regex=False)

# Address 'Kar?chi' and 'R?walpindi' problems
df['START'] = df.START.str.replace('Kar?chi', 'Karachi', regex=False)
df['STOP'] = df.STOP.str.replace('Kar?chi', 'Karachi', regex=False)
df['START'] = df.START.str.replace('R?walpindi', 'Rawalpindi', regex=False)
df['STOP'] = df.STOP.str.replace('R?walpindi', 'Rawalpindi', regex=False)
df['START'] = df.START.str.replace('Unknown Location', 'Unknown', regex=False)
df['STOP'] = df.STOP.str.replace('Unknown Location', 'Unknown', regex=False)

d = df.set_index('Trip_ID').to_dict(orient='index')
jsondata = json.dumps(d)

url = 'https://project551.firebaseio.com/index.json'
response = requests.put(url,jsondata)
# print(json.dumps(response.json(), indent=2, separators=(',\t',':')))
