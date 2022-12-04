"""
build_maps.py
"""
import difflib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as cx
mta_df = pd.read_csv("/Users/arjunshanmugam/Documents/GitHub/econ1660-final/data/raw/body.csv")
print(mta_df['structure'].value_counts())
top_5_stations = mta_df.groupby('stop_name')['entries'].sum().sort_values(ascending=False).iloc[0:5].index
mta_df = mta_df.loc[mta_df['stop_name'].isin(top_5_stations), :]
mta_df.loc[:, 'date'] = pd.to_datetime(mta_df['date'])
fig, ax = plt.subplots()
mta_df.loc[:, 'week'] = mta_df['date'].dt.isocalendar().week
mta_df.groupby(['stop_name', 'week'])['entries'].sum().reset_index().set_index('week').groupby('stop_name')['entries'].plot(legend=True, ax=ax)
ax.set_ylabel("turnstile entries")
plt.savefig("/Users/arjunshanmugam/Documents/GitHub/econ1660-final/output/entries_over_weeks.png", bbox_inches='tight')



mta_df = pd.read_csv("/Users/arjunshanmugam/Documents/GitHub/econ1660-final/data/raw/body.csv")
highest_var_stations = mta_df.groupby('stop_name')['entries'].agg(lambda x: x.std() / x.mean()).sort_values(ascending=False).iloc[0:10]
station_coords = (pd.read_csv("/Users/arjunshanmugam/Documents/GitHub/econ1660-final/data/raw/body.csv")
                    .groupby('stop_name')
                    .first()[['gtfs_longitude', 'gtfs_latitude']])
station_coords = gpd.GeoDataFrame(station_coords,
                                  geometry=gpd.points_from_xy(station_coords['gtfs_longitude'], station_coords['gtfs_latitude'])).set_crs("EPSG:4326")
gdf = gpd.GeoDataFrame(pd.concat([highest_var_stations, station_coords], axis=1).dropna()).reset_index()
fig, ax = plt.subplots()
print(highest_var_stations)
gdf.plot(ax=ax, markersize=(highest_var_stations-0.77)*100)
ax.set_axis_off()
gdf.apply(lambda x: ax.annotate(text=x['stop_name'], xy=x.geometry.centroid.coords[0], ha='left', fontsize='xx-small'), axis=1)
ax.set_title(f"NYC Subway Stations with Highest\nCoefficient of Variation in Entries")
cx.add_basemap(ax=ax, crs=gdf.crs, source=cx.providers.CartoDB.Voyager)
plt.savefig(f"/Users/arjunshanmugam/Documents/GitHub/econ1660-final/output/maps/map_variance.png", bbox_inches='tight', dpi=1000)
plt.close(fig)

"""
turnstile_df = turnstile_df.loc[turnstile_df['STATION'].isin(top_30_stations), :].groupby(by=['STATION', 'TIME'])['ENTRIES'].mean().reset_index()
turnstile_df = turnstile_df.set_index('TIME')

station_gdf = gpd.read_file(
    "/Users/arjunshanmugam/Documents/GitHub/econ1660-final/data/raw/Subway Stations/geo_export_375e3849-eb99-4e61-bd38-13e0e8290c27.shp")
station_gdf = station_gdf.replace({"Herald Sq - 34th St": "34 ST-HERALD SQ"})
station_gdf = station_gdf.groupby(by='name').first().reset_index()
station_gdf.loc[:, 'name'] = station_gdf['name'].str.lower()
turnstile_df.loc[:, 'STATION'] = (turnstile_df['STATION']
                                  .str.lower()
                                  .apply(lambda x: difflib.get_close_matches(x, station_gdf['name'].str.lower())[0]))
gdf = station_gdf.merge(turnstile_df,
                        left_on='name',
                        right_on='STATION',
                        validate='1:m',
                        how='inner')
gdf = gdf.set_crs("EPSG:4326")
for time in ["00:00:00", "04:00:00", "08:00:00", "12:00:00", "16:00:00"]:
    turnstile_df_subset = gpd.GeoDataFrame(gdf.loc[gdf['TIME'] == time, :])
    fig, ax = plt.subplots()
    turnstile_df_subset.plot(ax=ax, markersize=np.log(turnstile_df_subset['ENTRIES']))
    ax.set_axis_off()
    turnstile_df_subset.apply(lambda x: ax.annotate(text=x['STATION'], xy=x.geometry.centroid.coords[0], ha='center', fontsize='xx-small'), axis=1)
    ax.set_title(f"Entries at NYC's Busiest Subway Stations \n During the Four Hour Period Ending at {time}")
    cx.add_basemap(ax=ax, crs=turnstile_df_subset.crs, source=cx.providers.CartoDB.Voyager)
    figname = "map_" + time.replace(":", "-")
    plt.savefig(f"/Users/arjunshanmugam/Documents/GitHub/econ1660-final/output/maps/map_{figname}.png", bbox_inches='tight', dpi=1000)
    plt.close(fig)

"""