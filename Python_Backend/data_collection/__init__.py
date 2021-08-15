
from config import *
#from config import database_config
import pymongo
import multitimer
from secret import MONGOURI

from config import arduinos

isMarsAtmosphere = False


class data_collection(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        # Create Logger
        self.logger = logging.get_logger("Data Collection")
        self.logger.info("Configuring sensor readings table")
        # Connect to database and verify connection
        try:
            dbclient = pymongo.MongoClient(MONGOURI)
            mydb = dbclient["watlock"]

            self.logger.info("Database Connection Succeded")
        except BaseException:
            self.logger.error("Database Connection Failed!")
            os._exit(1)  # ABORT

        sensor_readings_collection = mydb['sensor_readings']

    def upload_sensor_data(self, arduino_name, arduino_id,
                           sensor_type, sensor_id, reading):
        new_item = {
            "arduino_name": arduino_name,
            "arduino_id": arduino_id,
            "sensor_type": sensor_type,
            "sensor_id": sensor_id,
            "reading": reading,
            "timestamp": self.get_timestamp()
        }

        if sensor_type == "pressure" and reading > 10000:
            isMarsAtmosphere = False
        else:
            isMarsAtmosphere = True

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
            multitimer.MultiTimer(
                interval=60, function=self.air_quality_readings),
            multitimer.MultiTimer(
                interval=60, function=self.pressure_readings),
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
        # Grab thread_lock (concurrency for I2C) and get sensor readings
        thread_lock.acquire()
        temperature = arduinos.get_sensor_reading(
            self, arduino_ID=arduino_id, sensor_number=1)
        thread_lock.release()
        # Send Readings to Database
        self.upload_sensor_data(
            arduino_name,
            arduino_id,
            'temperature',
            2,
            temperature)

    def air_quality_readings(self):
        # Group variables for Arduino
        arduino_name = 'air_quality_readings'
        arduino_id = 12
        # Grab thread_lock (concurrency for I2C) and get sensor readings
        thread_lock.acquire()
        air_quality = arduinos.get_sensor_reading(
            self, arduino_ID=arduino_id, sensor_number=2)  # sensor number 2
        thread_lock.release()
        # Send Readings to Database
        self.upload_sensor_data(
            arduino_name,
            arduino_id,
            'air_quality',
            2,
            air_quality)

    def pressure_readings(self):
        # Group variables for Arduino
        arduino_name = 'pressure_readings'
        arduino_id = 12
        # Grab thread_lock (concurrency for I2C) and get sensor readings
        thread_lock.acquire()
        pressure = arduinos.get_sensor_reading(
            self, arduino_ID=arduino_id, sensor_number=3)  # sensor number 3
        thread_lock.release()
        # Send Readings to Database
        self.upload_sensor_data(
            arduino_name,
            arduino_id,
            'pressure',
            3,
            pressure)

   # def other_function(self):
