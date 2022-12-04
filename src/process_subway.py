import csv
import math
from collections import defaultdict, Counter
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path

f = open('body.csv', 'r', encoding="utf8")

df = pd.read_csv(f, low_memory=False)
df['date'] = pd.to_datetime(df['date'])
df.sort_values(by='date')

count = df.groupby(['date', 'borough'])
count['entries'].sum().reset_index().to_csv('subway_by_borough.csv')