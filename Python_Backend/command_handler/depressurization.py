
from command_handler import *

@command_handler.route("/arduinos/depressurization")
def depressurization_command():
    if 'command' not in request.args:
        api_logger.warning("Depressurization command called without 'command' declared: Aborted")
        return
    if 'value' not in request.args:
        api_logger.warning("Depressurization command called without 'value' declared: Aborted")
        return
    # Read arguements into variables
    value = request.args['value']
    command = request.args['command']
    command_code = 0
    extra_data = 0

    # Handle each command
    if command == "pump_control":
        command_code = 1
        if value == "stop":  extra_data = [0x01]
        if value == "start": extra_data = [0x02]
    elif command == "value_control":
        command_code = 2
        if value == "close": extra_data = [0x01]
        if value == "open":  extra_data = [0x02]
    
    # Send message or log failure
    if command_code != 0 and extra_data != 0:
        arduinos.send_command(11, command_code, bytearray(extra_data))
    else:
        api_logger.warning("Depressurization command called with unknown parameters: command='%s', value='%s': Aborted", command, value)
        print(command)
        print(value)
    return 'okay'