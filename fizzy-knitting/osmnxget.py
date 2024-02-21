#!/usr/bin/env python

import json
import osmnx as ox
from osmnx.utils import log
from osmnx.downloader import _osm_network_download
from functools import partial
from itertools import groupby
import argparse as args

from shapely.geometry import shape, Point, LineString
from shapely.ops import transform
import geopandas as gp

ox.config(use_cache=True, log_console=True)

try:
    import pandas as pd
    pd.set_option('display.max_columns', None)
except ImportError:
    pass

PARSER = args.ArgumentParser(description='Download OSM rail data from OverpassAPI ')
PARSER.add_argument('--shpfiles', dest='shp', action='store_true',
                    default=False,
                    help='create ESRI ShapeFile data (default False)')

ARGS = PARSER.parse_args()
SHP = ARGS.shp

def _set_precision(precision=6):
    def _precision(x, y, z=None):
        return tuple([round(i, precision) for i in [x, y, z] if i])
    return partial(transform, _precision)

def get_node(e):
    node = {'geometry': Point(e['lon'], e['lat'])}
    node['osmid'] = e['id']
    if 'tags' in e:
        for t in ox.settings.useful_tags_node:
            if t in e['tags']:
                node['tags'] = True
                node[t] = e['tags'][t]                
    return node

def get_path(e):
    path = {}
    path['osmid'] = e['id']
    # remove any consecutive duplicate elements in the list of nodes
    g_list = groupby(e['nodes'])
    path['nodes'] = [g[0] for g in g_list]
    if 'tags' in e:
        for t in ox.settings.useful_tags_path:
            if t in e['tags']:
                path[t] = e['tags'][t]
    return path

def get_linestring(v):
    return LineString([NODES[i]['geometry'] for i in v])

with open('great-britain.json', 'r') as fin:
    POLYGON = shape(json.load(fin))

ox.settings.useful_tags_node = ['lon', 'timestamp', 'user', 'lat', 'ref', 'changeset', 'id', 'version', 'uid', 'ref:tiploc', 'name', 'electrified', 'frequency', 'voltage', 'railway']
ox.settings.useful_tags_path = ['bridge', 'tunnel', 'width', 'id', 'maxspeed', 'junction', 'name', 'version', 'uid', 'changeset', 'landuse', 'timestamp', 'user', 'ref', 'oneway', 'ref:tiploc', 'name', 'electrified', 'frequency', 'voltage', 'railway']

DATA = _osm_network_download(POLYGON, 'way["railway"]', '["railway"!~"highway|cycleway|footway|path|pedestrian|steps|corridor|elevator|escalator|proposed|construction|bridleway|abandoned|platform|raceway|service"]["railway"~"rail|subway|light_rail|tram|narrow_gauge"]')

log('Create node and path data')
NODES = {}
PATHS = {}
for osm_data in DATA:
    for e in osm_data['elements']:
        if e['type'] == 'node':
            key = e['id']
            NODES[key] = get_node(e)
        if e['type'] == 'way': #osm calls network paths 'ways'
            key = e['id']
            PATHS[key] = get_path(e)

log('Create GeoPandas dataframe')
GF1 = gp.GeoDataFrame.from_dict(PATHS, orient='index')
GF1['geometry'] = GF1['nodes'].apply(get_linestring)
GF1 = GF1.drop('nodes', axis=1)
GF1.crs = 'EPSG:4326'
GF1['type'] = 'way'
IDX1 = GF1.within(POLYGON) | GF1.intersects(POLYGON)
GF1['location'] = 'GB'
GF1.loc[~IDX1, 'location'] = 'IE'

if SHP:
    log('Output shapefiles')
    GF2 = gp.GeoDataFrame.from_dict(data=NODES, orient='index')
    GF2.crs = 'EPSG:4326'
    GF2 = GF2.loc[GF2['tags'].dropna().index].drop(columns='tags', axis=1)
    GF2['type'] = 'node'
    IDX2 = GF2.within(POLYGON) | GF2.intersects(POLYGON)
    GF2['location'] = 'GB'
    GF2.loc[~IDX2, 'location'] = 'IE'
    GF1.fillna('').to_file('shp/full_ways.shp', crs='epsg:4326')
    GF2.fillna('').to_file('shp/full_nodes.shp', crs='epsg:4326')

log('Trim dataframe')
GF1 = GF1[IDX1].drop('location', axis=1)

log('Create GeoJSON')
OUTPUT = GF1.__geo_interface__

log('Clean up GeoJSON')
for i in OUTPUT['features']:
    i['properties'] = {k: v for k, v in i['properties'].items()
                       if v is not None}
    i.pop('bbox', None)

log('Write output file')
with open('output-all.json', 'w') as fout:
    json.dump(OUTPUT, fout)
    
