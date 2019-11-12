# 
# This program is a basic outline of interaction between
# a Python Script and an Arduino.
# 
# The Basics of this Protocol can be expanded upon by
# setting up seperate serial ports for each Arduino and 
# addressing them each sequentially.
# 

import time                                                             # Needed for pauses in testing
import LoggingSetup as logging  #noqa
import ArduinoSetup as Arduino  #noqa

logger = logging.get_logger("MASTER----------------")

# LIST OF ARDUINOS
#Arduino.Arduino_List.append(["SERIAL_PORT_NAME"    , "SERIAL_#_OF_ARDUINO"     , ""])
Arduino.Arduino_List.append (["Testduino"           , "6"    , ""]) 


#Setup Serial Connections based on List above
Arduinos = Arduino.initialize_serial_connections()

print("\n")

#---------------------------------------------------------------------------------------------------------------------------------
#MAIN COMMAND LOOP

while (True): 

    # Data request Command
    print(Arduinos.Testduino.get_data())

    # Command to send String Command
    print(Arduinos.Testduino.send_command("Test Command"))



    # Get Raw Pressure Data
    print(Arduinos.Testduino.send_command("Raw Pressure"))

    # Get Raw Temperature Data
    print(Arduinos.Testduino.send_command("Raw Temperature Celsius"))


    

    # Check if Arduino is functioning properly and reconnect if not
    Arduinos.check_connections()


    print ("\n")
    time.sleep(2)                                                      # Pause so the terminal doesnt fill instantly (only needed for testing)
#---------------------------------------------------------------------------------------------------------------------------------
