import csv
import math
from collections import defaultdict, Counter
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path

f = open('crime_by_borough.csv', 'r', encoding="utf8")
f2 = open('subway_by_borough.csv', 'r', encoding="utf8")

def parse_boroughs(x):
    if 'bk' in x.lower():
       return 'Brooklyn'
    elif 'bx' in x.lower():
       return 'Bronx'
    elif 'm' in x.lower():
       return 'Manhattan'
    elif 'q' in x.lower():
       return 'Queens'
    elif 'si' in x.lower():
       return 'Staten Island'
    else:
       return None

df = pd.read_csv(f)
df['date'] = pd.to_datetime(df['OCCUR_DATE'])
df['borough'] = df['BORO'].apply(parse_boroughs)
df['num_shootings'] = df['0']
df.drop(['OCCUR_DATE', 'BORO', '0'], axis=1, inplace=True)
df.sort_values(by='date')

df = df.groupby('date')[['borough', 'num_shootings']].apply(
    lambda x: x.set_index('borough').to_dict(orient='index')).to_dict()

df2 = pd.read_csv(f2)
df2['date'] = pd.to_datetime(df2['date'])
df2['borough'] = df2['borough'].apply(parse_boroughs)
df2.sort_values(by='date')

cumulative = df2.copy()
cumulative['num_shootings'] = 0

for row in cumulative.iterrows():
    date = row[1]['date']
    borough = row[1]['borough']
    
    if date in df.keys():
        boroughs = df.get(date)
        if borough in boroughs.keys():
            entry = boroughs.get(borough)
            cumulative.loc[row[1]['Unnamed: 0'], 'num_shootings'] = entry.get('num_shootings')
                
cumulative.drop(['Unnamed: 0'], axis=1, inplace=True)
cumulative.to_csv('merged.csv')