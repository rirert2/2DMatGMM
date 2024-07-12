"""
Author: Patrick Kaczmarek
Code that automates flake detection via microscope.
"""
import argparse
import json
import os

import cv2
import numpy as np

from demo.demo_functions import visualise_flakes
from GMMDetector import MaterialDetector

from mysql.connector import Error, connect
from getpass import getpass
# libs for the stage and camera?
# may have to interop?????????? prolly not tho i'd explode if i had to

# Args can stay, just remember final product will have no --num_image

def arg_parse() -> dict:
    """
    Parse arguments to the detect module

    Returns:
        dict: Dictionary of arguments
    """
    # fmt: off
    # arg for size of chips?
    parser = argparse.ArgumentParser(description="2DMatGMM Demo")
    parser.add_argument("--material", dest="material", help="Material to process", default="Graphene", type=str)
    parser.add_argument("--size", dest="size", help="Size threshold in pixels", default=200, type=int)
    parser.add_argument("--min_confidence", dest="min_confidence", help="The Confidence threshold", default=0.5, type=float)
    parser.add_argument("--chip_x", dest="chip_x", help="Chip's size wrt the x-axis, mm", default = 10, type = float)
    parser.add_argument("--chip_y", dest="chip_y", help="Chip's size wrt the y-axis, mm", default = 10, type = float )
    # fmt: on
    return vars(parser.parse_args())

args = arg_parse()

# Constants
FILE_DIR = os.path.dirname(os.path.abspath(__file__)) # keep
CONTRAST_PATH_ROOT = os.path.join(FILE_DIR, "..", "GMMDetector", "trained_parameters") # keep
DATA_DIR = os.path.join(FILE_DIR, "..", "Datasets", "GMMDetectorDatasets") # redirect
OUT_DIR = os.path.join(FILE_DIR, args["out"]) # keep? may want to make unique for every go
# path for camera input
# path for 
os.makedirs(OUT_DIR, exist_ok=True)

MATERIAL = args["material"]
SIZE_THRESHOLD = args["size"]

# PREP PHASE

# Initialize camera, stage, etc. as necessary

# loads up the contrast dictionary for whatever material we want
with open(os.path.join(CONTRAST_PATH_ROOT, f"{MATERIAL}_GMM.json")) as f:
    contrast_dict = json.load(f)

# makes a model object
model = MaterialDetector(
    # passes constrast_dict that we made above
    contrast_dict = contrast_dict,
    # size threshold in pixels, 200 nm
    size_threshold = SIZE_THRESHOLD,
    # just leave std as 5
    standard_deviation_threshold = 5,
    used_channels="BGR",
)

# store flakes in here
flakes = []

# go to top left with stage - may have to find it (?)
# may also need to figure out how to move the got dang stage properly
# set mag level to 2.5x
# warm up model (?) Python is weird so it may be our best bet to make sure that time is a nonissue

# SCANNING PHASE

# Start by scanning the chip at a low magnification level
# Result: Stitched together image - may be sloppy but that's alright, prepped for next phase

# go to top left
# take photo, store somewhere
# move to next area
# repeat
# if all the way to right or left, go one down in y and then swap directions in x
# when done, stitch together all the images and turnit back into a user-accesible image

# Scans at 20x mag level, scan for flakes
# Result: List of flakes, a way to retrieve their x&ys, prepped for next phase

# adj mag level, reset to wherever it's supposed to be 
# may have to adjust model inputs? idk tho

# go to top left
# take photo, pass to model
# store any flakes in array
# move to next area
# repeat
# if all the way to right or left, go one down in yand then swap directions in x

# Revisit flakes and take images at different magnification levels
# Result: Images that detail where exactly the flake is

# goto x,y of flake
# take image at 2.5x (unnecessary maybe)
# take image at 20x
# take image at 50x
# store images
# repeat for all flakes


# DATABASE PHASE
"""
TABLE GUIDE:

Chip:
PRIMARY KEY Chip_id: Int, A unique integer for identifying the chip; auto_increment
Material: Str, Name of the material of the chip (Graphene or WSe2)
Size: Int, Size of the chip, millimeters squared
Image: Str, Filepath to a decent-resolution image of the entire chip


Flake: 
Flake_id: Int, for identifying the flake: one ID per chip but not unqiue, so different flakes on different chips may have the same flake_id
    ^ don't forget to increment in code
FOREIGN Chip_id: Int, identifies which chip the flake is on, reference from Chip
PRIMARY KEY [Chip_id, Flake_id]: Combo that identifies the particular flake on a particular chip

Thickness: Str, The name of the layer the flake is from (TAKEN FROM FLAKE CLASS)
Size: Int, Size of the flake, micrometers squared (TAKEN FROM FLAKE CLASS)
Center_x: Int, identifies in x where to move the stage to center the flake (DERIVEN FROM FLAKE CLASS)
Center_y: INt, identifies in y where to move the stage to center the flake (DERIVEN FROM FLAKE CLASS)
Confidence: Float, confidence that the flake is correctly identified (DERIVEN FROM FLAKE CLASS)

LowMag: Str, Filepath to a 2.5x magnification image of the flake
MedMag: Str, Filepath to a 20x magnification image of the flake 
HighMag: Str, Filepath to a 50x magnification image of the flake


IMAGES NOT STORED ON DATABASE (WOULD DRASTICALLY SLOW DATABASE WRITES AND READS)
    Instead, images are stored natively.

File Structure:

Custom (YOU ARE HERE)
| -- Output
|
| ----Chip 1 (Image of chip_id = 1 exists here) 
| ------Flake 1 (All images of chip_id = 1, flake_id = 1 exists here)
| ------Flake 2 (etc)
| ------Flake {flake_id} (etc) 
|
| ----Chip 2 (etc)
| ------Flake {flake_id} (etc)
|
| ----Chip {chip_id} (etc)
| ------Flake {flake_id} (etc)

Chips that have been discarded can have their directory under Output as well as
    all of their sub-directories; just keep in mind that this doesn't automatically
    drop them from the database


"""

try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database = "test_db",
    ) as connection:
        create_db_query = "CREATE DATABASE flakes_db"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
except Error as e:
    print(e)

# Maybe make a website to host images?

# Database must be able to store the set amount of images and the location of the flake, aswell as the flake object itself
# Maybe make a parent class to Flake called FlakeEX that bundles everything together
# So, DB just holds onto FlakeEX that has everything above.
# A schema would be just fine because there's no need to have the flexibility of different possible flakes.
# Conclusion: Use MySQL

# If no database, alternative way to view a map of flakes?

# Seperate development path: A webapp to view the data from all of them?
# Would need a server for both the database and the webapp anyways. Need to see if I can get a donor laptop 
# for everything so I don't have to pack all this up + server + webapp and get it out to the team
