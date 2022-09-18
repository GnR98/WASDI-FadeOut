import pandas as pd
from datetime import datetime
from meteostat import Point, Daily
from datetime import timedelta
import math
import os
# import module
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="CoordCheck")


def Checker(loc):
    sheet = pd.read_excel(loc, na_values=['NA'])
    for i, row in sheet.iterrows():

        if (not math.isnan(row[9]) and not math.isnan(row[8])):

            geolocation = do_reverse(str(row[9]) + "," + str(row[8]))
            if ("city" in geolocation.raw["address"] and row["Comune"].upper() not in geolocation.raw["address"]["city"].upper()):
                util(sheet,i,row)
            elif ("town" in geolocation.raw["address"] and row["Comune"].upper() not in geolocation.raw["address"]["town"].upper()):
                util(sheet,i,row)
            elif ("village" in geolocation.raw["address"] and row["Comune"].upper() not in geolocation.raw["address"]["village"].upper()):
                util(sheet,i,row)
    sheet.to_excel("NewGeolocation.xlsx", index=False);



def util(sheet,i,row):
    comune=row[1]
    via=row[2]
    civico=row[3]
    if(do_geocode(str(comune) + " " + str(via)+" "+str(civico))!=None):
        sheet.at[i,"COORD_Y SNAPSHOT GIS (LNG)"]=do_geocode(str(comune) + " " + str(via)+" "+str(civico)).latitude
        sheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"] = do_geocode(str(comune) + " " + str(via)+" "+str(civico)).longitude
    elif(do_geocode(str(comune) + " " + str(via))!=None):
        sheet.at[i, "COORD_Y SNAPSHOT GIS (LNG)"] = do_geocode(
            str(comune) + " " + str(via)).latitude
        sheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"] = do_geocode(
            str(comune) + " " + str(via)).longitude
    elif (do_geocode(str(comune)) != None):
        sheet.at[i, "COORD_Y SNAPSHOT GIS (LNG)"] = do_geocode(
            str(comune)).latitude
        sheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"] = do_geocode(
            str(comune)).longitude


def do_geocode(address, attempt=1, max_attempts=5):
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return do_geocode(address, attempt=attempt+1)
        raise

def do_reverse(coordinate, attempt=1, max_attempts=5):
    try:
        return geolocator.reverse(coordinate)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return do_reverse(coordinate, attempt=attempt+1)
        raise

if __name__ == '__main__':
    loc = input("Please specify location of excel file in input :\n")
    if (os.path.isfile(loc)):
        Checker(loc)
    else:
        print("ERROR: Excel source file not found")