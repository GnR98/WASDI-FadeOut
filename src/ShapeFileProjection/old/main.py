# This is a sample Python script.
import pandas as pd
import os
import shapely.geometry.linestring
# import module
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from pyproj import Geod
from pyproj import Transformer
import fiona
import osgeo.osr as osr
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


    def getAllProjections(self, excelloc, shapeloc, district):
        """
        Filter the Excel file for all the
        Create a new Excel file called "NewGeolocation_ShapefileProj_"+district+".xlsx" with all the columns inside
        NewGeolocation plus two more containing the coordinates of the projected points

        :param self:
        :param pipesVector: Array containing all the candidate pipes on which we try the projection
        :param interventionRow: Row formatted like the ones inside  the NewGeolocation file and thus containing
                                 all the information of the intervention
        :return:
        """

        # check inputs
        if not os.path.exists(excelloc):
            raise ValueError(f"{excelloc} is not valid path")
        if not os.path.exists(shapeloc):
            raise ValueError(f"{shapeloc} is not valid path")

        #read excel file
        wb = pd.read_excel(excelloc, na_values=['NA'])
        #filtering of excel file considering only the selected "Comune"
        # and all the row containing the "rete" word inside the "Intervento" column
        self.sheet = wb[wb['Comune'].str.contains(district)]
        self.sheet = self.sheet[self.sheet['Intervento'].str.contains('rete')]
        #check if we've got a non empty result
        if (self.sheet.empty):
            raise SystemExit("There is no data from the input file for the district of " + district)
            print("There is no data from the input file for the district of " + district)
            exit()    # Use a breakpoint in the code line below to debug your script.

        #creation of the 2 new column used to insert the projected coordinates
        self.sheet["Proiezione (LAT)"]=" "
        self.sheet["Proiezione (LNG)"]=" "

        #shape object
        shape = fiona.open(shapeloc)

        # match between the street names of shape and excel files
        for i, row in self.sheet.iterrows():
            temp=[]
            for j in shape:
                if(j['properties']['STREET'] != None):
                    if (j['properties']['STREET'].__contains__(".")):
                        if (j['properties']['STREET'].split(".")[1].upper() in row["Indirizzo"]):
                            temp.append(j)
                    if (row["Indirizzo"].__contains__(".")):
                        if (row["Indirizzo"].split(".")[1] in j['properties']['STREET'].upper()):
                            temp.append(j)
                    else:
                        if (row["Indirizzo"] in j['properties']['STREET'].upper() or j['properties']['STREET'].upper() in row["Indirizzo"]):
                            temp.append(j)
            if(temp):
                self.projectOnClosestPipe(temp, row)


        #take all the coordinates in self.dict and store it on the excel file
        for i,row in self.sheet.iterrows():
            for j in self.dict:
                if(len(j.split(":"))>1 and row["Indirizzo"]==row["Indirizzo"] and row["Civico"]==row["Civico"]):
                    if(j.split(":")[0] in row["Indirizzo"] and j.split(":")[1] in row["Civico"]):
                        self.sheet.at[i, "Proiezione (LAT)"] = self.dict.get(j).x
                        self.sheet.at[i, "Proiezione (LNG)"] = self.dict.get(j).y

                if(len(j.split(":"))==1):
                    if (j.split(":")[0] in row["Indirizzo"]):
                        self.sheet.at[i, "Proiezione (LAT)"] = self.dict.get(j).x
                        self.sheet.at[i, "Proiezione (LNG)"] = self.dict.get(j).y
        shapename = os.path.basename(shapeloc).split('.')[0]
        self.sheet.to_excel(
            "NewGeolocation_" + shapename + "_" + district + ".xlsx", index=False)


    def projectOnClosestPipe(self, pipesVector, interventionRow):

        """
        Project the point inside the interventionRow on all the pipes inside the pipesVector in order to find
        the closest one, then fill the dict attribute with key = intervention address and value = closest coordinates

        :param self:
        :param pipesVector: Array containing all the candidate pipes on which we try the projection
        :param interventionRow: Row formatted like the ones inside  the NewGeolocation file and thus containing
                                all the information of the intervention
        :return:
        """
        #finalPipe = None
        minDistance = 1000000
        i=0
        tempPoint=None
        #take the min distance between the
        for tubatura in pipesVector:
            for point in tubatura["geometry"]["coordinates"]:
                if(i==1):
                    line = LineString([tempPoint,tuple(reversed(point))])
                    if(self.geod.geometry_length(LineString(nearest_points(line, Point(interventionRow["COORD_X SNAPSHOT GIS (LAT)"], interventionRow["COORD_Y SNAPSHOT GIS (LNG)"]))))<minDistance):
                        minDistance=self.geod.geometry_length(LineString(nearest_points(line, Point(interventionRow["COORD_X SNAPSHOT GIS (LAT)"], interventionRow["COORD_Y SNAPSHOT GIS (LNG)"]))))
                        if(interventionRow["Civico"]==interventionRow["Civico"]):
                            self.dict[interventionRow["Indirizzo"] + ":" + interventionRow["Civico"]]=nearest_points(line, Point(interventionRow["COORD_X SNAPSHOT GIS (LAT)"], interventionRow["COORD_Y SNAPSHOT GIS (LNG)"]))[0]
                        else:
                            self.dict[interventionRow["Indirizzo"]] = nearest_points(line, Point(interventionRow["COORD_X SNAPSHOT GIS (LAT)"], interventionRow["COORD_Y SNAPSHOT GIS (LNG)"]))[0]
                    i=0
                else:
                    tempPoint=point
                    i+=1

    def convertShapefile(self,shapeloc):

        """
        Convert and substitute the coordinates in the selected shapefile from EPSG 32632 to WGS84.
        \b
        --THIS WILL OVERWRITE THE ORIGINAL COORDINATES--
        \b
        After a successful use of this function the conversion will not be needed anymore for the selected shapefile

        :param self:
        :param shapeloc: Absolute location of the shapefile that needs to be converted
        :return:
        """
        # check inputs
        if not os.path.exists(shapeloc):
            raise ValueError(f"{shapeloc} is not valid path")

        srs = osr.SpatialReference()  ###
        srs.SetFromUserInput("EPSG:4326")  ###
        crs = srs.ExportToWkt()
        # crs = from_epsg(4326)
        shape = fiona.open(shapeloc)
        transformer = Transformer.from_crs("EPSG:32632", "EPSG:4326")
        shapeDict = OrderedDict()

        # conversione coordinate da epsg 32632 a wgs84 e correzione vie delle tubature
        for i in shape:
            # print(i)
            temp = []
            shapeDict[i["id"]] = i
            for j in i["geometry"]["coordinates"]:
                p = transformer.transform(j[0], j[1])
                temp.append(tuple(reversed(p)))
            # i["geometry"]["coordinates"] = temp
            shapeDict[i["id"]]["geometry"]["coordinates"] = temp
            # inserisco la via corretta nello shape file controllando le coordinate
            if ("road" in self.do_reverse(temp[0]).raw['address']):
                shapeDict[i["id"]]['properties']['STREET'] = self.do_reverse(temp[0]).raw['address']['road']

            # print("\n")

        my_schema = {'properties': OrderedDict(
            [('OBJECTID', 'int:10'), ('NAME_NUM', 'str:254'), ('MUN', 'str:254'), ('STREET', 'str:254'),
             ('ISTAT', 'str:6'), ('MUN_OWN', 'str:254'), ('MAIN_FUNCT', 'str:254'), ('SPEC_FUNCT', 'str:254'),
             ('HYDR_FUNCT', 'str:254'), ('WAT_QUAL', 'str:254'), ('OPERATOR', 'str:254'), ('STATUS', 'str:254'),
             ('DETERMINAT', 'str:254'), ('DIAMETER', 'str:254'), ('MATERIAL', 'str:254'), ('MATERIAL_T', 'str:254'),
             ('LENGTH', 'float:31.15'), ('GROUND_ELE', 'float:31.15'), ('COVERING', 'float:31.15'),
             ('SURF_POS', 'str:254'), ('PIPE_NAME', 'str:254'), ('START_NODE', 'str:254'), ('END_NODE', 'str:254'),
             ('DATE_ACQ', 'date'), ('DATE_INS', 'date'), ('REMARK', 'str:254'), ('CREA_DATE', 'date'),
             ('LA_ED_DATE', 'date'), ('DMA', 'str:254')]), 'geometry': 'LineString'}

        with fiona.open(shapeloc, 'w', driver='ESRI Shapefile', schema=my_schema,
                        crs=crs) as output:
            for key, value in shapeDict.items():
                output.write({'geometry': value["geometry"], 'properties': value["properties"]})

    def do_reverse(self, coordinate, attempt=1, max_attempts=5):

        """
        Try the reverse geocoding operation at most a number of times equal to max_attempts.
        It will return the same object that the reverse method of the Nominatim API returns

        :param self:
        :param coordinate: coordinates of the place you want to execute the reverse geocoding
        :param attempt: current attempt (you don't need to specify it)
        :param max_attempts: maximum number of attempts to try the operation
        :return:
        """
        try:
            return self.geolocator.reverse(coordinate)
        except GeocoderTimedOut:
            if attempt <= max_attempts:
                return self.do_reverse(coordinate, attempt=attempt + 1)
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

            proj= Projection()

            # If the shapefile has not been corrected yet uncomment the line below (correction is needed only once for each shapefile)
            #proj.convertShapefile(shapeloc)

            proj.getAllProjections(excelloc, shapeloc, district)
        else:
            print("ERROR: Shape source file not found")
    else:
        print("ERROR: Excel source file not found")
