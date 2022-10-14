his is a sample Python script.
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


geolocator = Nominatim(user_agent="CoordCheck")
geod= Geod(ellps="WGS84")
dict = OrderedDict()


def run(excelloc,shapeloc,district):
    wb = pd.read_excel(excelloc, na_values=['NA'])
    sheet = wb[wb['Comune'].str.contains(district)]
    sheet = sheet[sheet['Intervento'].str.contains('rete')]
    if (sheet.empty):
        print("There is no data from the input file for the district of " + district)
        exit()    # Use a breakpoint in the code line below to debug your script.

    sheet["Proiezione (LAT)"]=" "
    sheet["Proiezione (LNG)"]=" "

    shape = fiona.open(shapeloc)

    for i, row in sheet.iterrows():
        temp=[]
        for j in shape:
            # match delle vie tra shapefile e lavorazione
            if(j['properties']['STREET'] != None):
                '''if(row[2] in j['properties']['STREET'].upper() or  j['properties']['STREET'].upper() in row[2]):
                    temp.append(j)'''
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
            proiezione(temp,row)



    for i,row in sheet.iterrows():
        for j in dict:
            if(len(j.split(":"))>1 and row[3]==row[3]):
                if(j.split(":")[0] in row[2] and j.split(":")[1] in row[3]):
                    sheet.at[i, "Proiezione (LAT)"] = dict.get(j).x
                    sheet.at[i, "Proiezione (LNG)"] = dict.get(j).y

            if(len(j.split(":"))==1):
                if (j.split(":")[0] in row[2]):
                    sheet.at[i, "Proiezione (LAT)"] = dict.get(j).x
                    sheet.at[i, "Proiezione (LNG)"] = dict.get(j).y

    sheet.to_excel(
        "Provalo4.xlsx",
        index=False);


def proiezione(vettoreTubature,lavorazione):
    #finalTubatura = None
    minDistance = 1000000
    i=0
    tempPoint=None
    for tubatura in vettoreTubature:
        for point in tubatura["geometry"]["coordinates"]:
            if(i==1):
                line = LineString([tempPoint,point])
                if(geod.geometry_length(LineString(nearest_points(line,Point(lavorazione[9],lavorazione[8]))))<minDistance):
                    minDistance=geod.geometry_length(LineString(nearest_points(line,Point(lavorazione[9],lavorazione[8]))))
                    if(lavorazione[3]==lavorazione[3]):
                        dict[lavorazione[2]+":"+lavorazione[3]]=nearest_points(line,Point(lavorazione[9],lavorazione[8]))[0]
                    else:
                        dict[lavorazione[2]] = nearest_points(line, Point(lavorazione[9], lavorazione[8]))[0]
                i=0
            else:
                tempPoint=point
                i+=1



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
