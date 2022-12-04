import csv
import math
from collections import defaultdict, Counter
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path

# f = open('NYPD_Calls_for_Service__Historic_.csv', 'r', encoding="utf8")

# chunksize = 5000
# for chunk in pd.read_csv(f, chunksize = chunksize):
#     chunk['INCIDENT_DATE'] = pd.to_datetime(chunk['INCIDENT_DATE'])
#     chunk = chunk[(chunk['INCIDENT_DATE'] < '01/01/2020') & (chunk['INCIDENT_DATE'] > '12/31/2018')]
    

    if (os.path.isfile('processed_crime_data_2019.csv')):
        chunk.to_csv('processed_crime_data_2019.csv', encoding='utf-8', mode='a', index=False, header=False)
    else:
        chunk.to_csv('processed_crime_data_2019.csv', encoding='utf-8', index=False)


# f = open('NYPD_Shooting_Incident_Data__Historic_.csv', 'r', encoding="utf8")

# chunksize = 5000
# for chunk in pd.read_csv(f, chunksize = chunksize):
#     chunk['OCCUR_DATE'] = pd.to_datetime(chunk['OCCUR_DATE'])
#     chunk = chunk[(chunk['OCCUR_DATE'] < '01/01/2020') & (chunk['OCCUR_DATE'] > '12/31/2018')]
    
#     if(os.path.isfile('processed_shooting_data_2019.csv')):
#         chunk.to_csv('processed_shooting_data_2019.csv', encoding='utf-8', mode='a', index=False, header=False)
#     else:
#         chunk.to_csv('processed_shooting_data_2019.csv', encoding='utf-8', index=False)

f = open('merged.csv', 'r', encoding="utf8")
df = pd.read_csv(f)
df.sort_values(by=['borough', 'date'], inplace=True)
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.to_csv('merged_sorted.csv',  encoding='utf-8', index=True)
        