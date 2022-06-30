# this is for the path handling and especially useful if you are on Windows
from pathlib import Path
from pprint import pprint
# 10 km buffer around AOI Point
from shapely.wkt import loads
from ost.helpers import vector as vec
# we will need this for our time of period definition
from datetime import datetime, timedelta

# this is the s1Project class, that basically handles all the workflow from beginning to the end
from ost import Sentinel1, Sentinel1Scene

# ----------------------------
# Area of interest
# ----------------------------

# Here we can either point to a shapefile or as well use
lat, lon = 41.8919, 12.5113
aoi = "POINT ({} {})".format(lon, lat)

# ----------------------------
# Time of interest
# ----------------------------
# we set only the start date to today - 30 days
start = ((datetime.today()-timedelta(days=2)) - timedelta(days=15)).strftime("%Y-%m-%d")

# ----------------------------
# Processing directory
# ----------------------------
# get home folder
home = Path.home()
# create a processing directory within the home folder
project_dir = home / "OST_Tutorials" / "Tutorial_3"

# ------------------------------
# Print out AOI and start date
# ------------------------------
print(
    "AOI: " + aoi,
)
print("TOI start: " + start)
print("Our project directory is located at: " + str(project_dir))


# ---------------------------------------------------

# create s1Project class instance
s1_project = Sentinel1(project_dir=project_dir, aoi=aoi, start=start, product_type="GRD")

s1_project.scihub_uname="robertognisci"
s1_project.scihub_pword="Ln2@U85jQgQVpCW"
s1_project.onda_uname="gniscir@gmail.com"
s1_project.onda_pword="S4538998_studenti"
s1_project.asf_uname= "GnisciRoberto"
s1_project.asf_pword= "yVEMTE?2?.PLAeN"
s1_project.peps_uname="gniscir@gmail.com"
s1_project.peps_pword="f7uyhm2dXFuVnP."
# search command
s1_project.search()
# uncomment in case you have issues with the registration procedure
# ost_s1.search(base_url='https://scihub.copernicus.eu/dhus')
print("We found {} products.".format(len(s1_project.inventory.identifier.unique())))
# combine OST class attribute with pandas head command to print out the first 5 rows of the
print(s1_project.inventory.head(5))

# we plot the full Inventory on a map
#s1_project.plot_inventory(transparency=0.1)

# ---------------------------------------------------
# for plotting purposes we use this iPython magic

#pylab.rcParams["figure.figsize"] = (13, 13)

# we give our inventory a shorter name iDf (for inventory Dataframe)
iDf = s1_project.inventory.copy()

# ---------------------------------------------------


# we select the latest scene based on the metadata entry endposition
latest_df = iDf[iDf.endposition == iDf.endposition.max()]

# we print out a little info on the date of the
print(" INFO: Latest scene found for {}".format(latest_df["acquisitiondate"].values[0]))

# we use the plotInventory method in combination with the newly
# created Geodataframe to see our scene footprint
#s1_project.plot_inventory(latest_df, transparency=0.5)

s1_project.download(latest_df,uname=s1_project.onda_uname,pword=s1_project.onda_pword)

# create a S1Scene class instance based on the scene identifier coming from our "latest scene dataframe"
latest_scene = Sentinel1Scene(latest_df["identifier"].values[0])

# print summarising infos
latest_scene.info()

# print file location
file_location = latest_scene.get_path(s1_project.download_dir)

print(" File is located at: ")
print(" " + str(file_location))




# turn WKT into shapely geometry object
shp_aoi = loads(s1_project.aoi)

# use OST helper's function to create a quadrant buffer for subset
subset_area = vec.geodesic_point_buffer(shp_aoi.x, shp_aoi.y, 10000, envelope=True)

print("-----------------------------------------------------------------------------")
latest_scene.create_ard(
    # we see our download path can be automatically generated by providing the Project's download directory
    infile=latest_scene.get_path(download_dir=s1_project.download_dir),
    # let's simply take our processing folder
    out_dir=s1_project.processing_dir,
    # define the subset
    subset=subset_area,
    # in case already processed, we will re-process
    overwrite=True,
)

print("-----------------------------------------------------------------------------")
print(" The path to our newly created ARD product can be obtained the following way:")
latest_scene.ard_dimap


latest_scene.create_rgb(outfile=s1_project.processing_dir / f"{latest_scene.start_date}.tif")
latest_scene.visualise_rgb(shrink_factor=1)