
from config import *
#from config import database_config
import mysql.connector
import pymongo
from config import sensor_readings_collection
import multitimer

from config import arduinos
class data_collection(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        # Create Logger
        self.logger = logging.get_logger("Data Collection")
        self.logger.info("Configuring sensor readings table")
        # Connect to database and verify connection
        try:
            dbclient = pymongo.MongoClient('mongodb+srv://watlock:general@cluster0.7s0cr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
            mydb = dbclient["watlock"]

            self.logger.info("Database Connection Succeded")
        except BaseException:
            self.logger.error("Database Connection Failed!")
            os._exit(1)  # ABORT

        sensor_readings_collection = mydb['sensor_readings']

    def upload_sensor_data(self, arduino_name, arduino_id, sensor_type, sensor_id, reading):
        query = "INSERT INTO sensor_readings (arduino_name,arduino_id,sensor_type,sensor_id,reading,time)" \
                "VALUES(%s,%s,%s,%s,%s,%s)"

        new_item = {
            "arduino_name": arduino_name,
            "arduino_id": arduino_id,
            "sensor_type": sensor_type,
            "sensor_id": sensor_id,
            "reading": reading,
            "timestamp": self.get_timestamp(self)
        }

        try:
            sensor_readings_collection.insert_one(new_item)
            self.logger.debug("Successful write to database")
        except Exception:
            self.logger.exception("Writing to database FAILED")
        return

    def get_timestamp(self):
        ts = time.time()
        return datetime.datetime.fromtimestamp(
            ts).strftime('%Y-%m-%d %H:%M:%S')

    """ ──────── Primary Run Function for Thread ──────── """

    def run(self):
        # Create timers for each Arduino
        timers = [
            multitimer.MultiTimer(interval=60, function=self.rtd_thermometer),
            #other_timer = multitimer.MultiTimer(interval=seconds, function=other_function),
        ]
        # Start all timers and enter while-true
        self.logger.info("Starting Arduino Data Timers")
        for timer in timers:
            timer.start()
        while True:
            pass

    """ ──────── TIMER FUNCTIONS ──────── """

    def rtd_thermometer(self):
        # Group variables for Arduino
        arduino_name = 'rtd_thermometer'
        arduino_id = 12
        ts = self.get_timestamp()
        # Grab thread_lock (concurrency for I2C) and get sensor readings
        thread_lock.acquire()
        temperature = arduinos.get_sensor_reading(arduino_id, 1)
        thread_lock.release()
        # Send Readings to Database
        self.upload_sensor_data(arduino_name, arduino_id, 'temperature', 2, temperature, ts)

   # def other_function(self):
