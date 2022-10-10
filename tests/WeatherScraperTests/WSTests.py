import os
import unittest
import WeatherScraper

class WeatherScraperTest(unittest.TestCase):

    def test_WeatherStat_Turbigo(self):
        loctest="Sheets/TestSheet_WeatherStat.xlsx"
        locres="Sheets/TestSheet_WeatherStat_res_turbigo.xlsx"
        WeatherScraper.WeatherStat(os.path.abspath(loctest),1,1,"TURBIGO")

        ressheet = WeatherScraper.pd.read_excel(os.path.abspath(locres), na_values=['NA'])
        weathersheet = WeatherScraper.pd.read_excel("Prcp_TURBIGO_30-11-2012_11-01-2013_past_1_future_1.xlsx", na_values=['NA'])

        for i,row in weathersheet.iterrows():
            self.assertEqual(
                weathersheet.at[i,"Precipitations (in mm), from 1 days before (in ascending order of date)"],
                ressheet.at[i,"Precipitations (in mm), from 1 days before (in ascending order of date)"])
            self.assertEqual(
                weathersheet.at[i, "Precipitations (in mm), until 1 days after (in ascending order of date)"],
                ressheet.at[i, "Precipitations (in mm), until 1 days after (in ascending order of date)"])
            self.assertEqual(
                str(weathersheet.at[i, "Mean precipitation value in the 1 days before the repair date (in mm)"]),
                str(ressheet.at[i, "Mean precipitation value in the 1 days before the repair date (in mm)"]))
            self.assertEqual(
                str(weathersheet.at[i, "Mean precipitation value in the 1 days after the repair date (in mm)"]),
                str(ressheet.at[i, "Mean precipitation value in the 1 days after the repair date (in mm)"]))
            self.assertEqual(
                str(weathersheet.at[i, "Did it rain before the repair date ?"]),
                str(ressheet.at[i, "Did it rain before the repair date ?"]))
            self.assertEqual(
                str(weathersheet.at[i, "Did it rain after the repair date ?"]),
                str(ressheet.at[i, "Did it rain after the repair date ?"]))

        os.remove(os.path.abspath("Prcp_TURBIGO_30-11-2012_11-01-2013_past_1_future_1.xlsx"))

    def test_WeatherStat_Magenta(self):
        loctest="Sheets/TestSheet_WeatherStat.xlsx"
        locres="Sheets/TestSheet_WeatherStat_res_magenta.xlsx"
        WeatherScraper.WeatherStat(os.path.abspath(loctest),1,1,"MAGENTA")

        ressheet = WeatherScraper.pd.read_excel(os.path.abspath(locres), na_values=['NA'])
        weathersheet = WeatherScraper.pd.read_excel("Prcp_MAGENTA_05-06-2017_27-09-2017_past_1_future_1.xlsx", na_values=['NA'])

        for i,row in weathersheet.iterrows():
            self.assertEqual(
                weathersheet.at[i,"Precipitations (in mm), from 1 days before (in ascending order of date)"],
                ressheet.at[i,"Precipitations (in mm), from 1 days before (in ascending order of date)"])
            self.assertEqual(
                weathersheet.at[i, "Precipitations (in mm), until 1 days after (in ascending order of date)"],
                ressheet.at[i, "Precipitations (in mm), until 1 days after (in ascending order of date)"])
            self.assertEqual(
                str(weathersheet.at[i, "Mean precipitation value in the 1 days before the repair date (in mm)"]),
                str(ressheet.at[i, "Mean precipitation value in the 1 days before the repair date (in mm)"]))
            self.assertEqual(
                str(weathersheet.at[i, "Mean precipitation value in the 1 days after the repair date (in mm)"]),
                str(ressheet.at[i, "Mean precipitation value in the 1 days after the repair date (in mm)"]))
            self.assertEqual(
                str(weathersheet.at[i, "Did it rain before the repair date ?"]),
                str(ressheet.at[i, "Did it rain before the repair date ?"]))
            self.assertEqual(
                str(weathersheet.at[i, "Did it rain after the repair date ?"]),
                str(ressheet.at[i, "Did it rain after the repair date ?"]))

        os.remove(os.path.abspath("Prcp_MAGENTA_05-06-2017_27-09-2017_past_1_future_1.xlsx"))

    def test_WeatherStat_Cassina(self):
        loctest="Sheets/TestSheet_WeatherStat.xlsx"
        locres="Sheets/TestSheet_WeatherStat_res_cassina.xlsx"
        WeatherScraper.WeatherStat(os.path.abspath(loctest),1,1,"CASSINA DE' PECCHI")

        ressheet = WeatherScraper.pd.read_excel(os.path.abspath(locres), na_values=['NA'])
        weathersheet = WeatherScraper.pd.read_excel("Prcp_CASSINA DE' PECCHI_22-07-2015_20-02-2021_past_1_future_1.xlsx", na_values=['NA'])

        for i,row in weathersheet.iterrows():
            self.assertEqual(
                weathersheet.at[i,"Precipitations (in mm), from 1 days before (in ascending order of date)"],
                ressheet.at[i,"Precipitations (in mm), from 1 days before (in ascending order of date)"])
            self.assertEqual(
                weathersheet.at[i, "Precipitations (in mm), until 1 days after (in ascending order of date)"],
                ressheet.at[i, "Precipitations (in mm), until 1 days after (in ascending order of date)"])
            self.assertEqual(
                str(weathersheet.at[i, "Mean precipitation value in the 1 days before the repair date (in mm)"]),
                str(ressheet.at[i, "Mean precipitation value in the 1 days before the repair date (in mm)"]))
            self.assertEqual(
                str(weathersheet.at[i, "Mean precipitation value in the 1 days after the repair date (in mm)"]),
                str(ressheet.at[i, "Mean precipitation value in the 1 days after the repair date (in mm)"]))
            self.assertEqual(
                str(weathersheet.at[i, "Did it rain before the repair date ?"]),
                str(ressheet.at[i, "Did it rain before the repair date ?"]))
            self.assertEqual(
                str(weathersheet.at[i, "Did it rain after the repair date ?"]),
                str(ressheet.at[i, "Did it rain after the repair date ?"]))

        os.remove(os.path.abspath("Prcp_CASSINA DE' PECCHI_22-07-2015_20-02-2021_past_1_future_1.xlsx"))

    def test_WeatherStat_null_loc(self):
        loctest = ""
        self.assertRaises(ValueError,WeatherScraper.WeatherStat,loctest, 1, 1, "TURBIGO")

    def test_WeatherStat_file_not_found(self):
        loctest = "WeatherScraperTests/Sheets/aTestSheet_WeatherStat.xlsx"
        self.assertRaises(ValueError, WeatherScraper.WeatherStat,os.path.abspath(loctest), 1, 1, "TURBIGO")

    def test_WeatherStat_invalid_days(self):
        loctest = "Sheets/TestSheet_WeatherStat.xlsx"
        self.assertRaises(ValueError, WeatherScraper.WeatherStat,os.path.abspath(loctest), "", 1, "TURBIGO")

    def test_WeatherStat_empty_filtered_sheet(self):
        loctest = "Sheets/TestSheet_WeatherStat.xlsx"
        self.assertRaises(SystemExit, WeatherScraper.WeatherStat,os.path.abspath(loctest), 1, 1, "Tasdfsa")


