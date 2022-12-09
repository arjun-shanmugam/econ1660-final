import pandas as pd
import statsmodels.api as sm
import numpy as np


station_data = pd.read_csv("../data/clean/subway_crime_panel.csv")
station_data.loc[:, 'month'] = pd.to_datetime(station_data['Date']).dt.month
station_data = station_data.set_index(['stop_name', 'month'])
stop_name_month_means = station_data.groupby(['stop_name', 'month'])[['entries', 'exits']].mean().rename(columns={'entries': 'mean_entries',
                                                                                                                  'exits': 'mean_exits'})
station_data = pd.concat([station_data, stop_name_month_means], axis=1)
station_data.loc[:, 'demeaned_entries'] = station_data['entries'] - station_data['mean_entries']
station_data.loc[:, 'demeaned_exits'] = station_data['exits'] - station_data['mean_exits']


# regress incidents on number of exits
X = station_data['demeaned_exits']
y = station_data['incidents']
model = sm.OLS(y, sm.add_constant(X)).fit()
print("overall log exits + log incidents:")
print(model.summary()) 

# regress incidents on number of entries
X = station_data['demeaned_entries']
y = station_data['incidents']
model = sm.OLS(y, sm.add_constant(X)).fit()
print("overall log entries + log incidents:")
print(model.summary()) 

