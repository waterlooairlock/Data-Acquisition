"""
This is the shared configuration for the various unit files
of this Python project.
"""

# Built in
from arduino_interface import fake_arduino_interface
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
import custom_logging as logging

# Configure Arguement parser
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--no_i2c',
                        action='store_true',
                        help='Run this Backend with a Dummy Arduino Interface. This interface will output to a seperate log file instead of the physical I2C interface. Returned sensor readings are random.')
args = arg_parser.parse_args()
use_i2c = not vars(args)["no_i2c"]

# Use 
if use_i2c:
    arduinos = arduino_interface.interface(1)
else:
    arduinos = fake_arduino_interface.interface()

thread_lock = threading.Lock()
threads = []
database_config = {
    'host':'localhost',
    'user':'watlock_user',
    'password':'elon_gated_musk_rat',
    'database':'watlock'
}
