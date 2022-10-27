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
import  fiona
from collections import OrderedDict
from shapely.geometry import shape
import geopandas as gpd
from pyproj import CRS
from shapely.geometry import LineString
from fiona.crs import from_epsg


geolocator = Nominatim(user_agent="CoordCheck")


def run(shapeloc):
    crs = from_epsg(4326)
    shape = fiona.open(shapeloc)
    transformer = Transformer.from_crs("EPSG:32632", "EPSG:4326")
    shapeDict= OrderedDict()

    #conversione coordinate da epsg 32632 a wgs84 e correzione vie delle tubature
    for i in shape:
        #print(i)
        temp=[]
        shapeDict[i["id"]]=i
        for j in i["geometry"]["coordinates"]:
            temp.append(transformer.transform(j[0], j[1]))
        #i["geometry"]["coordinates"] = temp
        shapeDict[i["id"]]["geometry"]["coordinates"]=temp
        #inserisco la via corretta nello shape file controllando le coordinate
        if("road" in do_reverse(temp[0]).raw['address']):
            shapeDict[i["id"]]['properties']['STREET'] = do_reverse(temp[0]).raw['address']['road']

        #print("\n")

    my_schema= {'properties': OrderedDict([('OBJECTID', 'int:10'), ('NAME_NUM', 'str:254'), ('MUN', 'str:254'), ('STREET', 'str:254'), ('ISTAT', 'str:6'), ('MUN_OWN', 'str:254'), ('MAIN_FUNCT', 'str:254'), ('SPEC_FUNCT', 'str:254'), ('HYDR_FUNCT', 'str:254'), ('WAT_QUAL', 'str:254'), ('OPERATOR', 'str:254'), ('STATUS', 'str:254'), ('DETERMINAT', 'str:254'), ('DIAMETER', 'str:254'), ('MATERIAL', 'str:254'), ('MATERIAL_T', 'str:254'), ('LENGTH', 'float:31.15'), ('GROUND_ELE', 'float:31.15'), ('COVERING', 'float:31.15'), ('SURF_POS', 'str:254'), ('PIPE_NAME', 'str:254'), ('START_NODE', 'str:254'), ('END_NODE', 'str:254'), ('DATE_ACQ', 'date'), ('DATE_INS', 'date'), ('REMARK', 'str:254'), ('CREA_DATE', 'date'), ('LA_ED_DATE', 'date'), ('DMA', 'str:254')]), 'geometry': 'LineString'}

    with fiona.open(shapeloc.removesuffix(".shp")+"prova.shp", 'w', driver='ESRI Shapefile', schema=my_schema, crs=crs) as output:
        for key, value in shapeDict.items():
            output.write({'geometry': value["geometry"], 'properties': value["properties"]})



def do_reverse(coordinate, attempt=1, max_attempts=5):
    try:
        return geolocator.reverse(coordinate)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return do_reverse(coordinate, attempt=attempt+1)
        raise

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    shapeloc=""
    file = open("config.json")
    jsonData = json.load(file)



    if ("SHAPELOC" in jsonData.keys()):
        shapeloc = jsonData.get("SHAPELOC")
    if (shapeloc == ""):
        shapeloc = input("Please specify location of excel file in input :\n")


    if(os.path.isfile(shapeloc)):
        run(shapeloc)
    else:
        print("ERROR: Shape source file not found")
