import pandas as pd
from datetime import datetime
from meteostat import Point, Daily
from datetime import timedelta
import math
import os
# import module
import json
from geopy.geocoders import Nominatim



def WeatherStat(loc,daysBefore,daysAfter,district):

    """
    :param loc: location of the input excel file
    :param daysBefore: number of days to search before the repair date
    :param daysAfter: number of days to search after the repair date
    :param district: name of the district (e.g. Turbigo)
    :return:
    """

    # Read only the column relative to: Comune, Inizio lavori, Coordinate
    wb = pd.read_excel(loc, na_values=['NA'], usecols="B,F,I,J")

    # Filter the chosen district
    sheet= wb[wb['Comune'].str.contains(district)]
    if(sheet.empty):
        print("There is no data from the input file for the district of "+district)
        exit()
    # New columns used to insert the details of preciptations on each requested date before and after the repair date
    # initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")

    sheet["Precipitations (in mm), from "+daysBefore+" days before (in ascending order of date)"]=" "
    sheet["Precipitations (in mm), until "+daysAfter+" days after (in ascending order of date)"]=" "
    # For each date in the excel, put the mean value of the precipitation
    # calculated on the days before('yourDataInAList1') and after('YourDataInaAList2') the repair date
    # and put on prcp1 and prcp2 the details of preciptations of each day (same convention as prior comment)
    yourDataInAList1=[]
    prcp1=[]
    yourDataInAList2 = []
    prcp2 = []
    
    #For each row the column cityVillageTown is used to store a value that determines if the given coordinates belong to a city, a town or a village
    #The locNames column contains the name of the city, town or village
    locNames=[]
    cityVillageTown=[]
    
    for i, row in sheet.iterrows():
        print(row)
        print("\n")
        start1 = row[1] - timedelta(days= int(daysBefore))
        start2 = row[1]

        location = Point(row[3], row[2])
        end1 = row[1]
        end2 = row[1] + timedelta(days=int(daysAfter))
        
        #If the coordinates are not NAN the geolocaation process starts then, depending on the result, the columns
        #cityVillageTown and locNames are filled with the correct values
        if( not math.isnan(row[3]) and not math.isnan(row[2]) ):
            geolocation = geolocator.reverse(str(row[3]) + "," + str(row[2]))
            if ("city" in geolocation.raw["address"]):
                cityVillageTown.append("city")
                locNames.append(geolocation.raw["address"]["city"])
            elif("town" in geolocation.raw["address"]):
                cityVillageTown.append("town")
                locNames.append(geolocation.raw["address"]["town"])
            elif("village" in geolocation.raw["address"]):
                cityVillageTown.append("village")
                locNames.append(geolocation.raw["address"]["village"])
        else:
            locNames.append("nan")
            cityVillageTown.append("nan")
            
        #Using meteostat API
        data1 = Daily(location, start1, end1)
        data2 = Daily(location, start2, end2)
        data1 = data1.fetch()
        data2 = data2.fetch()

        #counter used to have the exact number of valid values
        count= data1.prcp.size;

        if(data1.prcp.size!=0):
            tot = 0
            #Mean value of precipitation on the days before the repair date
            for q in data1.prcp:
                prcp1.append(q)
                if not math.isnan(q):
                    tot += q
                else:
                    count=count-1;
            if count==0:
                # We don't have valid values
                tot = "nan"
            else:
                tot = tot / count
            yourDataInAList1.append(tot)
        else:
            tot = "nan"
            yourDataInAList1.append("nan")

        #Column used to store if there were or not any precipitations before the repair date
        #the row values for this column are determined from the mean value
        match tot:
            case 0.0:
                sheet.at[i, "Did it rain before the repair date ?"]="false"
            case "nan":
                sheet.at[i, "Did it rain before the repair date ?"]="nan"
            case _:
                sheet.at[i, "Did it rain before the repair date ?"]="true"

        count= data2.prcp.size;

        if (data2.prcp.size != 0):
            tot = 0
            # Mean value of precipitation on the days after the repair date
            for q in data2.prcp:
                prcp2.append(q)
                if not math.isnan(q):
                    tot += q
                else:
                    count=count-1;
            if count==0:
                # We don't have valid values
                tot = "nan"
            else:
                tot = tot / count
            yourDataInAList2.append(tot)
        else:
            tot = "nan"
            yourDataInAList2.append("nan")

        #Column used to store if there were or not any precipitations after the repair date
        #the row values for this column are determined from the mean value
        match tot:
            case 0.0:
                sheet.at[i, "Did it rain after the repair date ?"]="false"
            case "nan":
                sheet.at[i, "Did it rain after the repair date ?"]="nan"
            case _:
                sheet.at[i, "Did it rain after the repair date ?"]="true"

        #Insertion of detailed values of precipitation (in mm)
        sheet.at[i,"Precipitations (in mm), from "+daysBefore+" days before (in ascending order of date)"]=prcp1.copy()
        sheet.at[i,"Precipitations (in mm), until "+daysAfter+" days after (in ascending order of date)"]=prcp2.copy()

        prcp1.clear()
        prcp2.clear()

    #Columns used to store the mean values
    sheet.insert(6,"Mean precipitation value in the "+ daysBefore + " days before the repair date (in mm)",value=yourDataInAList1)
    sheet.insert(7,"Mean precipitation value in the "+ daysAfter + " days after the repair date (in mm)",value=yourDataInAList2)
    sheet.insert(8,"Type of location",value=cityVillageTown)
    sheet.insert(9,"Name of location",value=locNames)

    #Earliest date of observation
    xlsStartDate = sheet["Data Inizio Esito"].get(sheet["Data Inizio Esito"].index[0]).strftime("%d-%m-%Y")

    #Latest date of observation
    xlsEndDate= sheet["Data Inizio Esito"].get(sheet["Data Inizio Esito"].index[sheet["Data Inizio Esito"].size-1]).strftime("%d-%m-%Y")

    #Output document containing all the details mentioned before,
    #format of document name: "Prcp_NameOfDistrict_EarliestDate_LatestDate_past_nDaysBefore_future_nDaysAfter.xlsx"
    sheet.to_excel("./Prcp_"+district+"_"+xlsStartDate+"_"+xlsEndDate+"_past_"+daysBefore+"_future_"+daysAfter+".xlsx", index=False);


if __name__ == '__main__':
    # JSON File location
    file = open("config.json")
    jsonData = json.load(file)

    daysBefore=""
    daysAfter=""
    district=""
    loc=""
    
    #if a key does not exists or the value of the key is not given (causing variable == ""), a console input will be requested
    #in order to fill the required variable
    if("DAYSBEFORE" in jsonData.keys()):
        daysBefore=jsonData.get("DAYSBEFORE")
    if(daysBefore==""):
        daysBefore = input("Please specify for how many days before the repair you want to fetch data :\n")
        while (not daysBefore.isnumeric()):
            print("Please insert a number\n")
            daysBefore = input("Please specify for how many days before the repair you want to fetch data :\n")


    if("DAYSAFTER" in jsonData.keys()):
        daysAfter= jsonData.get("DAYSAFTER")
    if(daysAfter==""):
        daysAfter = input("Please specify  for how many days after the repair you want to fetch data :\n")
        while (not daysAfter.isnumeric()):
            print("Please insert a number")
            daysAfter = str(input("Please specify for how many days after the repair you want to fetch data :\n"))

    if("DISTRICT" in jsonData.keys()):
        district = jsonData.get("DISTRICT").upper()
    if(district==""):
        district = input("Please specify the district :\n").upper()

    if("EXCELLOC" in jsonData.keys()):
       loc= jsonData.get("EXCELLOC")
    if(loc==""):
        loc= input("Please specify location of excel file in input :\n")

    #When every required variable is filled the script checks whether the source excle file exists before calling the function
    if(os.path.isfile(loc)):
        WeatherStat(loc,str(daysBefore),str(daysAfter),district)
    else:
        print("ERROR: Excel source file not found")
