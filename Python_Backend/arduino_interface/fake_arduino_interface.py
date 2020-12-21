
import time
import random
import logging
from custom_logging import log_path, get_logger

random.seed("WatLock") # Seed random number generator. Use constant seed so the values are always the same

class interface:
    def __init__(self):
        # Configure Logging for Fake Arduino
        log_format = '%(asctime)s  %(name)18s : %(levelname)7s > %(message)-70s [%(filename)-21s | ln:%(lineno)d]'
        file_handler = logging.FileHandler(filename=log_path+'Fake_Arduino.log', mode='w')
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(logging.DEBUG) # NOTE <-- Set log level here, Generally set to DEBUG
        self.logger = get_logger("Fake Arduino")
        self.logger.addHandler(file_handler)
        # Log Initialization
        self.logger.info("Initializing Fake Arduino")
        pass

    def get_sensor_reading(self, arduino_ID: int, sensor_number: int):
        # Generate Random float value
        value = round(random.uniform(0, 10),6)
        # Log Request
        self.logger.debug("Data request: {arduino_ID:%s, sensor_number:%s}, returned value {%s}", arduino_ID, sensor_number, value)
        return value

    def send_command(self, arduino_ID: int, command_code: int, extra_data: bytearray):
        # Log Command
        self.logger.debug("Command: {arduino_ID:%s, command_code:%s, extra_data:%s", arduino_ID, command_code, extra_data)
        return
