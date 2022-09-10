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

    sheet["Dettaglio (in mm), "+daysBefore+" giorni prima (in ordine crescente di data)"]=" "
    sheet["Dettaglio (in mm), "+daysAfter+" giorni dopo (in ordine crescente di data)"]=" "
    # For each date in the excel, put the mean value of the precipitation
    # calculated on the days before('yourDataInAList1') and after('YourDataInaAList2') the repair date
    # and put on data1 and data2 the details of preciptations of each day (same convention as prior comment)
    yourDataInAList1=[]
    prcp1=[]
    yourDataInAList2 = []
    prcp2 = []
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
                sheet.at[i, "Ha piovuto prima dei lavori ?"]="false"
            case "nan":
                sheet.at[i, "Ha piovuto prima dei lavori ?"]="nan"
            case _:
                sheet.at[i, "Ha piovuto prima dei lavori ?"]="true"

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
                sheet.at[i, "Ha piovuto dopo i lavori ?"]="false"
            case "nan":
                sheet.at[i, "Ha piovuto dopo i lavori ?"]="nan"
            case _:
                sheet.at[i, "Ha piovuto dopo i lavori ?"]="true"

        #Insertion of detailed values of precipitation (in mm)
        sheet.at[i,"Dettaglio (in mm), "+ daysBefore + " giorni prima (in ordine crescente di data)"]=prcp1.copy()
        sheet.at[i,"Dettaglio (in mm), "+ daysAfter + " giorni dopo (in ordine crescente di data)"]=prcp2.copy()

        prcp1.clear()
        prcp2.clear()

    #Columns used to store the mean values
    sheet.insert(6,"Media precipitazioni nei "+ daysBefore + " giorni prima dalla data di inizio(in mm)",value=yourDataInAList1)
    sheet.insert(7,"Media precipitazioni nei "+ daysAfter + " giorni dopo la data di inizio(in mm)",value=yourDataInAList2)
    sheet.insert(8,"Type of location",value=cityVillageTown)
    sheet.insert(9,"Dettaglio località",value=locNames)

    #Earliest date of observation
    xlsStartDate = sheet["Data Inizio Esito"].get(sheet["Data Inizio Esito"].index[0]).strftime("%d-%m-%Y")

    #Latest date of observation
    xlsEndDate= sheet["Data Inizio Esito"].get(sheet["Data Inizio Esito"].index[sheet["Data Inizio Esito"].size-1]).strftime("%d-%m-%Y")

    #Output document containing all the details mentioned before,
    #format of document name: "Prcp_NameOfDistrict_EarliestDate_LatestDate_past_nDaysBefore_future_nDaysAfter.xlsx"
    sheet.to_excel("./Prcp_"+district+"_"+xlsStartDate+"_"+xlsEndDate+"_past_"+daysBefore+"_future_"+daysAfter+".xlsx", index=False);


if __name__ == '__main__':
    # File location
    file = open("config.json")
    jsonData = json.load(file)

    daysBefore=""
    daysAfter=""
    district=""
    loc=""

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


    if(os.path.isfile(loc)):
        WeatherStat(loc,str(daysBefore),str(daysAfter),district)
    else:
        print("ERROR: Excel source file not found")
