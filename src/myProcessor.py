import wasdi
from datetime import datetime
from datetime import timedelta
import zipfile
import os
from osgeo import gdal
import numpy

def run():
    # STEP 1: Read "real" parameters
    sBBox = wasdi.getParameter("BBOX")
    # L2
    # sImageType = wasdi.getParameter("IMAGETYPE", "S2MSI2A")
    # Check the Bounding Box: is needed
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


    # Check the cloud coverage
    # sCloudCoverage = None
    # if sMaxCloud is not None:
    #     sCloudCoverage = "[0 TO " + sMaxCloud + "]"
    #     wasdi.wasdiLog("Cloud Coverage " + sCloudCoverage)
    # else:
    #     wasdi.wasdiLog("Cloud Coverage not set")

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

    # STEP 4: From the S2 image create a 8-bit RGB GeoTiff
    # Get again the list of images in the workspace:
    #asAvailableImages = wasdi.getProductsByActiveWorkspace()
    # Check if we have at least one image
    # if len(asAvailableImages) <= 0:
    #     # Nothing found
    #     wasdi.wasdiLog("No images available, nothing to do.")
    #     wasdi.updateStatus("DONE", 100)
    #     return
    # # Take the first image
    # sImageToProcess = asAvailableImages[0]
    # # Get the local path of the image: this is one of the key-feature of WASDI
    # # The system checks if the image is available locally and, if it is not, it will download it
    # sLocalImagePath = wasdi.getPath(sImageToProcess)
    # sStatus = wasdi.executeWorkflow(sImageToProcess,['S1Processed'],"FirstWorkflow")
    # if sStatus == 'DONE':
    #     wasdi.wasdiLog('The product is now in your workspace, look at it on the website')
    #
    # wasdi.wasdiLog('It\'s over!')



def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days

if __name__ == '__main__':
    wasdi.init("./config.json")
    run()