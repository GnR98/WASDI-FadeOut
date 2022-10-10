import os
from pathlib import Path
from pprint import pprint
# 10 km buffer around AOI Point
import wasdi
# we will need this for our time of period definition
from datetime import datetime, timedelta


def run():
    #Get parameters from parameters.json
    sBBox = wasdi.getParameter("BBOX")
    sStartDate = wasdi.getParameter("STARTDATE",)
    oStartDay = datetime.strptime(sStartDate,'%Y-%m-%d')
    sMaxCloud = wasdi.getParameter("MAXCLOUD", "20")
    sSearchDays = wasdi.getParameter("SEARCHDAYS", "10")
    sProvider = wasdi.getParameter("PROVIDER", "ONDA")

    # Check the Bounding Box: is needed
    if sBBox is None:
        wasdi.wasdiLog("BBOX Parameter not set. Exit")
        wasdi.updateStatus("ERROR", 0)
        return

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
    sCloudCoverage = None

    if sMaxCloud is not None:
        sCloudCoverage = "[0 TO " + sMaxCloud + "]"
        wasdi.wasdiLog("Cloud Coverage " + sCloudCoverage)
    else:
        wasdi.wasdiLog("Cloud Coverage not set")

    # STEP 2: Search EO Images
    aoImages = wasdi.searchEOImages("S1", sStartDate, sEndDate, fLatN, fLonW, fLatS, fLonE, "GRD", None, None,
                                    sCloudCoverage, sProvider)

    asAvailableImages = []
    for oImage in aoImages:
        wasdi.wasdiLog("Image Name WITHOUT Extension:" + oImage['title'])
        asAvailableImages.append(oImage['fileName'])

    # STEP 3: Import product on WASDI and process it with the first workflow

    wasdi.importAndPreprocess(aoImages, "GRD_to_ARD1", "_temp_ard.tif")

    # STEP 4
    # Get again the list of images in the workspace:

    # Check if we have at least one image
    if len(asAvailableImages) <= 0:
        # Nothing found
        wasdi.wasdiLog("No images available, nothing to do.")
        wasdi.updateStatus("DONE", 100)
        return

    # Take only the already processed files
    asSemiProcessedImages = wasdi.getProductsByActiveWorkspace()
    for i in asSemiProcessedImages:
        if ("_temp_ard" not in i or ".zip" in i):
            asSemiProcessedImages.remove(i)

    #Process the images again with the second workflow and save the names in an array
    asMosaicImages = []
    for i in asSemiProcessedImages:
        if ("_temp_ard" in i):
            wasdi.executeWorkflow([i], [i.replace("_temp_ard", "_ard")], "GRD_to_ARD2")
            asMosaicImages.append(i.replace("_temp_ard", "_ard"))
            wasdi.deleteProduct(i)

    #Use the new array as input to create a mosaic
    # for i in range(0, len(asMosaicImages)):
    #     if asMosaicImages[i].endswith(".dim"):
    #          asMosaicImages[i] = asMosaicImages[i][:-len(".dim")]
    #     if (".zip" in asMosaicImages[i]):
    #         asMosaicImages.remove(asMosaicImages[i])
    sMosaicImgName = "mosaicImg_"+sStartDate+"_"+asBBox[0]+"-"+asBBox[1]+"-"+asBBox[2]+"-"+asBBox[3]+".tif"
    wasdi.mosaic(asMosaicImages, sMosaicImgName)

    #Create a subset of the newly obtained mosaic
    SubsetImg = ["subset_"+sStartDate+"_"+asBBox[0]+"-"+asBBox[1]+"-"+asBBox[2]+"-"+asBBox[3]+".tif"]
    wasdi.multiSubset(sInputFile=sMosaicImgName, asOutputFiles=SubsetImg, adLatN=[fLatN], adLonW=[fLonW],
                      adLatS=[fLatS], adLonE=[fLonE], bBigTiff=True)

    #(Optional) Delete the ARD products
    bDeleteArd = True
    if (bDeleteArd):
        for sARDimage in asMosaicImages:
            try:
                wasdi.deleteProduct(sARDimage)
            except:
                wasdi.wasdiLog("Error removing " + sARDimage)


if __name__ == '__main__':
    wasdi.init("./config.json")
    run()
