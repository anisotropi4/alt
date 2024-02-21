# Railway and Trunk Roads in Great Britain

This extracts railway and trunk road data from Open Street Map (OSM) data using the `python osmnx` module and presents these in a number of formats including an interactive web visualisation.

## Creating the datafiles and associated GeoJSON and vector tiles

Once the `tippecanoe` build and `python` dependencies are met run the script to create the railway and trunk road output for England, Scotland and Wales:

    $ ./prepublish

This downloads railway and trunk road data from OSM using [overpass api](http://overpass-api.de/) and creates ESRI Shape files in the `shp` directory, `GeoJSON` in the base directory, and the vector-tiles in the `tiles` directory. The vector-tiles layer created using a local build of the `Mapbox tippecanoe` toolset uses the `Leaflet` JavaScript library to create an interactive web visualisation.

## Dependencies

### `tippecanoe` dependencies

To download and install the `Mapbox tippecanoe` tool run the script:

    $ ./build.sh
    
#### If `tippecanoe` is missing compile dependencies 

Install the `build-essential`, `libsqlite3` and `zlib1g-dev` libraries. 

On an Debian based Linux system:

    $ sudo apt install build-essential libsqlite3-dev zlib1g-dev
    
### `python` dependencies

For ease of use manage package `python` packages dependencies with a local virtual environment `venv`:

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

#### If `virtualenv` is missing install the `python virtualenv` package

    $ sudo apt install virtualenv

# Data License

Licenses for the digital boundaries and reference map data:
* OpenStreetMap data copyright [OpenStreetMap contributors](www.openstreetmap.org)

# Thanks to

* [OpenStreetMap](https://www.openstreetmap.org) contributors
* [Overpass API](http://overpass-api.de/)
* [OSMnx](https://github.com/gboeing/osmnx)

# Reference

Boeing, G. 2017. "OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks." Computers, Environment and Urban Systems 65, 126-139. 
doi:10.1016/j.compenvurbsys.2017.05.004
