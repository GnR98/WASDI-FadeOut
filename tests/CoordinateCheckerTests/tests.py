import unittest
from unittest.mock import patch
import CoordinateChecker

class TestCoordinateChecker(unittest.TestCase):

    ############################ TEST do_reverse ############################

    def test_do_reverse_std(self):
        location = "45.46704,8.8958"
        geolocation = CoordinateChecker.do_reverse(location)
        expectedres = "Maglificio Mapom, Via Pastrengo, Magenta, Milano, Lombardia, 20013, Italia"
        self.assertEqual(str(geolocation),expectedres, "error")

    def test_do_reverse2_std(self):
        location = "45.46704,8.8958"
        geolocation = CoordinateChecker.do_reverse(location)
        expectedres = CoordinateChecker.geolocator.reverse(location)
        self.assertEqual(geolocation, expectedres, "error")

    def test_do_reverse_single_coor(self):
        location="45.46704"
        self.assertRaises(ValueError,CoordinateChecker.do_reverse,location)

    def test_do_reverse_no_coor(self):
        location = ""
        self.assertRaises(ValueError, CoordinateChecker.do_reverse, location)

    def test_do_reverse_wrong_lat(self):
        location = "4546.704,8.8958"
        self.assertRaises(ValueError, CoordinateChecker.do_reverse, location)

    def test_do_reverse_none_return(self):
        location = "45,46704, 8,8958"
        geolocation = CoordinateChecker.do_reverse(location)
        self.assertEqual(geolocation, None, "error")

    def test_do_reverse_timeout(self):
        location = "45.46704,8.8958"
        with patch('CoordinateChecker.geolocator.reverse') as mock_reverse:
            mock_reverse.side_effect=CoordinateChecker.GeocoderTimedOut
            self.assertRaises(CoordinateChecker.GeocoderTimedOut,CoordinateChecker.do_reverse,location)
            self.assertEqual(mock_reverse.call_count,6,"Deve essere chiamata 6 volte")

    def test_do_reverse_4timeout(self):
        location = "45.46704,8.8958"
        expectedres = "Maglificio Mapom, Via Pastrengo, Magenta, Milano, Lombardia, 20013, Italia"
        with patch('CoordinateChecker.geolocator.reverse') as mock_reverse:
            mock_reverse.side_effect = [
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                unittest.mock.DEFAULT
            ]
            mock_reverse.return_value=expectedres
            self.assertEqual(str(CoordinateChecker.do_reverse(location)), expectedres, "error")
            self.assertEqual(mock_reverse.call_count, 5, "Deve essere chiamata 5 volte")

    ############################ TEST do_geocode ############################

    def test_do_geocode_std(self):
        address="MAGENTA,VIA PASTRENGO,33"
        expectedlat=45.46704
        expectedlong= 8.8958
        geo=CoordinateChecker.do_geocode(address)
        self.assertAlmostEqual(geo.latitude,  expectedlat,3)
        self.assertAlmostEqual(geo.longitude, expectedlong, 3)

    def test_do_geocode_no_civic(self):
       address = "MAGENTA,VIA PASTRENGO"
       expectedlat = 45.46704
       expectedlong = 8.8958
       geo = CoordinateChecker.do_geocode(address)
       self.assertAlmostEqual(geo.latitude, expectedlat, 3)
       self.assertAlmostEqual(geo.longitude, expectedlong, 3)

    def test_do_geocode_wrong_address(self):
        address = "MAGggENTA,VIA PASTRENGO,33"
        self.assertEqual(CoordinateChecker.do_geocode(address),None,"Indirizzo sbagliato deve restituire none")

    def test_do_geocode_no_address(self):
        address = ""
        self.assertEqual(CoordinateChecker.do_geocode(address),None,"Indirizzo vuoto deve restituire none")

    def test_do_geocode_timeout(self):
        address = "MAGENTA,VIA PASTRENGO,33"
        with patch('CoordinateChecker.geolocator.geocode') as mock_geocode:
            mock_geocode.side_effect=CoordinateChecker.GeocoderTimedOut
            self.assertRaises(CoordinateChecker.GeocoderTimedOut,CoordinateChecker.do_geocode,address)
            self.assertEqual(mock_geocode.call_count,6,"Deve essere chiamata 6 volte")

    def test_do_geocode_4timeout(self):
        address = "MAGENTA,VIA PASTRENGO,33"
        expectedlat = 45.46704
        expectedlong = 8.8958
        with patch('CoordinateChecker.geolocator.geocode') as mock_geocode:
            mock_geocode.side_effect = [
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                CoordinateChecker.GeocoderTimedOut,
                unittest.mock.DEFAULT
            ]
            mock_geocode.return_value.latitude=expectedlat
            mock_geocode.return_value.longitude = expectedlong
            geo = CoordinateChecker.do_geocode(address)
            self.assertAlmostEqual(geo.latitude, expectedlat, 3)
            self.assertAlmostEqual(geo.longitude, expectedlong, 3)
            self.assertEqual(mock_geocode.call_count, 5, "Deve essere chiamata 5 volte")

    ############################ TEST util ############################



if __name__ == '__main__':
    unittest.main()