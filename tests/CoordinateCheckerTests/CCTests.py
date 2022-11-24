import os
import unittest
from unittest.mock import patch
import CoordinateChecker

class TestCoordinateChecker(unittest.TestCase):

    CC = CoordinateChecker.CoordinatesChecker()

    ############################ TEST do_reverse ############################

    def test_do_reverse_std(self):
        location = "45.46704,8.8958"
        geolocation = self.CC.do_reverse(location)
        expectedres = "Maglificio Mapom, Via Pastrengo, Magenta, Milano, Lombardia, 20013, Italia"
        self.assertEqual(str(geolocation),expectedres, "error")

    def test_do_reverse_single_coor(self):
        location="45.46704"
        self.assertRaises(ValueError, self.CC.do_reverse, location)

    def test_do_reverse_no_coor(self):
        location = ""
        self.assertRaises(ValueError, self.CC.do_reverse, location)

    def test_do_reverse_wrong_lat(self):
        location = "4546.704,8.8958"
        self.assertRaises(ValueError, self.CC.do_reverse, location)

    def test_do_reverse_none_return(self):
        location = "45,46704, 8,8958"
        geolocation = self.CC.do_reverse(location)
        self.assertEqual(geolocation, None, "error")

    def test_do_reverse_timeout(self):
        location = "45.46704,8.8958"
        with patch('geopy.geocoders.Nominatim.reverse') as mock_reverse:
            mock_reverse.side_effect = CoordinateChecker.GeocoderTimedOut
            self.assertRaises(CoordinateChecker.GeocoderTimedOut, self.CC.do_reverse, location)
            self.assertEqual(mock_reverse.call_count,6,"Deve essere chiamata 6 volte")

    def test_do_reverse_4timeout(self):
        location = "45.46704,8.8958"
        expectedres = "Maglificio Mapom, Via Pastrengo, Magenta, Milano, Lombardia, 20013, Italia"
        with patch('geopy.geocoders.Nominatim.reverse') as mock_reverse:
            mock_reverse.side_effect = [
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                unittest.mock.DEFAULT
            ]
            mock_reverse.return_value=expectedres
            self.assertEqual(str(self.CC.do_reverse(location)), expectedres, "error")
            self.assertEqual(mock_reverse.call_count, 5, "Deve essere chiamata 5 volte")

    ############################ TEST do_geocode ############################

    def test_do_geocode_std(self):
        address="MAGENTA,VIA PASTRENGO,33"
        expectedlat=45.46704
        expectedlong= 8.8958
        geo=self.CC.do_geocode(address)
        self.assertAlmostEqual(geo.latitude,  expectedlat,3)
        self.assertAlmostEqual(geo.longitude, expectedlong, 3)

    def test_do_geocode_no_civic(self):
       address = "MAGENTA,VIA PASTRENGO"
       expectedlat = 45.46704
       expectedlong = 8.8958
       geo = self.CC.do_geocode(address)
       self.assertAlmostEqual(geo.latitude, expectedlat, 3)
       self.assertAlmostEqual(geo.longitude, expectedlong, 3)

    def test_do_geocode_no_civic_no_street(self):
       address = "MAGENTA, Italia"
       expectedlat = 45.46704
       expectedlong = 8.8958
       geo = self.CC.do_geocode(address)
       self.assertAlmostEqual(geo.latitude, expectedlat, 1)
       self.assertAlmostEqual(geo.longitude, expectedlong, 1)

    def test_do_geocode_wrong_address(self):
        address = "MAGggENTA,VIA PASTRENGO,33"
        self.assertEqual(self.CC.do_geocode(address), None, "Indirizzo sbagliato deve restituire none")

    def test_do_geocode_no_address(self):
        address = ""
        self.assertEqual(self.CC.do_geocode(address), None, "Indirizzo vuoto deve restituire none")

    def test_do_geocode_timeout(self):
        address = "MAGENTA,VIA PASTRENGO,33"
        with patch('geopy.geocoders.Nominatim.geocode') as mock_geocode:
            mock_geocode.side_effect=CoordinateChecker.GeocoderTimedOut
            self.assertRaises(CoordinateChecker.GeocoderTimedOut, self.CC.do_geocode, address)
            self.assertEqual(mock_geocode.call_count,6,"Deve essere chiamata 6 volte")

    def test_do_geocode_4timeout(self):
        address = "MAGENTA,VIA PASTRENGO,33"
        expectedlat = 45.46704
        expectedlong = 8.8958
        with patch('geopy.geocoders.Nominatim.geocode') as mock_geocode:
            mock_geocode.side_effect = [
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                unittest.mock.DEFAULT
            ]
            mock_geocode.return_value.latitude=expectedlat
            mock_geocode.return_value.longitude = expectedlong
            geo = self.CC.do_geocode(address)
            self.assertAlmostEqual(geo.latitude, expectedlat, 3)
            self.assertAlmostEqual(geo.longitude, expectedlong, 3)
            self.assertEqual(mock_geocode.call_count, 5, "Deve essere chiamata 5 volte")

    ############################ TEST util ############################

    def test_util_full(self):
        loctest = "Sheets/TestSheet_util.xlsx"
        locres = "Sheets/TestSheet_util_result.xlsx"
        testsheet = CoordinateChecker.pd.read_excel(loctest, na_values=['NA'])
        ressheet = CoordinateChecker.pd.read_excel(locres, na_values=['NA'])
        self.CC.sheet=testsheet
        for i, row in self.CC.sheet.iterrows():
            self.CC.util(i, row)
            self.assertAlmostEqual(self.CC.sheet.at[i,"COORD_Y SNAPSHOT GIS (LNG)"],ressheet.at[i,"COORD_Y SNAPSHOT GIS (LNG)"],3)
            self.assertAlmostEqual(self.CC.sheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"],ressheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"],3)

    ############################ TEST checker ############################

    def test_checker(self):
        loctest = "Sheets/TestSheet_checker.xlsx"
        self.CC.Checker(loctest)
        locres = "Sheets/TestSheet_checker_res.xlsx"
        ressheet = CoordinateChecker.pd.read_excel(locres, na_values=['NA'])
        newgeoloc = "NewGeolocation.xlsx"
        newgeosheet = CoordinateChecker.pd.read_excel(newgeoloc, na_values=['NA'])
        for i,row in newgeosheet.iterrows() :
            self.assertEqual(newgeosheet.at[i,"COORD_Y SNAPSHOT GIS (LNG)"], ressheet.at[i,"COORD_Y SNAPSHOT GIS (LNG)"],
                             f"Latitude at line {i} does not match")
            self.assertEqual(newgeosheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"], ressheet.at[i, "COORD_X SNAPSHOT GIS (LAT)"],
                             f"Longitude at line {i} does not match")
        os.remove("NewGeolocation.xlsx")

    def test_checker_null_location (self):
        loc = ""
        self.assertRaises(ValueError,self.CC.Checker,loc)




if __name__ == '__main__':
    unittest.main()
