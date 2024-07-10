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

from mysql.connector import Error, connect
from getpass import getpass

"""
Connect to the MySQL server.
Create a new database.
Connect to the newly created or an existing database.
Execute a SQL query and fetch results.
Inform the database if any changes are made to a table.
Close the connection to the MySQL server.
"""


try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database = "test_db",
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("DESCRIBE movies")
            result = cursor.fetchall()
            for row in result: 
                print(row)
except Error as e:
    print(e)