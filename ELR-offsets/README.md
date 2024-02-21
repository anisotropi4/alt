# Network Model (ELR) offsets 

Under the UK Freedom of Information Act (FOIA) 2000 request FOI2020/00232 Network Rail have published [Network Model Engineering Line of Route (ELR) offsets](https://www.whatdotheyknow.com/request/conversion_tables_for_latitude_a) as WG84 longitude and latitude links. 

These scripts extracts these links convert these to link and point GeoJSON layers. The script also creates `ESRI Shape` files.

## Creating the datafiles and associate GeoJSON format report

Once the dependencies to create the report are met run the script:

    $ ./prepublish

This will download the report and create `ESRI Shape` files in the `shp`, as well as a `Leaflet` JavaScript visualisation using the network model data in GeoJSON format.

## Dependencies

These are environment and project dependencies.

### `python` dependencies

For ease of use manage package `python` packages dependencies with a local virtual environment `venv`:

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

### If missing install the `python virtualenv` package

    $ sudo apt install virtualenv
    
# Data License

FOI reference data:

The data is protected under copyright as set out [here](https://www.whatdotheyknow.com/request/643748/response/1539326/attach/2/FOI202000232%20Response.pdf).

This indicates that the data may be used for activities such as private study and non-commerial research and any other purpose authorised by exception in current law. Any other re-use such as commerical publication would require permission of the copyright holder.
