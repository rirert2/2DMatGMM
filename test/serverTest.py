"""
Author: Patrick Kaczmarek
General server-related testing things
"""
import argparse
import json
import os

import cv2
import numpy as np

from demo.demo_functions import visualise_flakes
from GMMDetector import MaterialDetector

import time

import mysql.connector
