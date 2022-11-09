import pandas as pd
import math
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class CoordinatesChecker():

    def __init__(self):

        # Sheet is the excel file that will be modified will be checked and eventually modified
        self.sheet = None
        # Initialising Nominatim API
        self.geolocator = Nominatim(user_agent="CoordCheck")

    def Checker(self, loc):

        """
        Main method of the class, it checks if the coordinates in the excel files are correct and if they are not
        corrects them. A new file NewGeolocation.xlsx will be created in the project folder.

        :param loc: location of the input excel file
        :return:
        """

        if not os.path.exists(loc):
            raise ValueError(f"{loc} is not valid path")

        # Read Excel file and for every row do a check in the ccordinates (i is the row number, row is the actual row)
        self.sheet = pd.read_excel(loc, na_values=['NA'])

        # invert the LAT and LNG column values ( they are wrong from raw data)
        lng = self.sheet["COORD_Y SNAPSHOT GIS (LNG)"]
        self.sheet["COORD_Y SNAPSHOT GIS (LNG)"] = self.sheet["COORD_X SNAPSHOT GIS (LAT)"]
        self.sheet["COORD_X SNAPSHOT GIS (LAT)"] = lng

        for i, row in self.sheet.iterrows():

            if (not math.isnan(row["COORD_X SNAPSHOT GIS (LAT)"]) and not math.isnan(
                    row["COORD_Y SNAPSHOT GIS (LNG)"])):

                # check the coordinates that the Nominatim API gives us with the current address
                geolocation = self.do_reverse(
                    str(row["COORD_X SNAPSHOT GIS (LAT)"]) + "," + str(row["COORD_Y SNAPSHOT GIS (LNG)"]))

                # if the district is not the same as the one the API returns then the script corrects them with util
                if ("city" in geolocation.raw["address"] and row["Comune"].upper() not in geolocation.raw["address"][
                    "city"].upper()):
                    self.util(i, row)
                elif ("town" in geolocation.raw["address"] and row["Comune"].upper() not in geolocation.raw["address"][
                    "town"].upper()):
                    self.util(i, row)
                elif ("village" in geolocation.raw["address"] and row["Comune"].upper() not in
                      geolocation.raw["address"]["village"].upper()):
                    self.util(i, row)

        self.sheet.to_excel("NewGeolocation.xlsx", index=False);

    def util(self, i, row):

        """
        Method used to correct the coordinates by using the do_geocode method and then substituting the newly obtained
        coordinates in the i-th row

        :param i:
        :param row:
        :return:
        """

        comune = str(row["Comune"])
        via = str(row["Indirizzo"])
        civico = str(row["Civico"])

        # if the geocode operations does not fail the substitution occurs in the sheet
        if (newgeo := self.do_geocode(comune + " " + via + " " + civico)) is not None:
            self.sheet.at[i, "COORD_Y SNAPSHOT GIS (LNG)"] = newgeo.longitude
            self.sheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"] = newgeo.latitude
        elif (newgeo := self.do_geocode(comune + " " + via)) is not None:
            self.sheet.at[i, "COORD_Y SNAPSHOT GIS (LNG)"] = newgeo.longitude
            self.sheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"] = newgeo.latitude
        elif (newgeo := self.do_geocode(comune + ", ITALIA")) is not None:
            self.sheet.at[i, "COORD_Y SNAPSHOT GIS (LNG)"] = newgeo.longitude
            self.sheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"] = newgeo.latitude

    def do_geocode(self, address, attempt=1, max_attempts=5):

        """
        Method used to try the geocode operation at most a number of times equal to max_attempts.
        It will return the same object that the geocode method of the Nominatim API returns

        :param address:
        :param attempt:
        :param max_attempts:
        :return:
        """
        try:
            return self.geolocator.geocode(address)
        except GeocoderTimedOut:
            if attempt <= max_attempts:
                return self.do_geocode(address, attempt=attempt + 1)
            raise

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
    loc = input("Please specify location of excel file in input :\n")
    checker = CoordinatesChecker()
    checker.Checker(loc)