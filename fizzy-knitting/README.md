# OSM Rail Network in Great Britain

Using [OSMnx](https://github.com/gboeing/osmnx) (Python for Street Maps) to download [Open Street Map (OSM)](https://www.openstreetmap.org) rail-data using the [Overpass API](http://overpass-api.de)

## Creating the datafiles and associate GeoJSON format report

Once the dependencies are met run the script to gather the data:

    $ ./prepublish

This will download and create `ESRI Shape` files in the `shp` directory for all Towns as well as all locations in Great Britian, as well as a `Leaflet` JavaScript visualisation using the Town data in a GeoJSON format.

## Dependencies

These are environment and project dependencies.

### `python` dependencies

For ease of use manage package `python` packages dependencies with a local virtual environment `venv`:

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install osmnx

### If missing install the `python virtualenv` package

    $ sudo apt install virtualenv
    
# Data and Map Tile License

[Open Street Map](https://www.openstreetmap.org) data is licensed under the [Open Data Commons Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/) 

[Open Street Map tiles](https://www.openstreetmap.org/copyright) are licenced by CC BY-SA (c) OpenStreetMap contributors
