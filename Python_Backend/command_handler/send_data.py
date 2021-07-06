
from command_handler import *

# This is an event-driven function that is called by flask
# Whenever there is an HTTP request made to:
# 127.0.0.1:8080/getdata?sensor=temperature
#
# There is also a good amount of logging used to make it easier
# to debug issues on both the Python and Arduino end.

@command_handler.route("/getdata")
def get_data():
    sensor = request.args['sensor']

    if(sensor != 'temperature' or sensor != 'pressure' or sensor != 'airquality'):
      return 
    
    sensor_reading = command_handler.send_sensor_value(sensor)

    api_logger.info("Sending sensor values to the ")
    return {
      'reading': sensor_reading,
      'sensor': sensor
    }
