import pandas as pd
import statsmodels.api as sm
import numpy as np


station_data = pd.read_csv("../data/clean/subway_crime_panel.csv")

unique_stations = station_data.stop_name.unique().tolist()

# # regress incidents on number of exits for 1st ave station only
# first_ave = station_data.loc[station_data.stop_name==unique_stations[0]]
# X = np.log(first_ave['exits'] +1) 
# y = np.log(first_ave['incidents'] +1)
# model = sm.OLS(y, sm.add_constant(X)).fit()
# print("first ave station only log exits + log incidents:")
# print(model.summary()) 

# # regress incidents on number of exits for canal st station only
# index = unique_stations.index('Canal St')
# canal_st = station_data.loc[station_data.stop_name==unique_stations[index]]
# X = np.log(canal_st['exits'] +1) 
# y = np.log(canal_st['incidents'] +1)
# model = sm.OLS(y, sm.add_constant(X)).fit()
# print("canal st station only log exits + log incidents:")
# print(model.summary()) 

# regress incidents on number of exits for canal st station only
index = unique_stations.index('Mets - Willets Point')
mwp = station_data.loc[station_data.stop_name==unique_stations[index]]
X = np.log(mwp['exits'] +1) 
y = np.log(mwp['incidents'] +1)
model = sm.OLS(y, sm.add_constant(X)).fit()
print("Mets - Willets Point station only log exits + log incidents:")
print(model.summary())


# regress incidents on number of exits
X = np.log(station_data['exits']+1)
y = np.log(station_data['incidents']+1)
model = sm.OLS(y, sm.add_constant(X)).fit()
print("overall log exits + log incidents:")
print(model.summary()) 

# regress incidents on number of entries
X = np.log(station_data['entries']+1)
y = np.log(station_data['incidents']+1)
model = sm.OLS(y, sm.add_constant(X)).fit()
print("overall log entries + log incidents:")
print(model.summary()) 

