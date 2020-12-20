"""
This is the shared configuration for the various unit files
of this Python project.
"""

# Built in
import os
import time
import datetime

# Generic
import threading
import multitimer
import mysql.connector

# Modules and Packages
import Custom_Logging as logging
from arduino_interface import *

arduinos = arduino_interface(1)
thread_lock = threading.Lock()
threads = []
database_config = {
    'host':'localhost',
    'user':'watlock_user',
    'password':'elon_gated_musk_rat',
    'database':'watlock'
}

