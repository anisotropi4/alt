#!/usr/bin/env python3

import os
from functools import partial
import numpy as np
from fiona.transform import transform_geom

import pandas as pd
import geopandas as gp
from shapely.ops import transform
from shapely.geometry import Point

from scipy.spatial import cKDTree

pd.set_option('display.max_columns', None)

# EPSG:4326 WG 84
# EPSG:32630
# EPSG:27700 OS GB36

URBANTYPES = {'Large Town',
         'Large Town in Conurbation',
         'Core City (outside London)',
         'Village or small community in Conurbation',
         'Other City',
         'Small Town in Conurbation',
         'Small Town',
         'Medium Town',
         'Medium Town in Conurbation',
         'Core City (London)',
         'Village or Small Community in Conurbation'}

def _set_precision(precision=6):
    def _precision(x, y, z=None):
        return tuple([round(i, precision) for i in [x, y, z] if i])
    return partial(transform, _precision)

def nearest_stations(c, stations):
    stree = cKDTree(stations['geometry'].apply(lambda v: (v.x, v.y)).to_list())
    return stree.query(c.centroid.apply(lambda v: (v.x, v.y)).to_list(), k=1)

print('Load Output Area Data')
TOWNDATA = pd.read_csv('oa-classification-csv.csv')

TOWNDATA['name'] = TOWNDATA['bua_name']
IDX1 = TOWNDATA['bua_name'] == 'None'
TOWNDATA.loc[IDX1, 'name'] = TOWNDATA.loc[IDX1, 'la_name']
TOWNDATA['Town'] = TOWNDATA['name']
for k in [' BUA in Conurbation', ' BUASD', ' BUA']:
    TOWNDATA['Town'] = TOWNDATA['Town'].str.replace(k, '')

TOWNS = TOWNDATA.groupby(['bua_code', 'name', 'region_name']).filter(lambda v: v['population'].sum() > 1)
del TOWNDATA

IDX2 = TOWNS['citytownclassification'].isin(URBANTYPES)
TOWNS['urban'] = 'N'
TOWNS.loc[IDX2, 'urban'] = 'Y'

print('Loaded Output Area Data')
print('Load Scotland')
CRS = 'EPSG:32630'

SC = gp.read_file('work/OutputArea2011_MHW.shp')
SC = SC.to_crs(CRS)
KEYS = ['code', 'Popcount', 'SHAPE_1_Ar', 'DataZone', 'geometry']
G1 = SC[KEYS].set_index('DataZone').join(TOWNS.set_index('lsoa_code', drop=False))
G1 = G1.rename(columns={'population': 'lsoa_population'})
G1 = G1.rename(columns={'code': 'OA11CD', 'SHAPE_1_Ar': 'Area', 'Popcount': 'population'})
G1 = G1.drop(columns='outputarea_code')
print('Loaded Scotland')

print('Load England and Wales')
EW = gp.read_file('work/Output_Areas__December_2011__Boundaries_EW_BGC.shp')
EW = EW.to_crs(CRS)
KEYS = ['OA11CD', 'Shape__Are', 'geometry']
G2 = EW[KEYS].set_index('OA11CD', drop=False).join(TOWNS.set_index('outputarea_code'))
G2 = G2.rename(columns={'code': 'OA11CD', 'Shape__Are': 'Area'})
G2['lsoa_population'] = G2['population']
print('Loaded England and Wales')

DENSITY = G1.append(G2).reset_index(drop=True)
DENSITY['density'] = DENSITY['population'] / DENSITY['Area']

print('Nearest station')
def nearest_stations(c, stations):
    stree = cKDTree(stations['geometry'].apply(lambda v: (v.x, v.y)).to_list())
    return stree.query(c.centroid.apply(lambda v: (v.x, v.y)).to_list(), k=1)

_precision = _set_precision(5)
STATIONS = gp.read_file('download/output-stations.json')
for k in [' Rail Station', ' Railway', ' Station']:
    STATIONS['Station_Name'] = STATIONS['Station_Name'].str.replace(k, '')

STATIONS = STATIONS.to_crs(CRS)
IDXS = STATIONS['Status'] == 'active'
KEYS = ['Type', 'TIPLOC', 'CRS', 'Station_Name', 'geometry']

ACTIVE = STATIONS.loc[IDXS, KEYS].reset_index(drop=True).rename(columns={'Station_Name': 'Station', 'Type': 'type'})

POINTS = gp.GeoDataFrame(geometry=DENSITY.centroid, crs=CRS)

D, IDXD = nearest_stations(POINTS, ACTIVE)

DF1 = ACTIVE.drop(columns='geometry').loc[IDXD].reset_index(drop=True)
DF1['distance'] = D.round(0)
DENSITY = DENSITY.join(DF1)

POINTS['geometry'] = POINTS['geometry'].to_crs('EPSG:4326').apply(_precision)
POINTS['data'] = POINTS['geometry'].apply(lambda v: [v.x, v.y])
DENSITY['longitude'], DENSITY['latitude'] = zip(*POINTS.pop('data'))

DENSITY = DENSITY.to_crs('EPSG:4326')
DENSITY['geometry'] = DENSITY['geometry'].apply(_precision)

print("Write all")
IDX3 = DENSITY['urban'] == 'Y'
IDX4 = (DENSITY['density'] > 0.0015) & (DENSITY['bua_code'] != 'None') & ~IDX3
DENSITY.loc[IDX4, 'urban'] = 'S'

KEYS = ['OA11CD', 'region_name', 'Town', 'bua_code', 'lsoa_code', 'msoa_code', 'population', 'Area', 'density', 'constituency_name', 'urban', 'type', 'TIPLOC', 'CRS', 'Station', 'distance', 'geometry']

DENSITY[KEYS].to_file('shp/all_density.shp', crs='EPSG:4326')
DENSITY[KEYS].to_file('all_density.geojson', crs='EPSG:4326', driver='GeoJSON')

print("Write urban")
DENSITY.loc[IDX3, KEYS].to_file('shp/urban_density.shp', crs='EPSG:4326')
DENSITY.loc[IDX3, KEYS].to_file('urban_density.geojson', crs='EPSG:4326', driver='GeoJSON')

print("Write semiurban")
DENSITY.loc[IDX4, KEYS].to_file('shp/semiurban_density.shp', crs='EPSG:4326')
DENSITY.loc[IDX4, KEYS].to_file('semiurban_density.geojson', crs='EPSG:4326', driver='GeoJSON')
