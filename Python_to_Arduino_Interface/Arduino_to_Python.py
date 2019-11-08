# 
# This program is a basic outline of interaction between
# a Python Script and an Arduino.
# 
# The Basics of this Protocol can be expanded upon by
# setting up seperate serial ports for each Arduino and 
# addressing them each sequentially.
# 

import time                                                             # Needed for pauses in testing
from . import LoggingSetup as logging
from . import ArduinoSetup as Arduino                                          # API Library for WatLock Arduino Commands
#import LoggingSetup as logging


logger = logging.get_logger("MASTER----------------")

# LIST OF ARDUINOS
#Arduino.Arduino_List.append(["SERIAL_PORT_NAME"    , "SERIAL_#_OF_ARDUINO"     , ""])
Arduino.Arduino_List.append (["Testduino"           , "85735313033351409161"    , ""]) 

#Setup Serial Connections based on List above
Arduinos = Arduino.start_serial_connections()


#---------------------------------------------------------------------------------------------------------------------------------
#MAIN COMMAND LOOP

while (True): #Run Forever

    # Data request Command
    try:
        reply_from_arduino = Arduinos.Testduino.get_data()
        if not "ERROR" in reply_from_arduino:
            print (reply_from_arduino)
    except:
        logger.error("Arduino \"Testduino\" was not connected")                
    

    # Send text Command
    try:
        reply_from_arduino = Arduinos.Testduino.send_command("Test Command")
        if not "ERROR" in reply_from_arduino:
            print (reply_from_arduino)
    except:
        logger.error("Arduino \"Testduino\" was not connected")


    # Check if Arduino is functioning properly and reconnect if not
    try:
        reply_from_arduino = Arduinos.Testduino.test_command()
        if "ERROR" in reply_from_arduino:
            logger.error("Arduino \"Testduino\" is not communicating properly")
            Arduinos.reconnect("Testduino")
    except:
        logger.error("Arduino \"Testduino\" was not connected")


    print ("\n")
    time.sleep(2)                                                      # Pause so the terminal doesnt fill instantly (only needed for testing)
#---------------------------------------------------------------------------------------------------------------------------------   
