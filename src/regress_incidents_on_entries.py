import os

import pandas as pd
import statsmodels.api as sm
import numpy as np
import contextily as cx
import geopandas as gpd
# Add demeaned entries and exits as columns.
from matplotlib import pyplot as plt
import matplotlib
# matplotlib.rcParams['figure.dpi'] = 500
OUTPUT = "/Users/arjunshanmugam/Documents/GitHub/econ1660-final/output/maps"
station_data = pd.read_csv("../data/clean/subway_crime_panel.csv")
print(station_data.columns)
station_data.loc[:, 'month'] = pd.to_datetime(station_data['Date']).dt.month
station_data = station_data.set_index(['stop_name', 'month'])
stop_name_month_means = station_data.groupby(['stop_name', 'month'])[['entries', 'exits']].mean().rename(columns={'entries': 'mean_entries',
                                                                                                                  'exits': 'mean_exits'})
station_data = pd.concat([station_data, stop_name_month_means], axis=1)
station_data.loc[:, 'demeaned_entries'] = station_data['entries'] - station_data['mean_entries']
station_data.loc[:, 'demeaned_exits'] = station_data['exits'] - station_data['mean_exits']

# Regress incidents on number of entries, entire dataset.
X = station_data['demeaned_entries']
y = station_data['incidents']
model = sm.OLS(y, sm.add_constant(X)).fit()
print("overall log entries + log incidents:")
print(model.summary())

# Regress incidents on number of exits, entire dataset.
X = station_data['demeaned_exits']
y = station_data['incidents']
model = sm.OLS(y, sm.add_constant(X)).fit()
print("overall log exits + log incidents:")
print(model.summary())

# Regress incidents on entries and incidents on exits, separately by station.
station_data = station_data.reset_index()
stop_names = station_data['stop_name'].value_counts().index
independent_variables = ['entries', 'demeaned_entries', 'exits', 'demeaned_exits']
results_df = pd.DataFrame(index=stop_names, columns=independent_variables)
for stop_name in stop_names:
    y = np.log(station_data.loc[station_data['stop_name'] == stop_name, 'incidents'])
    for independent_variable in independent_variables:
        longitude = station_data.loc[station_data['stop_name'] == stop_name, 'gtfs_longitude'].iloc[0]
        latitude = station_data.loc[station_data['stop_name'] == stop_name, 'gtfs_latitude'].iloc[0]
        X = station_data.loc[station_data['stop_name'] == stop_name, independent_variable]
        model = sm.OLS(y, sm.add_constant(X)).fit()
        if "Beach" in stop_name:
            print(f"Results for {stop_name}")
            print(model.summary())
            print("\n\n\n\n")
        if model.pvalues[independent_variable] <= 0.05:
            results_df.loc[stop_name, independent_variable] = model.params[independent_variable]
        else:
            results_df.loc[stop_name, independent_variable] = 0
        results_df.loc[stop_name, 'longitude'] = longitude
        results_df.loc[stop_name, 'latitude'] = latitude
print(results_df)
# Keep track of which stations display the strongest relationships between crime and congestion.
strongest_relationships_dict = {}
for independent_variable in independent_variables:
    results_df.loc[:, independent_variable] = np.abs(results_df[independent_variable])
    strongest_relationship_stops = results_df.loc[:, [independent_variable, 'longitude', 'latitude']].sort_values(by=independent_variable,
                                                                                                                  ascending=False).iloc[:10]
    strongest_relationships_dict[independent_variable] = (gpd.GeoDataFrame(strongest_relationship_stops,
                                                                           geometry=gpd.points_from_xy(strongest_relationship_stops['longitude'],
                                                                                                       strongest_relationship_stops['latitude']))
                                                          .set_crs("EPSG:4326"))

fig, axes = plt.subplots(1, 2, figsize=(8, 6), sharex='all', sharey='all')
fig.suptitle("Stations Where the Relationship is Strongest Between Entries and Crime Incidents")
titles = ["Without Station-Month F.E.", "With Station-Month F.E."]
for ax, title, gdf in zip(axes, titles, [strongest_relationships_dict['entries'], strongest_relationships_dict['demeaned_entries']]):
    gdf.plot(ax=ax)
    ax.set_title(title)
    ax.set_axis_off()
    ax.set_ylim(40.5, None)
    ax.set_xlim(None, -73.75)
    gdf = gdf.reset_index()
    gdf.apply(lambda x: ax.annotate(text=x['index'], xy=x.geometry.centroid.coords[0], ha='left', fontsize='xx-small'), axis=1)
    cx.add_basemap(ax, crs="EPSG:4236")
plt.savefig(os.path.join(OUTPUT, "entries_strongest_relationships.png"), bbox_inches='tight')

fig, axes = plt.subplots(1, 2, figsize=(8, 6), sharex='all', sharey='all')
fig.suptitle("Stations Where the Relationship is Strongest Between Exits and Crime Incidents")
titles = ["Without Station-Month F.E.", "With Station-Month F.E."]
for ax, title, gdf in zip(axes, titles, [strongest_relationships_dict['exits'],
                                         strongest_relationships_dict['demeaned_exits']]):
    gdf.plot(ax=ax)
    ax.set_title(title)
    ax.set_axis_off()
    ax.set_ylim(40.5, None)
    ax.set_xlim(None, -73.75)
    gdf = gdf.reset_index()
    gdf.apply(lambda x: ax.annotate(text=x['index'], xy=x.geometry.centroid.coords[0], ha='left', fontsize='xx-small'), axis=1)
    cx.add_basemap(ax, crs="EPSG:4236")
plt.savefig(os.path.join(OUTPUT, "exits_strongest_relationships.png"), bbox_inches='tight')


