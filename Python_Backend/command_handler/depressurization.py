
from command_handler import *

# This is an event-driven function that is called by flask
# Whenever there is an HTTP request made to:
# 127.0.0.1:8080/arduinos/depressurization
#
# For example, This HTTP request:
# http://127.0.0.1:8080/arduinos/depressurization?command=pump_control&value=stop
#
# Sends a "pump_control" command with a value of "stop", these
# request parameters are parsed below and the needed command
# is send to the arduino responsible.
#
# There is also a good amount of logging used to make it easier
# to debug issues on both the Python and Arduino end.
#
# Currently, this only handles "pump_control" and "valve_control"
# commands, but more can be easily added.
#
# IT WOULD BE WISE TO COPY THIS EXACT FUNCTION AND MODIFY IT
# AS NEEDED FOR OTHER ARDUINOS.


@command_handler.route("/arduinos/depressurization")
def depressurization_command():
    if 'command' not in request.args:
        api_logger.warning(
            "Depressurization command called without 'command' declared: Aborted")
        return
    if 'value' not in request.args:
        api_logger.warning(
            "Depressurization command called without 'value' declared: Aborted")
        return
    # Read arguements into variables
    value = request.args['value']
    command = request.args['command']
    command_code = 0
    extra_data = 0

    # Handle each command
    if command == "pump_control":
        command_code = 1  # This is the command code that will be sent to the arduino, will be handled by the `handle_command()` function
        if value == "stop":
            # This is extra data that will be send to the arduino
            extra_data = [0x01]
        if value == "start":
            extra_data = [0x02]
    elif command == "valve_control":
        command_code = 2  # Ditto
        if value == "close":
            extra_data = [0x01]  # Ditto
        if value == "open":
            extra_data = [0x02]

    # Send message or log failure
    if command_code != 0:
        arduinos.send_command(11, command_code, bytearray(extra_data))
    else:
        api_logger.warning(
            "Depressurization command called with unknown parameters: command='%s', value='%s': Aborted",
            command,
            value)
        print(command)
        print(value)
    return 'okay'
