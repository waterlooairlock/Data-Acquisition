
import struct
from smbus2 import SMBus

I2C_COMMAND_CODE = 1 # Alignes with enumerator values for message_type in data_acquisition_lib.h

# This interface class allows the Python Backend to send commands
# and request sensor readings from the various arduinos in the system
class interface:
    def __init__(self, bus_number: int):
        self.bus = SMBus(bus_number)
        return

    # Get a sensor readings from an arduino with a given id.
    # This will ultimately call the `get_sensor_[number]()`
    # function on the specified arduino. The arduino will
    # send the value over I2C and it will be returned from
    # this function.
    def get_sensor_reading(self, arduino_ID: int, sensor_number: int):
        # Request reading from sensor, Data returned as float in 4 Bytes
        sensor_data = bytearray(self.bus.read_block_data(arduino_ID, sensor_number, 4))
        # Convert 4 raw bytes into Float value
        value = struct.unpack('>f', sensor_data[:4]) # Uses BIG ENDIAN, This may be incorrect. If float values are incorrect, try '>f' instead
        return value

    # Send a text command to the arduino, This will call the `handle_commnd()`
    # function on thw arduino. No value is returned from the arduino.
    def send_command(self, arduino_ID: int, command_code: int, extra_data: bytearray):
        # Create Data array to send
        data_array = bytearray(command_code) + extra_data
        # Send command over I2C
        self.bus.write_block_data(arduino_ID, I2C_COMMAND_CODE, data_array)
        return
