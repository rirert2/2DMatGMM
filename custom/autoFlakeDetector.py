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

# libs?

# Args can stay, just remember final product will have no --num_image

def arg_parse() -> dict:
    """
    Parse arguments to the detect module

    Returns:
        dict: Dictionary of arguments
    """
    # fmt: off
    parser = argparse.ArgumentParser(description="2DMatGMM Demo")
    parser.add_argument("--out", dest="out", help="Output directory", default="output", type=str)
    parser.add_argument("--num_image", dest="num_image", help="Number of images to process", default=10, type=int)
    parser.add_argument("--material", dest="material", help="Material to process", default="Graphene", type=str)
    parser.add_argument("--size", dest="size", help="Size threshold in pixels", default=200, type=int)
    parser.add_argument("--std", dest="std", help="Standard deviation threshold", default=5, type=float)
    parser.add_argument("--min_confidence", dest="min_confidence", help="The Confidence threshold", default=0.5, type=float)
    parser.add_argument("--channels", dest="channels", help="Channels to use", default="BGR", type=str)
    parser.add_argument("--shuffel", dest="shuffel", default=True, type=bool)
    # fmt: on
    return vars(parser.parse_args())

args = arg_parse()

# Constants
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRAST_PATH_ROOT = os.path.join(FILE_DIR, "..", "GMMDetector", "trained_parameters")
DATA_DIR = os.path.join(FILE_DIR, "..", "Datasets", "GMMDetectorDatasets")
OUT_DIR = os.path.join(FILE_DIR, args["out"])
os.makedirs(OUT_DIR, exist_ok=True)

NUM_IMAGES = args["num_image"]
MATERIAL = args["material"]
SIZE_THRESHOLD = args["size"]
STD_THRESHOLD = args["std"]

# loads up the contrast dictionary for whatever material we want
with open(os.path.join(CONTRAST_PATH_ROOT, f"{MATERIAL}_GMM.json")) as f:
    contrast_dict = json.load(f)

# makes a model object
model = MaterialDetector(
    # passes constrast_dict that we made above
    contrast_dict=contrast_dict,
    # size threshold in pixels, 200 nm
    size_threshold=SIZE_THRESHOLD,
    standard_deviation_threshold=STD_THRESHOLD,
    used_channels="BGR",
)

# SCANNING PHASE

# Start by scanning the chip at a low magnification level
# Result: Stitched together image - may be sloppy but that's alright

# Scans at 20x mag level, scan for flakes
# Result: List of flakes, a way to retrieve their x&ys

# adj mag level, reset to wherever it's supposed to be 
# may have to adjust model inputs? idk tho

# go to top left
#  


# Revisit flakes and take images at different magnification levels
# Result: Images that detail where exactly the flake is

# goto x,y
# take image at 2.5x (unnecessary maybe)
# take image at 20x
# take image at 50x
# store
# repeat


# DATABASE PHASE

# Upload images to database
# Maybe make a website to host images?

# If no database, alternative way to view a map of flakes?