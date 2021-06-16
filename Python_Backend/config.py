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
import mysql.connector

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
    arduinos = arduino_interface.arduino_interface
else:
    arduinos = arduino_interface.fake_arduino_interface

# Global variables
thread_lock = threading.Lock()
threads = []
database_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'watlock'
}
