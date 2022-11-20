"""
build_maps.py
"""
import pandas as pd
import geopandas as gpd

turnstile_df = pd.read_csv("/Users/arjunshanmugam/Documents/GitHub/econ1660-final/data/raw/turnstile_counts.csv")
top_30_stations = (turnstile_df
                   .groupby(by='STATION')['ENTRIES']
                   .sum()
                   .sort_values(ascending=False)
                   .iloc[0:30].index)

