# Population Density in Great Britain

The Office for National Statistics and the Nation Record of Scotland provide population and shapefile data for the 2011 census for Great Britain. This creates population density by Output Area (OA11) in a number of formats including an interactive web visualisation.

## Creating the datafiles and associated GeoJSON and vector tiles

Once the `tippecanoe` build and `python` are met run the script to create the population density output for England, Scotland and Wales:

    $ ./prepublish

This downloads Census Output Area population `ESRI Shape` files and creates the `shp`, `GeoJSON` in the base directory, and the vector-tiles in the `tiles` directory. The vector-tiles layer created using a local build of the `Mapbox tippecanoe` toolset uses the `Leaflet` JavaScript library to create an interactive web visualisation.

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
* Source: Office for National Statistics licensed under the Open Government Licence v.3.0. 
* Source: National Records Scotland data (c) Crown copyright and database right 2021.
* Contains OS data (c) Crown copyright and database right 2021.
