import pandas as pd
from meteostat import Point, Daily
from datetime import timedelta
import math
import os
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class WeatherScraper():

    def __init__(self):
        self.sheet=None
        self.geolocator = Nominatim(user_agent="CoordCheck")

    def WeatherStat(self,loc, daysBefore, daysAfter, district):

        """
        Function used to fetch data about precipitations in a set of given places and dates. The method filters the
        excel file keeping only the rows that have in the "Comune" column the "district" value , then for each of them reads
        the reparation date and fecthes the precipitation data for every day between (reparation date-daysBefore) and
        (reparation date+daysAfter). The collected data is then organized in columns; more columns are added for the mean value
        for the past and future days, a boolean variable that tells whether it has rained or not before or after the reparation date,
        and the type of place (city,town,village). A new excel file will be created with all the relevant columns
        (excess ones are cut)


        :param loc: location of the input excel file
        :param daysBefore: number of days to search before the repair date
        :param daysAfter: number of days to search after the repair date
        :param district: name of the district (e.g. Turbigo)
        :return:
        """
        #Check inputs
        if not os.path.exists(loc):
            raise ValueError(f"{loc} is not valid path")



        # Read only the column relative to: Comune, Inizio lavori, Coordinate
        wb = pd.read_excel(loc, na_values=['NA'], usecols="B,F,I,J")

        # Filter the chosen district
        district=district.upper()
        self.sheet = wb[wb['Comune'].str.contains(district)]
        if (self.sheet.empty):
            raise SystemExit("There is no data from the input file for the district of " + district)

        # New columns used to insert the details of precipitations on each requested date before and after the repair date
        self.sheet["Precipitations (in mm), from " + str(daysBefore) + " days before (in ascending order of date)"] = " "
        self.sheet["Precipitations (in mm), until " + str(daysAfter) + " days after (in ascending order of date)"] = " "

        # For each date in the excel, put the mean value of the precipitation
        # calculated on the days before('yourDataInAList1') and after('YourDataInaAList2') the repair date
        # and put on prcp1 and prcp2 the details of preciptations of each day (same convention as prior comment)
        yourDataInAList1 = []
        prcp1 = []
        yourDataInAList2 = []
        prcp2 = []

        # For each row the column cityVillageTown is used to store a value that determines if the given coordinates belong to a city, a town or a village
        # The locNames column contains the name of the city, town or village
        locNames = []
        cityVillageTown = []

        for i, row in self.sheet.iterrows():
            # print(row)
            # print("\n")
            start1 = row["Data Inizio Esito"] - timedelta(days=int(daysBefore))
            start2 = row["Data Inizio Esito"]

            location = Point(row["COORD_X SNAPSHOT GIS (LAT)"], row["COORD_Y SNAPSHOT GIS (LNG)"])
            end1 = row["Data Inizio Esito"]
            end2 = row["Data Inizio Esito"] + timedelta(days=int(daysAfter))

            # If the coordinates are not NAN the geolocaation process starts then, depending on the result, the columns
            # cityVillageTown and locNames are filled with the correct values
            if (not math.isnan(row["COORD_Y SNAPSHOT GIS (LNG)"]) and not math.isnan(row["COORD_X SNAPSHOT GIS (LAT)"])):
                geolocation = self.do_reverse(str(row["COORD_X SNAPSHOT GIS (LAT)"]) + "," + str(row["COORD_Y SNAPSHOT GIS (LNG)"]))
                if ("city" in geolocation.raw["address"]):
                    cityVillageTown.append("city")
                    locNames.append(geolocation.raw["address"]["city"])
                elif ("town" in geolocation.raw["address"]):
                    cityVillageTown.append("town")
                    locNames.append(geolocation.raw["address"]["town"])
                elif ("village" in geolocation.raw["address"]):
                    cityVillageTown.append("village")
                    locNames.append(geolocation.raw["address"]["village"])
            else:
                locNames.append("nan")
                cityVillageTown.append("nan")

            # Using meteostat API
            data1 = Daily(location, start1, end1)
            data2 = Daily(location, start2, end2)
            data1 = data1.fetch()
            data2 = data2.fetch()

            # counter used to have the exact number of valid values
            count = data1.prcp.size

            if (data1.prcp.size != 0):
                tot = 0
                # Mean value of precipitation on the days before the repair date
                for q in data1.prcp:
                    prcp1.append(q)
                    if not math.isnan(q):
                        tot += q
                    else:
                        count = count - 1
                if count == 0:
                    # We don't have valid values
                    tot = "nan"
                else:
                    tot = tot / count
                yourDataInAList1.append(tot)
            else:
                tot = "nan"
                yourDataInAList1.append("nan")

            # Column used to store if there were or not any precipitations before the repair date
            # the row values for this column are determined from the mean value
            match tot:
                case 0.0:
                    self.sheet.at[i, "Did it rain before the repair date ?"] = "false"
                case "nan":
                    self.sheet.at[i, "Did it rain before the repair date ?"] = "nan"
                case _:
                    self.sheet.at[i, "Did it rain before the repair date ?"] = "true"

            count = data2.prcp.size

            if (data2.prcp.size != 0):
                tot = 0
                # Mean value of precipitation on the days after the repair date
                for q in data2.prcp:
                    prcp2.append(q)
                    if not math.isnan(q):
                        tot += q
                    else:
                        count = count - 1
                if count == 0:
                    # We don't have valid values
                    tot = "nan"
                else:
                    tot = tot / count
                yourDataInAList2.append(tot)
            else:
                tot = "nan"
                yourDataInAList2.append("nan")

            # Column used to store if there were or not any precipitations after the repair date
            # the row values for this column are determined from the mean value
            match tot:
                case 0.0:
                    self.sheet.at[i, "Did it rain after the repair date ?"] = "false"
                case "nan":
                    self.sheet.at[i, "Did it rain after the repair date ?"] = "nan"
                case _:
                    self.sheet.at[i, "Did it rain after the repair date ?"] = "true"

            # Insertion of detailed values of precipitation (in mm)
            self.sheet.at[
                i, "Precipitations (in mm), from " + str(daysBefore) + " days before (in ascending order of date)"] = prcp1.copy()
            self.sheet.at[
                i, "Precipitations (in mm), until " + str(daysAfter) + " days after (in ascending order of date)"] = prcp2.copy()

            prcp1.clear()
            prcp2.clear()

        # Columns used to store the mean values
        self.sheet.insert(6, "Mean precipitation value in the " + str(daysBefore) + " days before the repair date (in mm)",
                     value=yourDataInAList1)
        self.sheet.insert(7, "Mean precipitation value in the " + str(daysAfter) + " days after the repair date (in mm)",
                     value=yourDataInAList2)
        self.sheet.insert(8, "Type of location", value=cityVillageTown)
        self.sheet.insert(9, "Name of location", value=locNames)

        # Earliest date of observation
        xlsStartDate = self.sheet["Data Inizio Esito"].get(self.sheet["Data Inizio Esito"].index[0]).strftime("%d-%m-%Y")

        # Latest date of observation
        xlsEndDate = self.sheet["Data Inizio Esito"].get(
            self.sheet["Data Inizio Esito"].index[self.sheet["Data Inizio Esito"].size - 1]).strftime("%d-%m-%Y")

        # Output document containing all the details mentioned before,
        # format of document name: "Prcp_NameOfDistrict_EarliestDate_LatestDate_past_nDaysBefore_future_nDaysAfter.xlsx"
        self.sheet.to_excel(
            "./Prcp_" + district + "_" + xlsStartDate + "_" + xlsEndDate + "_past_" + str(daysBefore) + "_future_" + str(daysAfter) + ".xlsx",
            index=False)

    def do_reverse(self, coordinate, attempt=1, max_attempts=5):

        """
        Method used to try the reverse geocoding operation at most a number of times equal to max_attempts.
        It will return the same object that the reverse method of the Nominatim API returns

        :param self:
        :param coordinate:
        :param attempt:
        :param max_attempts:
        :return:
        """
        try:
            return self.geolocator.reverse(coordinate)
        except GeocoderTimedOut:
            if attempt <= max_attempts:
                return self.do_reverse(coordinate, attempt=attempt + 1)
            raise


if __name__ == '__main__':
    # JSON File location
    file = open("config.json")
    jsonData = json.load(file)

    daysBefore = ""
    daysAfter = ""
    district = ""
    loc = ""

    # if a key does not exists or the value of the key is not given (causing variable == ""), a console input will be requested
    # in order to fill the required variable
    if ("DAYSBEFORE" in jsonData.keys()):
        daysBefore = jsonData.get("DAYSBEFORE")
    if (daysBefore == ""):
        daysBefore = input("Please specify for how many days before the repair you want to fetch data :\n")
        while (not daysBefore.isnumeric()):
            print("Please insert a number\n")
            daysBefore = input("Please specify for how many days before the repair you want to fetch data :\n")

    if ("DAYSAFTER" in jsonData.keys()):
        daysAfter = jsonData.get("DAYSAFTER")
    if (daysAfter == ""):
        daysAfter = input("Please specify  for how many days after the repair you want to fetch data :\n")
        while (not daysAfter.isnumeric()):
            print("Please insert a number")
            daysAfter = str(input("Please specify for how many days after the repair you want to fetch data :\n"))

    if ("DISTRICT" in jsonData.keys()):
        district = jsonData.get("DISTRICT").upper()
    if (district == ""):
        district = input("Please specify the district :\n").upper()

    if ("EXCELLOC" in jsonData.keys()):
        loc = jsonData.get("EXCELLOC")
    if (loc == ""):
        loc = input("Please specify location of excel file in input :\n")

    # When every required variable is filled the script checks whether the source excle file exists before calling the function
    if (os.path.isfile(loc)):
        WeatherScraper = WeatherScraper()
        WeatherScraper.WeatherStat(loc, str(daysBefore), str(daysAfter), district)
    else:
        print("ERROR: Excel source file not found")
