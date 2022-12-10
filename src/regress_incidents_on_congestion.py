import pandas as pd
import numpy as np

import statsmodels.api as sm
INPUT_DATA_CONGESTION = "../data/clean/congestion.csv"
INPUT_DATA_RIDERSHIP = "../data/clean/subway_crime_panel.csv"

congestion_df = pd.read_csv(INPUT_DATA_CONGESTION)
congestion_df = congestion_df.drop_duplicates(subset=['stop_name', 'date'])
ridership_df = pd.read_csv(INPUT_DATA_RIDERSHIP)
ridership_df = ridership_df.rename(columns={'Date': 'date'})
print(ridership_df.columns)

df = congestion_df.merge(ridership_df, on=['stop_name', 'date'], validate='1:1')

X = df['congestion']
y = np.log(df['incidents'] + 1)

model = sm.OLS(y, X).fit()
print(model.summary())