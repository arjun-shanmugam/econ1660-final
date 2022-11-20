import csv
import math
from collections import defaultdict, Counter
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path

# f = open('NYPD_Calls_for_Service__Year_to_Date_.csv', 'r', encoding="utf8")

# chunksize = 5000
# for chunk in pd.read_csv(f, chunksize = chunksize):
#     chunk['INCIDENT_DATE'] = pd.to_datetime(chunk['INCIDENT_DATE'])
#     chunk = chunk[(chunk['INCIDENT_DATE'] < '10/01/2022') & (chunk['INCIDENT_DATE'] > '09/22/2022')]
    
#     if(os.path.isfile('processed_crime_data.csv')):
#         chunk.to_csv('processed_crime_data.csv', encoding='utf-8', mode='a', index=False, header=False)
#     else:
#         chunk.to_csv('processed_crime_data.csv', encoding='utf-8', index=False)

f = open('processed_crime_data.csv', 'r', encoding="utf8")
df = pd.read_csv(f)