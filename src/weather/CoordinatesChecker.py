from meteostat import Point, Daily
from datetime import timedelta
import math
import os
# import module
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class CoordinatesChecker():

    def __init__(self):
        self.sheet=None
        self.geolocator = Nominatim(user_agent="CoordCheck")

    def Checker(self,loc):

        if not os.path.exists(loc):
            raise ValueError(f"{loc} is not valid path")

        sheet = pd.read_excel(loc, na_values=['NA'])
        for i, row in sheet.iterrows():

            if (not math.isnan(row[9]) and not math.isnan(row[8])):

                geolocation = self.do_reverse(str(row[9]) + "," + str(row[8]))
                if ("city" in geolocation.raw["address"] and row["Comune"].upper() not in geolocation.raw["address"]["city"].upper()):
                    self.util(i,row)
                elif ("town" in geolocation.raw["address"] and row["Comune"].upper() not in geolocation.raw["address"]["town"].upper()):
                    self.util(i,row)
                elif ("village" in geolocation.raw["address"] and row["Comune"].upper() not in geolocation.raw["address"]["village"].upper()):
                    self.util(i,row)
        sheet.to_excel("NewGeolocation.xlsx", index=False);



    def util(self,i,row):
        comune=str(row[1])
        via=str(row[2])
        civico=str(row[3])
        if(self.do_geocode(comune + " " + via+" "+civico)!=None):
            self.sheet.at[i,"COORD_Y SNAPSHOT GIS (LNG)"]=self.do_geocode(comune + " " + via+" "+civico).latitude
            self.sheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"] = self.do_geocode(comune + " " + via+" "+civico).longitude
        elif(self.do_geocode(comune + " " + via)!=None):
            self.sheet.at[i, "COORD_Y SNAPSHOT GIS (LNG)"] = self.do_geocode(
                comune + " " + via).latitude
            self.sheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"] = self.do_geocode(
                comune + " " + via).longitude
        elif (self.do_geocode(comune) != None):
            self.sheet.at[i, "COORD_Y SNAPSHOT GIS (LNG)"] = self.do_geocode(
                comune).latitude
            self.sheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"] = self.do_geocode(
                comune).longitude


    def do_geocode(self,address, attempt=1, max_attempts=5):
        try:
            return self.geolocator.geocode(address)
        except GeocoderTimedOut:
            if attempt <= max_attempts:
                return self.do_geocode(address, attempt=attempt+1)
            raise

    def do_reverse(self,coordinate, attempt=1, max_attempts=5):
        try:
            return self.geolocator.reverse(coordinate)
        except GeocoderTimedOut:
            if attempt <= max_attempts:
                return self.do_reverse(coordinate, attempt=attempt+1)
            raise

if __name__ == '__main__':
    loc = input("Please specify location of excel file in input :\n")
    checker = CoordinatesChecker()
    checker.Checker(loc)
