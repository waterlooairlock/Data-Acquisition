# 
# This program is a basic outline of interaction between
# a Python Script and an Arduino.
# 
# The Basics of this Protocol can be expanded upon by
# setting up seperate serial ports for each Arduino and 
# addressing them each sequentially.
# 

import time                                                             # Needed for pauses in testing
import LoggingSetup as logging
import ArduinoSetup as Arduino                                          # API Library for WatLock Arduino Commands
#import LoggingSetup as logging


logger = logging.get_logger("Master")

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
        reply_from_arduino = Arduinos.Testduino.get_data()                               # VSCode and other IDE's may dislike the use of an object that has not been created,
        print (reply_from_arduino)                                                       # This is due to the dynamic creation of the Serial Objects in the code above. Ignore these errors.
    except:
        logger.warning("ERROR: Arduino \"Testduino\" was not connected")
    

    # Command to send String Command
    try:
        reply_from_arduino = Arduinos.Testduino.send_command("Test Command")
        print (reply_from_arduino)
    except:
        logger.warning("ERROR: Arduino \"Testduino\" was not connected")



    try:
        Arduinos.reconnect("Testduino")
    except:
        logger.warning("ERROR: Arduino cannot be found for restart")


    print ("\n")
    time.sleep(1)                                                      # Pause so the terminal doesnt fill instantly (only needed for testing)
#---------------------------------------------------------------------------------------------------------------------------------   
