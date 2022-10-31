import math
import os
import unittest
import myProcessor
import wasdi


class GRD_toArd_tests(unittest.TestCase):


    def test_run(self):
        wasdi.init("./config.json")
        myProcessor.run()
        sTestProductName="subset_2021-03-25_45.9-8.7-45.7-8.5.tif"
        wasdi._downloadFile(sTestProductName)
        sTestProductPath=wasdi.getPath(sTestProductName)
        iDimTestproduct=os.path.getsize(sTestProductPath)
        sExpectedProductpath=os.path.abspath("subset_2021-03-25_45.9-8.7-45.7-8.5_exp.tif")
        iExpectedDimProduct=os.path.getsize(sExpectedProductpath)
        iDelta=math.floor(iExpectedDimProduct/10)
        self.assertAlmostEqual(iExpectedDimProduct,iDimTestproduct,None,"The test image has"+str(iDelta)+" bytes more/less than the expected one",iDelta)
        os.remove(sTestProductPath)
        asProducts=wasdi.getProductsByActiveWorkspace()
        for sProduct in asProducts:
            try:
                wasdi.deleteProduct(sProduct)
            except Exception as oEx:
                wasdi.wasdiLog("Error removing " + sProduct + f"due to {repr(oEx)}")


