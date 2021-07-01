"""
This is the shared configuration for the various unit files
of this Python project.
"""

# Built in
import os
import time
import datetime

# Generic
import argparse
import threading
import multitimer
import pymongo

# Modules and Packages

import arduino_interface
import Custom_Logging as logging

# Configure Arguement parser
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--no_i2c',
                        action='store_true',
                        help='Run this Backend with a Dummy Arduino Interface. This interface will output to a seperate log file instead of the physical I2C interface. Returned sensor readings are random.')
args = arg_parser.parse_args()
use_i2c = not vars(args)["no_i2c"]

# Determine if Real Arduinos or the fake interface should be used.

if use_i2c:
    arduinos = arduino_interface.arduino_interface.interface
else:
    arduinos = arduino_interface.fake_arduino_interface.interface

logger = logging.get_logger("Database connection")
try:
    dbclient = pymongo.MongoClient('mongodb+srv://watlock:general@cluster0.7s0cr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    mydb = dbclient["watlock"]
    sensor_readings_collection = mydb['sensor_readings']
    logger.info("Database connected successfully")
except:
    logger.error("Database failed to connect")

# Global variables
thread_lock = threading.Lock()
threads = []

logger = logging.get_logger("Database connection")
try:
    dbclient = pymongo.MongoClient('mongodb+srv://watlock:general@cluster0.7s0cr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    mydb = dbclient["watlock"]
    sensor_readings_collection = mydb['sensor_readings']
    logger.info("Database connected successfully")
except:
    logger.error("Database failed to connect")