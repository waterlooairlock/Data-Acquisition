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

logger = logging.get_logger("MASTER----------------")

# LIST OF ARDUINOS
#Arduino.Arduino_List.append(["SERIAL_PORT_NAME"    , "SERIAL_#_OF_ARDUINO"                 , ""])
Arduino.Arduino_List.append (["Testduino"           , "85735313033351409161"                , ""])
Arduino.Arduino_List.append (["Arduinot"            , "6"                                   , ""])

#Setup Serial Connections based on List above
Arduinos = Arduino.start_serial_connections()

print("\n")

#---------------------------------------------------------------------------------------------------------------------------------
#MAIN COMMAND LOOP

while (True):
    
    # Data request Command
    print(Arduinos.Testduino.get_data())

    # Send text Command
    print(Arduinos.Testduino.send_command("Test Command"))  



    # Data request Command
    print(Arduinos.Arduinot.get_data())
    
    # Send text Command
    print(Arduinos.Arduinot.send_command("Test Command"))



    Arduinos.check_connections()


    print ("\n")
    time.sleep(1)                                                      # Pause so the terminal doesnt fill instantly (only needed for testing)
#---------------------------------------------------------------------------------------------------------------------------------   
