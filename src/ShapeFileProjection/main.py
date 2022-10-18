import pandas as pd
import os
import shapely.geometry.linestring
# import module
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from pyproj import Geod
import  fiona
from collections import OrderedDict
from shapely.geometry import shape
from shapely.geometry import LineString,Point
from shapely.ops import nearest_points



class Projection():

    def __init__(self):
        self.sheet = None
        self.geod = Geod(ellps="WGS84")
        self.geolocator = Nominatim(user_agent="CoordCheck")
        self.dict = OrderedDict()


    def run(self,excelloc,shapeloc,district):
        wb = pd.read_excel(excelloc, na_values=['NA'])
        self.sheet = wb[wb['Comune'].str.contains(district)]
        self.sheet = self.sheet[self.sheet['Intervento'].str.contains('rete')]
        if (self.sheet.empty):
            print("There is no data from the input file for the district of " + district)
            exit()    # Use a breakpoint in the code line below to debug your script.

        self.sheet["Proiezione (LAT)"]=" "
        self.sheet["Proiezione (LNG)"]=" "

        shape = fiona.open(shapeloc)

        for i, row in self.sheet.iterrows():
            temp=[]
            for j in shape:
                # match delle vie tra shapefile e lavorazione
                if(j['properties']['STREET'] != None):
                    if (j['properties']['STREET'].__contains__(".")):
                        if (j['properties']['STREET'].split(".")[1].upper() in row[2]):
                            temp.append(j)
                    if (row[2].__contains__(".")):
                        if (row[2].split(".")[1] in j['properties']['STREET'].upper()):
                            temp.append(j)
                    else:
                        if (row[2] in j['properties']['STREET'].upper() or j['properties']['STREET'].upper() in row[2]):
                            temp.append(j)
            if(temp):
                self.proiezione(temp,row)



        for i,row in self.sheet.iterrows():
            for j in self.dict:
                if(len(j.split(":"))>1 and row[3]==row[3]):
                    if(j.split(":")[0] in row[2] and j.split(":")[1] in row[3]):
                        self.sheet.at[i, "Proiezione (LAT)"] = self.dict.get(j).x
                        self.sheet.at[i, "Proiezione (LNG)"] = self.dict.get(j).y

                if(len(j.split(":"))==1):
                    if (j.split(":")[0] in row[2]):
                        self.sheet.at[i, "Proiezione (LAT)"] = self.dict.get(j).x
                        self.sheet.at[i, "Proiezione (LNG)"] = self.dict.get(j).y

        self.sheet.to_excel(
            "Provalo4.xlsx",
            index=False);


    def proiezione(self,vettoreTubature,lavorazione):
        #finalTubatura = None
        minDistance = 1000000
        i=0
        tempPoint=None
        for tubatura in vettoreTubature:
            for point in tubatura["geometry"]["coordinates"]:
                if(i==1):
                    line = LineString([tempPoint,point])
                    if(self.geod.geometry_length(LineString(nearest_points(line,Point(lavorazione[9],lavorazione[8]))))<minDistance):
                        minDistance=self.geod.geometry_length(LineString(nearest_points(line,Point(lavorazione[9],lavorazione[8]))))
                        if(lavorazione[3]==lavorazione[3]):
                            self.dict[lavorazione[2]+":"+lavorazione[3]]=nearest_points(line,Point(lavorazione[9],lavorazione[8]))[0]
                        else:
                            self.dict[lavorazione[2]] = nearest_points(line, Point(lavorazione[9], lavorazione[8]))[0]
                    i=0
                else:
                    tempPoint=point
                    i+=1


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
            proj= Projection()
            proj.run(excelloc,shapeloc,district)
        else:
            print("ERROR: Shape source file not found")
    else:
        print("ERROR: Excel source file not found")
