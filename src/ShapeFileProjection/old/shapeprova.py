# This is a sample Python script.
import pandas as pd
import math
import os

import shapely.geometry.linestring
from shapely.ops import nearest_points
# import module
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from pyproj import Transformer
import geopy.distance
# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import fiona
from collections import OrderedDict
from ShapeProj.ShapeProjection import Projection
from fiona.crs import from_epsg
from shapely.geometry import shape
import geopandas as gpd
from pyproj import CRS
from shapely.geometry import LineString

if __name__ == '__main__':
    with fiona.open("C:\\Users\\Matteo\\Desktop\\Turbigo\\_EXPORT_MODELLAZIONE_IDRAULICA\\WAT_PIPE.shp", "r") as src:
        schema = src.schema
        driver = src.driver
        crs = from_epsg(32632)
        with fiona.open("C:\\Users\\Matteo\\Desktop\\Turbigo\\_EXPORT_MODELLAZIONE_IDRAULICA\\Test_shape_EPGS32632.shp", 'w',crs=crs,
                        driver=driver, schema=schema) as output:
            for i in src:
                if (i['properties']['STREET'] != None):
                    if i['properties']['STREET'].upper()=="VIA NOSATE" :
                        output.write(i)

    # shapec = Projection()
    # shapec.convertShapefile("C:\\Users\\Matteo\\Desktop\\Turbigo\\_EXPORT_MODELLAZIONE_IDRAULICA\\Test_shape_EPGS4326.shp")
    # shapec.getAllProjections("C:\\Users\\Matteo\\PycharmProjects\\SoilMoisture\\ShapeProj\\Sheets\\Test_shape_Turbigo.xlsx",
    #                          "C:\\Users\\Matteo\\PycharmProjects\\SoilMoisture\\ShapeProj\\Sheets\\Test_shape_EPGS4326.shx", "turbigo")
