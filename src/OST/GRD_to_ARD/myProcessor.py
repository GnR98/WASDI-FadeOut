from pathlib import Path
from pprint import pprint
# 10 km buffer around AOI Point
from ost.helpers import vector as vec
import wasdi
import OSTProcess
# we will need this for our time of period definition
from datetime import datetime, timedelta

# this is the s1Project class, that basically handles all the workflow from beginning to the end
from ost import Sentinel1, Sentinel1Scene

def run():
    sBBox = wasdi.getParameter("BBOX")
    sDate = wasdi.getParameter("DATE")
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

    iDaysToSearch = 10

    try:
        iDaysToSearch = int(sSearchDays)
    except Exception as oEx:
        wasdi.wasdiLog(f'Number of days to search not valid due to {repr(oEx)}, assuming 10 [' + str(sSearchDays) + "]")

    # Check the date: assume now
    oEndDay = datetime.today()

    try:
        # Try to convert the one in the params
        oEndDay = datetime.strptime(sDate, '%Y-%m-%d')
    except Exception as oEx:
        # No good: force to yesterday
        wasdi.wasdiLog(f'Date not valid due to {repr(oEx)}, assuming today')

    oTimeDelta = timedelta(days=iDaysToSearch)
    oStartDay = oEndDay - oTimeDelta
    sEndDate = oEndDay.strftime("%Y-%m-%d")
    sStartDate = oStartDay.strftime("%Y-%m-%d")

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
    aoImages = wasdi.searchEOImages("S1", sStartDate, sEndDate, fLatN, fLonW, fLatS, fLonE,"GRD", None, None,
                                    sCloudCoverage, sProvider)

    asAvailableImages = []
    for oImage in aoImages:
        wasdi.wasdiLog("Image Name WITHOUT Extension:" + oImage['title'])
        asAvailableImages.append(oImage['fileName'])

    # STEP 3: Import product on WASDI

    sImportWithDict = wasdi.importProductList(aoImages, sProvider)
    #
    # STEP 4
    # Get again the list of images in the workspace:

    # Check if we have at least one image
    if len(asAvailableImages) <= 0:
        # Nothing found
        wasdi.wasdiLog("No images available, nothing to do.")
        wasdi.updateStatus("DONE", 100)
        return
    asImageTiff = []
    # Take only the Sentinel 1 files
    for sImageToProcess in asAvailableImages:
        sLocalImagePath = wasdi.getPath(sImageToProcess)
        # processing of image with OST
        temp = OSTProcess.process(sImageToProcess)
        asImageTiff.append(temp)
        wasdi.addFileToWASDI(temp)

    wasdi.mosaic(asImageTiff, "mosaicImg.tif")
    SubsetImg=["subset.tif"]
    wasdi.multiSubset(sInputFile="mosaicImg",asOutputFiles=SubsetImg, adLatN=[fLatN], adLonW=[fLonW], adLatS=[fLatS], adLonE=[fLonE],bBigTiff=True)



if __name__ == '__main__':
    wasdi.init("./config.json")
    run()
