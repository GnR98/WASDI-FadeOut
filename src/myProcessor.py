import wasdi
from datetime import datetime
from datetime import timedelta
import zipfile
import os
from osgeo import gdal
import numpy
from ost import Sentinel1Scene

def run():
    # STEP 1: Read "real" parameters
    sBBox = wasdi.getParameter("BBOX")
    sWorkflow= wasdi.getParameter("WORKFLOW","LISTSinglePreproc")
    if sWorkflow is None:
        wasdi.wasdiLog("Workflow not set. Exit")
        wasdi.updateStatus("ERROR", 0)
        return
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



    # # STEP 2: Search EO Images
    # #"S1", sStartDate, sEndDate, fLatN, fLonW, fLatS, fLonE, sImageType, None, None, sCloudCoverage, sProvider
    # aoImages = wasdi.searchEOImages(sPlatform="S1", sDateFrom=sStartDate, sDateTo=sEndDate,
    #                fULLat=fLatN, fULLon=fLonW, fLRLat=fLatS, fLRLon=fLonE,
    #                sProductType="GRD", iOrbitNumber=None,
    #                sSensorOperationalMode=None, sCloudCoverage=None,
    #                sProvider=sProvider, oBoundingBox=None, aoParams=None)
    # for oImage in aoImages:
    #     wasdi.wasdiLog("Image Name WITHOUT Extension:" + oImage['title'])
    #
    # #STEP 3: Import product on WASDI
    #
    # sImportWithDict = wasdi.importAndPreprocess(aoImages,sWorkflow,"_proc.tif",sProvider=sProvider)



    # STEP 4
    # Get again the list of images in the workspace:
    asAvailableImages = wasdi.getProductsByActiveWorkspace()
    # Check if we have at least one image
    if len(asAvailableImages) <= 0:
         # Nothing found
        wasdi.wasdiLog("No images available, nothing to do.")
        wasdi.updateStatus("DONE", 100)
        return
    # # Take only the Sentinel 1 files
    asImagesToExtract=[]
    for i in asAvailableImages:
        if "_proc.tif" in i and ("S1A" in i or "S1B" in i):
            asImagesToExtract.append(i)



     # Get the local path of the image: this is one of the key-feature of WASDI
     # The system checks if the image is available locally and, if it is not, it will download it
    for sImageToExtract in asImagesToExtract:
        sLocalImagePath = wasdi.getPath(sImageToExtract)
        sTiffDeflateFile = extractBands(sImageToExtract,fLatN,fLonW,fLatS,fLonE)
        wasdi.wasdiLog("Generated RGB Tiff: " + sTiffDeflateFile)
        sOutputFile = sTiffDeflateFile.replace(".tiff", "_deflate.tiff")
        #stretchBandValues(sTiffFile, sOutputFile)
        # Delete intermediate Tiff File: NOTE this has not been added to WASDI
        # so there is the need to clean only the physical file
        try:
            os.remove(wasdi.getPath(sTiffDeflateFile))
        except:
            wasdi.wasdiLog("Error removing " + sTiffDeflateFile)
        # Add the real output to the WASDI Workspace
        # NOTE: here starts the opposite path: when running locally, WASDI will upload the file to the cloud
        wasdi.addFileToWASDI(sOutputFile)



def extractBands(sFile,fLatN, fLonW, fLatS, fLonE):
  try:
      sOutputVrtFile = sFile.replace(".tif", ".vrt")
      sOutputTiffFile = sFile
      # Get the Path
      sLocalFilePath = wasdi.getPath(sFile)
      sOutputVrtPath = wasdi.getPath(sOutputVrtFile)
      sOutputTiffPath = wasdi.getPath(sOutputTiffFile)
      asOrderedZipBands = []

      #Band Names for S2 L2
      asBandsJp2 = ['Sigma0_VV_db.jp2']
      image=gdal.Open(sLocalFilePath)
      band=image.GetRasterBand(1)
      # with zipfile.ZipFile(sLocalFilePath, 'r') as sZipFiles:
      #     asZipNameList = sZipFiles.namelist()
      #     asBandsS1 = [name for name in asZipNameList for band in asBandsJp2 if band in name]
      #     asBandsZip = ['/vsizip/' + sLocalFilePath + '/' + band for band in asBandsS1]
      #     asOrderedZipBands = []
      #     for sBand in ['Sigma0_VV_db']:
      #         for sZipBand in asBandsZip:
      #             if sBand in sZipBand:
      #                 asOrderedZipBands.append(sZipBand)
      #                 break
      #gdal.BuildVRT(sOutputVrtPath, asOrderedZipBands, separate=True)
      # , options="-tr " + sResolution + " " + sResolution
      translateoption=gdal.TranslateOptions(format="GTiff", options=['COMPRESS=DEFLATE'])
      gdal.Translate(sOutputTiffPath, image, options=translateoption)
      wasdi.mosaic()
      wasdi.multiSubset()
      os.remove(sOutputVrtPath)
      return sOutputTiffFile
  except Exception as oEx:
      wasdi.wasdiLog(f'extractBands EXCEPTION: {repr(oEx)}')
  return ""

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days

if __name__ == '__main__':
    wasdi.init("config.json")
    run()