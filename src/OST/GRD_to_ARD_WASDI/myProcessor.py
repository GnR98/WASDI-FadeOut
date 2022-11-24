import os
from pathlib import Path
from pprint import pprint
# 10 km buffer around AOI Point
import numpy as np
import wasdi
# we will need this for our time of period definition
from datetime import datetime, timedelta


def run():
    #Get parameters from parameters.json
    oBBox = wasdi.getParameter("BBOX")
    sStartDate = wasdi.getParameter("STARTDATE",)
    oStartDay = datetime.strptime(sStartDate,'%Y-%m-%d')
    sMaxCloud = str((wasdi.getParameter("MAXCLOUD", 20)))
    sSearchDays = wasdi.getParameter("SEARCHDAYS", "10")
    sProvider = wasdi.getParameter("PROVIDER", "ONDA")
    bDeleteArd = wasdi.getParameter("DELETE ARD", "")

    # Check the Bounding Box: is needed
    if oBBox is None:
        wasdi.wasdiLog("BBOX Parameter not set. Exit")
        wasdi.updateStatus("ERROR", 0)
        return

    # Split the bbox: it is in the format: NORTH, WEST, SOUTH, EAST
    try :
        fLatN = float(oBBox["northEast"]["lat"])
        fLonE = float(oBBox["northEast"]["lng"])
        fLatS = float(oBBox["southWest"]["lat"])
        fLonW = float(oBBox["southWest"]["lng"])
    except Exception as oEx:
        wasdi.wasdiLog(f"BBOX Not valid. due to {repr(oEx)} Please use LATN,LONE,LATS,LONW")
        wasdi.wasdiLog("exit")
        wasdi.updateStatus("ERROR", 0)
        return


    #Getting the number of days to search so that EndDate may be calculated
    iDaysToSearch = 10

    try:
        iDaysToSearch = int(sSearchDays)
    except Exception as oEx:
        wasdi.wasdiLog(f'Number of days to search not valid due to {repr(oEx)}, assuming 10 [' + str(sSearchDays) + "]")

    #Computing the EndDate (the string version is needed for the search algorithm)
    oTimeDelta = timedelta(days=iDaysToSearch)
    oEndDay = oStartDay + oTimeDelta
    if oEndDay - datetime.today() > timedelta(days=0):
        wasdi.wasdiLog(f'Date not valid, assuming today')
        oEndDay=datetime.today()
    sEndDate = oEndDay.strftime("%Y-%m-%d")

    # Print the date
    wasdi.wasdiLog("Search from " + sStartDate + " to " + sEndDate)

    # Check the cloud coverage

    # STEP 2: Search EO Images
    aoImages = wasdi.searchEOImages("S1", sStartDate, sEndDate, fLatN, fLonW, fLatS, fLonE, "GRD", None, None,
                                     sProvider)

    asAvailableImages = []
    for oImage in aoImages:
        wasdi.wasdiLog("Image Name WITHOUT Extension:" + oImage['title'])
        asAvailableImages.append(oImage['fileName'])

    aoImagestoimport=[]

    asProductsinWorkspace=wasdi.getProductsByActiveWorkspace()
    for sImage in asAvailableImages:
        if sImage.replace(".zip","_ard.tif") not in asProductsinWorkspace:
            aoImagestoimport.append([oImage for oImage in aoImages if oImage["fileName"]==sImage][0])

    # STEP 3: Import product on WASDI and process it with the first workflow

    wasdi.importAndPreprocess(aoImagestoimport, "GRD_to_ARD1", "_temp_ard.tif")

    # STEP 4
    # Get again the list of images in the workspace:

    # Check if we have at least one image
    if len(asAvailableImages) <= 0:
        # Nothing found
        wasdi.wasdiLog("No images available, nothing to do.")
        wasdi.updateStatus("DONE", 100)
        return

    # Take only the already processed files
    asSemiProcessedImages = [oImage["fileName"].replace(".zip","_temp_ard.tif") for oImage in aoImagestoimport]

    #Process the images again with the second workflow and save the names in an array
    asMosaicImages = []
    for sSemiProcessedImage in asSemiProcessedImages:
        #if ("_temp_ard" in sSemiProcessedImage):
            wasdi.executeWorkflow([sSemiProcessedImage], [sSemiProcessedImage.replace("_temp_ard", "_ard")], "GRD_to_ARD2")

    asProductsinWorkspace = wasdi.getProductsByActiveWorkspace()
    for oImage in aoImages:
        sFile=oImage["fileName"].replace(".zip","_ard.tif")
        if sFile in asProductsinWorkspace:
            asMosaicImages.append(sFile)

    #Use the new array as input to create a mosaic
    sMosaicImgName = "mosaicImg_"+sStartDate+"_"+str(fLatN)+"-"+str(fLonE)+"-"+str(fLatS)+"-"+str(fLonW)+".vrt"
    wasdi.mosaic(asMosaicImages, sMosaicImgName,iNoDataValue=-1,iIgnoreInputValue=0)

    #Create a subset of the newly obtained mosaic
    SubsetImg = ["subset_"+sStartDate+"_"+str(fLatN)+"-"+str(fLonE)+"-"+str(fLatS)+"-"+str(fLonW)+".tif"]
    wasdi.multiSubset(sInputFile=sMosaicImgName, asOutputFiles=SubsetImg, adLatN=[fLatN], adLonW=[fLonW],
                      adLatS=[fLatS], adLonE=[fLonE], bBigTiff=True)
    #wasdi._downloadFile("subset_"+sStartDate+"_"+str(fLatN)+"-"+str(fLonE)+"-"+str(fLatS)+"-"+str(fLonW)+".tif")

    #(Optional) Delete the ARD products

    if (bDeleteArd):
        for oImage in aoImages:
            sTempARDImage = oImage["fileName"].replace(".zip", "_temp_ard.tif")
            sARDimage = oImage["fileName"].replace(".zip", "_ard.tif")
            try:
                wasdi.deleteProduct(sTempARDImage)
            except Exception as oEx:
                wasdi.wasdiLog("Error removing " + sTempARDImage + f"due to {repr(oEx)}")
            try:
                wasdi.deleteProduct(sARDimage)
            except Exception as oEx:
                wasdi.wasdiLog("Error removing " +sARDimage+ f"due to {repr(oEx)}")


if __name__ == '__main__':
    wasdi.init("./config.json")
    run()