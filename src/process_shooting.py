import csv
import math
from collections import defaultdict, Counter
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path

f = open('processed_shooting_data_2019.csv', 'r', encoding="utf8")

def parse_boroughs(x):
    if 'brooklyn' in x.lower():
       return 'Bk'
    elif 'bronx' in x.lower():
       return 'Bx'
    elif 'manhattan' in x.lower():
       return 'M'
    elif 'queens' in x.lower():
       return 'Q'
    elif 'staten' in x.lower():
       return 'SI'
    else:
       return None

df = pd.read_csv(f)
df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE'])
df['BORO'] = df['BORO'].apply(parse_boroughs)
df.sort_values(by='OCCUR_DATE')

count = df.groupby(['OCCUR_DATE', 'BORO'])
count.size().reset_index().to_csv('crime_by_borough.csv')