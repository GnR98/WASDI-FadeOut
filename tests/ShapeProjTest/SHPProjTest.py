from unittest import TestCase
import os

import fiona

import pandas as pd
import ShapeProjection

class SHPProjTest(TestCase):
        SHP = ShapeProjection.Projection()
        def test_getAllProjections_wrong_excelloc(self):
            excelloc = os.path.abspath("Sheets/Test_shape_Turbigo123.xlsx")
            shapeloc = os.path.abspath("Sheets/Test_shape_EPGS4326.shp")
            self.assertRaises(ValueError, self.SHP.getAllProjections, excelloc, shapeloc, "turbigo")

        def test_getAllProjections_wrong_shapeloc(self):
            excelloc = os.path.abspath("Sheets/Test_shape_Turbigo.xlsx")
            shapeloc = os.path.abspath("Sheets/Test_shape_EPGS326324325.shp")
            self.assertRaises(ValueError, self.SHP.getAllProjections, excelloc, shapeloc, "turbigo")

        def test_getAllProjections_empty_sheet(self):
            excelloc = os.path.abspath("Sheets/Test_shape_Turbigo.xlsx")
            shapeloc = os.path.abspath("Sheets/Test_shape_EPGS4326.shp")
            self.assertRaises(SystemExit, self.SHP.getAllProjections, excelloc, shapeloc, "asdf")

        def test_getAllProjection_turbigo(self):
            excelloc = os.path.abspath("Sheets/Test_shape_Turbigo.xlsx")
            shapeloc = os.path.abspath("Sheets/Test_shape_EPGS4326.shp")
            self.SHP.getAllProjections(excelloc, shapeloc, "TURBIGO")
            projsheet = pd.read_excel(os.path.abspath("NewGeolocation_Test_shape_EPGS4326_TURBIGO.xlsx"))
            ressheet = pd.read_excel(os.path.abspath("Sheets/Test_shape_Turbigo_result.xlsx"))
            for i, row in projsheet.iterrows():
                self.assertEqual(projsheet.at[i, "Proiezione (LAT)"], ressheet.at[i, "Proiezione (LAT)"])
                self.assertEqual(projsheet.at[i, "Proiezione (LNG)"], ressheet.at[i, "Proiezione (LNG)"])

            os.remove(os.path.abspath("NewGeolocation_Test_shape_EPGS4326_TURBIGO.xlsx"))

        def test_projectClosestPipe(self):
            SHP2 = ShapeProjection.Projection()
            excelloc = os.path.abspath("Sheets/Test_shape_Turbigo.xlsx")
            shapeloc = os.path.abspath("Sheets/Test_shape_EPGS4326.shp")
            shape = fiona.open(shapeloc)
            sheet = pd.read_excel(excelloc)
            ressheet = pd.read_excel(os.path.abspath("Sheets/Test_shape_Turbigo_result.xlsx"))
            pipes = []
            for pipe in shape:
                pipes.append(pipe)
            for i, row in sheet.iterrows():
                SHP2.projectOnClosestPipe(pipes, row)
                break
            for j in SHP2.dict:
                self.assertAlmostEqual(SHP2.dict.get(j).x, ressheet.at[0, "Proiezione (LAT)"],10)
                self.assertAlmostEqual(SHP2.dict.get(j).y, ressheet.at[0, "Proiezione (LNG)"],10)
