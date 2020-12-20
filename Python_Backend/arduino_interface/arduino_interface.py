
import struct
from smbus2 import SMBus

I2C_COMMAND_CODE = 1 # Alignes with enumerator values for message_type in data_acquisition_lib.h

class interface:
    def __init__(self, bus_number: int):
        self.bus = SMBus(bus_number)
        return

    def get_sensor_reading(self, arduino_ID: int, sensor_number: int):
        # Request reading from sensor, Data returned as float in 4 Bytes
        sensor_data = bytearray(self.bus.read_block_data(arduino_ID, sensor_number, 4))
        # Convert 4 raw bytes into Float value
        value = struct.unpack('>f', sensor_data[:4]) # Uses BIG ENDIAN, This may be incorrect. If float values are incorrect, try '>f' instead
        return value

    def send_command(self, arduino_ID: int, command_code: int, extra_data: bytearray):
        # Create Data array to send
        data_array = bytearray(command_code) + extra_data
        # Send command over I2C
        self.bus.write_block_data(arduino_ID, I2C_COMMAND_CODE, data_array)
        return
