import numpy as np
import pandas as pd
from datetime import datetime
from meteostat import Point, Daily
from datetime import timedelta
import math
from collections import OrderedDict
import os



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
    sheet["Dettaglio (in mm), "+daysBefore+" giorni prima (in ordine crescente di data)"]=" "
    sheet["Dettaglio (in mm), "+daysAfter+" giorni dopo (in ordine crescente di data)"]=" "

    # For each date in the excel, put the mean value of the precipitation
    # calculated on the days before('YourDataInAList1') and after('YourDataInaAList2') the repair date
    # and put on Data1 and Data2 the details of preciptations of each day (same convention as prior comment)
    YourDataInAList1=[]
    Data1=[]
    YourDataInAList2 = []
    Data2 = []
    for i, row in sheet.iterrows():
        print(row)
        print("\n")
        start1 = row[1] - timedelta(days= int(daysBefore))
        start2 = row[1]

        location = Point(row[3], row[2])
        end1 = row[1]
        end2 = row[1] + timedelta(days=int(daysAfter))


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
                Data1.append(q)
                if not math.isnan(q):
                    tot += q
                else:
                    count=count-1;
            if count==0:
                # We don't have valid values
                tot = "nan"
            else:
                tot = tot / count
            YourDataInAList1.append(tot)
        else:
            tot = "nan"
            YourDataInAList1.append("nan")

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
                Data2.append(q)
                if not math.isnan(q):
                    tot += q
                else:
                    count=count-1;
            if count==0:
                # We don't have valid values
                tot = "nan"
            else:
                tot = tot / count
            YourDataInAList2.append(tot)
        else:
            tot = "nan"
            YourDataInAList2.append("nan")

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
        sheet.at[i,"Dettaglio (in mm), "+ daysBefore + " giorni prima (in ordine crescente di data)"]=Data1.copy()
        sheet.at[i,"Dettaglio (in mm), "+ daysAfter + " giorni dopo (in ordine crescente di data)"]=Data2.copy()

        Data1.clear()
        Data2.clear()

    #Columns used to store the mean values
    sheet.insert(6,"Media precipitazioni nei "+ daysBefore + " giorni prima dalla data di inizio(in mm)",value=YourDataInAList1)
    sheet.insert(7,"Media precipitazioni nei "+ daysAfter + " giorni dopo la data di inizio(in mm)",value=YourDataInAList2)

    #Earliest date of observation
    xlsStartDate = sheet["Data Inizio Esito"].get(sheet["Data Inizio Esito"].index[0]).strftime("%d-%m-%Y")

    #Latest date of observation
    xlsEndDate= sheet["Data Inizio Esito"].get(sheet["Data Inizio Esito"].index[sheet["Data Inizio Esito"].size-1]).strftime("%d-%m-%Y")

    #Output document containing all the details mentioned before,
    #format of document name: "Prcp_NameOfDistrict_EarliestDate_LatestDate_past_nDaysBefore_future_nDaysAfter.xlsx"
    sheet.to_excel("./Prcp_"+district+"_"+xlsStartDate+"_"+xlsEndDate+"_past_"+daysBefore+"_future_"+daysAfter+".xlsx", index=False);


if __name__ == '__main__':
    # File location
    loc = os.getcwd()+"\\Geolocation.xlsx"
    if(os.path.isfile(loc)):

        daysBefore = input("Please specify for how many days before the repair you want to fetch data :\n")
        while(not daysBefore.isnumeric()):
            print("Please insert a number\n")
            daysBefore = input("Please specify for how many days before the repair you want to fetch data :\n")

        daysAfter = input("Please specify  for how many days after the repair you want to fetch data :\n")
        while (not daysAfter.isnumeric()):
            print("Please insert a number")
            daysAfter = input("Please specify for how many days after the repair you want to fetch data :\n")

        district = input("Please specify the district :\n").upper()
        WeatherStat(loc,daysBefore,daysAfter,district)

    else:
        print("ERROR: No file named \"Geolocation.xlsx\" on project directory, check if the file is in the project directory")
