
import time
import random
import logging
from custom_logging import log_path, get_logger

# Use constant seed so the random values are always the same
random.seed("WatLock")  # Seed random number generator.

# This is a fake Arduino Interface. The primary purpose of this
# is to allow developers to test the backend without needing an
# actual arduino with sensors setup to handle the requests and
# commands. This class writes messages to the "logs\Fake_Arduino.log"
# file. These logs will show the requests sent by the Backend,
# and the values returned by the fake interface.


class interface:
    def __init__(self):
        # Configure Logging for Fake Arduino
        log_format = '%(asctime)s  %(name)18s : %(levelname)7s > %(message)-70s [%(filename)-21s | ln:%(lineno)d]'
        file_handler = logging.FileHandler(
            filename=log_path + 'Fake_Arduino.log', mode='w')
        file_handler.setFormatter(logging.Formatter(log_format))
        # NOTE <-- Set log level here, Generally set to DEBUG
        file_handler.setLevel(logging.DEBUG)
        self.logger = get_logger("Fake Arduino")
        self.logger.addHandler(file_handler)
        # Log Initialization
        self.logger.info("Initializing Fake Arduino")
        pass

    # This simulates getting a reading from an Arduino Sensor.
    # A random value between 0 and 10 is returned, and a log
    # message is written to the log file.
    def get_sensor_reading(self, arduino_ID: int, sensor_number: int):
        # Generate Random float value
        value = round(random.uniform(0, 10), 6)
        # Log Request
        self.logger.debug(
            "Data request: {arduino_ID:%s, sensor_number:%s}, returned value {%s}",
            arduino_ID,
            sensor_number,
            value)
        return value

    # This simulates sending a command to an Arduino. No message
    # is sent anywhere, but a log message with the content of the
    # command is written to the log file.
    def send_command(self, arduino_ID: int, command_code: int,
                     extra_data: bytearray):
        # Log Command
        self.logger.debug(
            "Command: {arduino_ID:%s, command_code:%s, extra_data:%s",
            arduino_ID,
            command_code,
            extra_data)
        return
