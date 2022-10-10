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

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import  fiona
from collections import OrderedDict
from shapely.geometry import shape
import geopandas as gpd
from pyproj import CRS

geolocator = Nominatim(user_agent="CoordCheck")


def run(excelloc,shapeloc,district):
    wb = pd.read_excel(excelloc, na_values=['NA'])
    sheet = wb[wb['Comune'].str.contains(district)]
    sheet = sheet[sheet['Intervento'].str.contains('rete')]
    if (sheet.empty):
        print("There is no data from the input file for the district of " + district)
        exit()    # Use a breakpoint in the code line below to debug your script.

    sheet["Proiezione"]=" "

    shape = fiona.open(shapeloc)
    print(shape.schema)
    {'geometry': 'LineString', 'properties': OrderedDict([(u'FID', 'float:11')])}
    # first feature of the shapefile
    transformer = Transformer.from_crs("EPSG:32632", "EPSG:4326")

    #conversione coordinate da epsg 32632 a wgs84 e correzione vie delle tubature
    for i in shape:
        #print(i)
        temp=[]
        for j in i["geometry"]["coordinates"]:
            temp.append(transformer.transform(j[0], j[1]))
        i["geometry"]["coordinates"] = temp
        #inserisco la via corretta nello shape file controllando le coordinate
        if("road" in do_reverse(temp[0]).raw['address']):
            i['properties']['STREET'] = do_reverse(temp[0]).raw['address']['road']

        #print("\n")

    for i, row in sheet.iterrows():
        temp=[]
        for i in shape:
            # match delle vie tra shapefile e lavorazione
            if(i['properties']['STREET'] != None):
                if(row[2] in i['properties']['STREET'].upper() or  i['properties']['STREET'].upper() in row[2]):
                    temp.append(i)
        if(temp):
            proiezione(temp,row)







    #pts3 = gpd2.geometry.unary_union

'''def near(point, pts=pts3):
    # find the nearest point and return the corresponding Place value
    nearest = gpd2.geometry == nearest_points(point, pts)[1]
    return gpd2[nearest].Place.get_values()[0]

gpd1['Nearest'] = gpd1.apply(lambda row: near(row.geometry), axis=1)'''


def proiezione(vettoreTubature,lavorazione):
    print(vettoreTubature)

def do_reverse(coordinate, attempt=1, max_attempts=5):
    try:
        return geolocator.reverse(coordinate)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return do_reverse(coordinate, attempt=attempt+1)
        raise

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    district = ""
    excelloc = ""
    shapeloc=""
    file = open("config.json")
    jsonData = json.load(file)

    if ("EXCELLOC" in jsonData.keys()):
        excelloc = jsonData.get("EXCELLOC")
    if (excelloc == ""):
        excelloc = input("Please specify location of excel file in input :\n")

    if ("SHAPELOC" in jsonData.keys()):
        shapeloc = jsonData.get("SHAPELOC")
    if (shapeloc == ""):
        shapeloc = input("Please specify location of excel file in input :\n")

    if ("DISTRICT" in jsonData.keys()):
        district = jsonData.get("DISTRICT").upper()
    if (district == ""):
        district = input("Please specify the district :\n").upper()

    if (os.path.isfile(excelloc)):
        if(os.path.isfile(shapeloc)):
            run(excelloc,shapeloc,district)
        else:
            print("ERROR: Shape source file not found")
    else:
        print("ERROR: Excel source file not found")
