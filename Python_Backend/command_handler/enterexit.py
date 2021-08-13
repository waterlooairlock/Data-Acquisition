
from command_handler import *
from data_collection.__init__ import isMarsAtmosphere
import time

# This is an event-driven function that is called by flask
# Whenever there is an HTTP request made to:
# 127.0.0.1:8080/arduinos/enterexit
#
# For example, This HTTP request:
# http://127.0.0.1:8080/arduinos/enterexit?entering=true?inMars=true


@command_handler.route("/arduinos/enterexit")
def enterexit():
    if 'entering' not in request.args:
        api_logger.warning(
            "Depressurization command called without 'entering' declared: Aborted")
        return
    if 'inMars' not in request.args:
        api_logger.warning(
            "Depressurization command called without 'inMars' declared: Aborted")
        return
    # Read arguements into variables
    entering = request.args['entering']
    inMars = request.args['inMars']

    command_code = 0
    # open is 1
    # close is 0

    if entering:
      if not isMarsAtmosphere:
        arduinos.send_command(11, 1, bytearray([0x02]))
        time.sleep(2)
        arduinos.send_command(14, 1, bytearray([0x01]))
        arduinos.send_command(14, 1, bytearray([0x02]))
        time.sleep(2)

        # We need to wait until crew lock pressure matches max vacuum pressure
        # We will add this function once we know a valid threshold value

        time.sleep(2)
        arduinos.send_command(11, 1, bytearray([0x01]))
        time.sleep(2)

        arduinos.send_command(14, 0, bytearray([0x01]))
        arduinos.send_command(14, 0, bytearray([0x02]))     
        time.sleep(2)

        arduinos.send_command(14, 1, bytearray([0x04]))

        while not isMarsAtmosphere:
          continue

        arduinos.send_command(14, 0, bytearray([0x04]))

      time.sleep(10)

      arduinos.send_command(11, 1, bytearray([0x02]))
      time.sleep(2)

      arduinos.send_command(14, 1, bytearray([0x01]))
      arduinos.send_command(14, 1, bytearray([0x02]))
      time.sleep(2)

      # We need to wait until crew lock pressure matches max vacuum pressure
      # We will add this function once we know a valid threshold value

      arduinos.send_command(11, 1, bytearray([0x01]))
      time.sleep(2)

      arduinos.send_command(14, 0, bytearray([0x01]))
      arduinos.send_command(14, 0, bytearray([0x02]))     
      time.sleep(2)

      arduinos.send_command(14, 1, bytearray([0x05]))

      time.sleep(15)

      arduinos.send_command(14, 0, bytearray([0x05]))

    else:
      if isMarsAtmosphere:
        arduinos.send_command(11, 1, bytearray([0x02]))
        time.sleep(2)

        arduinos.send_command(14, 1, bytearray([0x01]))
        arduinos.send_command(14, 1, bytearray([0x02]))
        # We need to wait until crew lock pressure matches max vacuum pressure
        # We will add this function once we know a valid threshold value

        arduinos.send_command(11, 1, bytearray([0x01]))
        time.sleep(2)

        arduinos.send_command(14, 0, bytearray([0x01]))
        arduinos.send_command(14, 0, bytearray([0x02]))     
        time.sleep(2)

        arduinos.send_command(14, 1, bytearray([0x05]))

        while isMarsAtmosphere:
          continue

        arduinos.send_command(14, 0, bytearray([0x05]))

      time.sleep(15)

      arduinos.send_command(11, 1, bytearray([0x02]))
      time.sleep(2)

      arduinos.send_command(14, 1, bytearray([0x01]))
      arduinos.send_command(14, 1, bytearray([0x02]))
      # We need to wait until crew lock pressure matches max vacuum pressure
      # We will add this function once we know a valid threshold value

      arduinos.send_command(14, 0, bytearray([0x01]))
      arduinos.send_command(14, 0, bytearray([0x02]))
      time.sleep(2)


      arduinos.send_command(14, 1, bytearray([0x04]))

      while not isMarsAtmosphere:
        continue

      arduinos.send_command(14, 0, bytearray([0x04]))

    return 'okay'
