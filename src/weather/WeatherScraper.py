import numpy as np
import pandas as pd
from datetime import datetime
from meteostat import Point, Daily
from datetime import timedelta
import math
from collections import OrderedDict

def run():
    # File location
    loc = ("C:\\Users\\gnisc\\AppData\\Local\\Programs\\Python\\Python310\\weather\\Geolocation.xlsx")

    # Read only the column relative to: Comune, Inizio lavori, Coordinate
    wb = pd.read_excel(loc, na_values=['NA'], usecols="B,F,I,J")
    # Filter only Turbigo
    sheet=wb.query("Comune == 'TURBIGO' or Comune == 'TURBIGO ()' or Comune == 'TURBIGO (20029)'")

    # New column used to insert the detail of preciptation on each day of the 15 days before the start work
    sheet["Dettaglio 15 giorni prima"]=" "
    sheet["Dettaglio 15 giorni dopo"]=" "

    # For each date in the excel, put the mean value of the precipitation
    # calculated on 15 days before the start work, on 'YourDataInAList'
    # and put on Data the detail of preciptation on each day
    # of the 15 days before the start work
    YourDataInAList1=[]
    Data1=[]
    YourDataInAList2 = []
    Data2 = []
    for i, row in sheet.iterrows():
        print(row)
        start1 = row[1] - timedelta(days=15)
        start2 = row[1]

        location = Point(row[3], row[2])
        end1 = row[1]
        end2 = row[1] + timedelta(days=15)


        data1 = Daily(location, start1, end1)
        data2 = Daily(location, start2, end2)
        data1 = data1.fetch()
        data2 = data2.fetch()
        #15 giorni prima
        if(data1.prcp.size!=0):
            tot = 0
            #Mean value of precipitation in the 15 days before the start work
            for q in data1.prcp:
                Data1.append(q)
                if not math.isnan(q):
                    tot += q
            tot = tot / data1.prcp.size
            YourDataInAList1.append(tot)
            print(data1.prcp[1])
        else:
            YourDataInAList1.append(np.NAN)
        #15 giorni dopo
        if (data2.prcp.size != 0):
            tot = 0
            # Mean value of precipitation in the 15 days after the start work
            for q in data2.prcp:
                Data2.append(q)
                if not math.isnan(q):
                    tot += q
            tot = tot / data2.prcp.size
            YourDataInAList2.append(tot)
            print(data2.prcp[1])
        else:
            YourDataInAList2.append(np.NAN)

        sheet.at[i,"Dettaglio 15 giorni prima (in ordine crescente di data)"]=Data1.copy()
        sheet.at[i,"Dettaglio 15 giorni dopo (in ordine crescente di data)"]=Data2.copy()

        Data1.clear()
        Data2.clear()

    sheet.insert(4,"Media precipitazioni nei 15 giorni prima dalla data di inizio(in mm)",value=YourDataInAList1)
    sheet.insert(5,"Media precipitazioni nei 15 giorni dopo la data di inizio(in mm)",value=YourDataInAList2)

    sheet.to_excel("./YourNewExcel.xlsx", index=False);


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

