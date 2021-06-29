
from config import *
#from config import database_config
import mysql.connector
import pymongo

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
        # Make connection and add sensor readings, otherwise log the error
        try:
            db = mysql.connector.connect(**database_config)
            db.autocommit = True
            cursor = db.cursor()
            cursor.executemany(query, readings)
            cursor.close()
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
            multitimer.MultiTimer(interval=1, function=self.depressurization),
            #other_timer = multitimer.MultiTimer(interval=seconds, function=other_function),
        ]
        # Start all timers and enter while-true
        self.logger.info("Starting Arduino Data Timers")
        for timer in timers:
            timer.start()
        while True:
            pass

    """ ──────── TIMER FUNCTIONS ──────── """

    def depressurization(self):
        # Group variables for Arduino
        arduino_name = 'depressurization'
        arduino_id = 11
        ts = self.get_timestamp()
        # Grab thread_lock (concurrency for I2C) and get sensor readings
        thread_lock.acquire()
        #pressure = arduinos.get_sensor_reading(arduino_id, 1)
        #temperature = arduinos.get_sensor_reading(arduino_id, 2)
        thread_lock.release()
        # Send Readings to MySQL Database
        self.upload_sensor_data([
            (arduino_name, arduino_id, 'pressure', 1, 21, ts),
            (arduino_name, arduino_id, 'temperature', 2, 23, ts)])

    # def other_function(self):

