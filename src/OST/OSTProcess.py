# these imports we need to handle the folders, independent of the OS
import os
import sys
from pathlib import Path
from pprint import pprint

# this is the Sentinel1Scene class, that basically handles all the workflow from beginning to the end
from ost import Sentinel1Scene

# from ost.helpers.settings import set_log_level
# import logging
# set_log_level(logging.DEBUG)
# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def process (sImageToProcess):

    # get home folder
    home = Path.home()

    # create a processing directory
    output_dir = home /".wasdi"/"matteoaic@gmail.com"/"28f65c36-96a8-4357-89da-9b030b1f48f0"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(str(output_dir))
    scene_id=os.path.splitext(sImageToProcess)[0]
    s1 = Sentinel1Scene(scene_id)

    # print summarising infos about the scene
    s1.info()



    # create a S1Scene class instance based on the scene identifier of the first ever Dual-Pol Sentinel-1 IW product

    # ---------------------------------------------------
    # Some scenes to choose from

    # very first IW (VV/VH) S1 image available over Istanbul/Turkey
    # NOTE:only available via ASF data mirror


    # create an S1Scene instance


    # print summarising infos about the scene


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

    s1.create_ard(infile=output_dir/sImageToProcess, out_dir=output_dir, overwrite=True)

    print(" The path to our newly created ARD product can be obtained the following way:")
    s1.ard_dimap

    s1.create_rgb(outfile=output_dir/sImageToProcess / f"{s1.start_date}.tif")

    print(" The path to our newly created RGB product can be obtained the following way:")
    s1.ard_rgb
