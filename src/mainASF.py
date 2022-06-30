# these imports we need to handle the folders, independent of the OS
from pathlib import Path
from pprint import pprint
import wasdi
from osgeo import gdal
import numpy
import zipfile
from datetime import datetime
from datetime import timedelta
import os
# this is the Sentinel1Scene class, that basically handles all the workflow from beginning to the end
from ost import Sentinel1Scene

# from ost.helpers.settings import set_log_level
# import logging
# set_log_level(logging.DEBUG)
# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def run():
    # STEP 1: Read "real" parameters
    sBBox = wasdi.getParameter("BBOX")
    if sBBox is None:
        wasdi.wasdiLog("BBOX Parameter not set. Exit")
        wasdi.updateStatus("ERROR", 0)
        return
    sStartDate = wasdi.getParameter("STARTDATE")
    sProvider = wasdi.getParameter("PROVIDER", "AUTO")
    # L1
    #sImageType = wasdi.getParameter("IMAGETYPE", "GRD")
    if(wasdi.getParameter("ENDDATE") is None):
        try:
            sSearchDays = wasdi.getParameter("SEARCHDAYS", "10")
            sEndDate= (datetime.strptime(sStartDate, "%Y-%m-%d") + timedelta(days=int(sSearchDays))).strftime("%Y-%m-%d")
            print(sEndDate)
        except Exception as oEx:
            wasdi.wasdiLog(f'Number of days to search not valid due to {repr(oEx)}, assuming 10 [' + str(sSearchDays) + "]")
    else:
        sEndDate= wasdi.getParameter("ENDDATE", "2020-10-27")
        #Controllo se la data di fine è successiva alla data di inizio
        if (days_between(sStartDate,sEndDate)<0):
            wasdi.wasdiLog("The end date must be after the start date. Exit")
            wasdi.updateStatus("ERROR", 0)
            return
    # Print the date
    wasdi.wasdiLog("Search from " + sStartDate + " to " + sEndDate)
    # Split the bbox: it is in the format: NORTH, WEST, SOUTH, EAST
    asBBox = sBBox.split(",")
    if len(asBBox) != 4:
        wasdi.wasdiLog("BBOX Not valid. Please use LATN,LONW,LATS,LONE")
        wasdi.wasdiLog("BBOX received:" + sBBox)
        wasdi.wasdiLog("exit")
        wasdi.updateStatus("ERROR", 0)
        return
    # Ok is good, print it and convert in float
    wasdi.wasdiLog("Bounding Box: " + sBBox)
    fLatN = float(asBBox[0])
    fLonW = float(asBBox[1])
    fLatS = float(asBBox[2])
    fLonE = float(asBBox[3])

    # STEP 2: Search EO Images
    #"S1", sStartDate, sEndDate, fLatN, fLonW, fLatS, fLonE, sImageType, None, None, sCloudCoverage, sProvider
    aoImages = wasdi.searchEOImages(sPlatform="S1", sDateFrom=sStartDate, sDateTo=sEndDate,
                   fULLat=fLatN, fULLon=fLonW, fLRLat=fLatS, fLRLon=fLonE,
                   sProductType="GRD", iOrbitNumber=None,
                   sSensorOperationalMode=None, sCloudCoverage=None,
                   sProvider=sProvider, oBoundingBox=None, aoParams=None)
    for oImage in aoImages:
        wasdi.wasdiLog("Image Name WITHOUT Extension:" + oImage['title'])

    #STEP 3: Import product on WASDI
    sImportWithDict = wasdi.importAndPreprocess(aoImages,"FirstWorkflow","_proc.tif",sProvider=sProvider)





    # get home folder
    home = Path.home()

    # create a processing directory
    output_dir = home / "OST_Tutorials" / "Tutorial_1"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(str(output_dir))


    # create a S1Scene class instance based on the scene identifier of the first ever Dual-Pol Sentinel-1 IW product

    # ---------------------------------------------------
    # Some scenes to choose from

    # very first IW (VV/VH) S1 image available over Istanbul/Turkey
    # NOTE:only available via ASF data mirror
    scene_id = "S1A_IW_GRDH_1SDV_20220326T053534_20220326T053559_042488_05112D_1F19"


    # create an S1Scene instance
    s1 = Sentinel1Scene(scene_id)

    # print summarising infos about the scene
    s1.info()

    s1.download(output_dir)

    # Default ARD parameter

    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("Our ARD parameters dictionary contains 4 keys. For the moment, only single_ARD is relevant.")
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    pprint(s1.ard_parameters.keys())
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("")

    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("Dictionary of our default OST ARD parameters for single scene processing:")
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    pprint(s1.ard_parameters["single_ARD"])
    print(
        "----------------------------------------------------------------------------------------------------------"
    )
    print("")

    # Default ARD parameter

    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("Our ARD parameters dictionary contains 4 keys. For the moment, only single_ARD is relevant.")
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    pprint(s1.ard_parameters.keys())
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("")

    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("Dictionary of our default OST ARD parameters for single scene processing:")
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    pprint(s1.ard_parameters["single_ARD"])
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("")

    # Customised ARD parameters

    # we cusomize the resolution and image resampling
    s1.ard_parameters["single_ARD"]["resolution"] = 100  # set output resolution to 100m
    s1.ard_parameters["single_ARD"]["remove_speckle"] = False  # apply a speckle filter
    s1.ard_parameters["single_ARD"]["dem"][
        "image_resampling"
    ] = "BILINEAR_INTERPOLATION"  # BICUBIC_INTERPOLATION is default

    # s1.ard_parameters['single_ARD']['product_type'] = 'RTC-gamma0'

    # uncomment this for the Azores EW scene
    # s1.ard_parameters['single_ARD']['dem']['dem_name'] = 'GETASSE30'
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("Dictionary of our customised ARD parameters for the final scene processing:")
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    pprint(s1.ard_parameters["single_ARD"])
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )

    s1.create_ard(infile="C:\\Users\\gnisc\\OST_Tutorials\\Tutorial_1\\SAR\GRD\\2022\\03\\26\\S1A_IW_GRDH_1SDV_20220326T053534_20220326T053559_042488_05112D_1F19.zip", out_dir=output_dir, overwrite=True)

    print(" The path to our newly created ARD product can be obtained the following way:")
    s1.ard_dimap

    s1.create_rgb(outfile=output_dir / f"{s1.start_date}.tif")

    print(" The path to our newly created RGB product can be obtained the following way:")
    s1.ard_rgb

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days

if __name__ == '__main__':
    wasdi.init("./config.json")
    run()
