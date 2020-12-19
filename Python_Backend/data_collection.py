
import threading
import multitimer

import config

class data_collection(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.logger = logging.get_logger("Data Collection")
        self.logger.info("Configuring sensor readings table")
        cursor = db.cursor()
        cursor.execute(open("./db_schema/schema.sql", "r").read()) # Run Database Schema to Create it
        cursor.close()
    
    def run(self):
        timers = [
            multitimer.MultiTimer(interval=1, function=self.depressurization),
            #other_timer = multitimer.MultiTimer(interval=seconds, function=other_function),
        ]
        
        for timer in timers:
            timer.start()
        while True:
            pass
    
    def upload_sensor_data(self, readings):
        query = "INSERT INTO sensor_readings(id,arduino_name,sensor_type,sensor_id,reading" \
                "VALUES(%d,%s,%s,%d,%f)"
        try:
            cursor = db.cursor()
            cursor.executemany(query, readings)
        except:
            self.logger.error("Writing sensor data to database FAILED")
        finally:
            cursor.close()
        return

    """ ──────── ARDUINO TIMER FUNCTIONS ──────── """
    def depressurization(self):
        arduino_id = 11
        arduino_name = 'depressurization'

        thread_lock.acquire()
        pressure = arduinos.get_sensor_reading(arduino_id, 1)
        temperature = arduinos.get_sensor_reading(arduino_id, 2)
        thread_lock.release()

        self.upload_sensor_data[(arduino_name, 'pressure',    arduino_id, 1, pressure),
                                (arduino_name, 'temperature', arduino_id, 2, temperature)]
    #def other_function(self):
