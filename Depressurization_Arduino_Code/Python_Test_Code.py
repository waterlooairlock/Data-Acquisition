# 
# This program is a basic outline of interaction between
# a Python Script and an Arduino.
# 
# The Basics of this Protocol can be expanded upon by
# setting up seperate serial ports for each Arduino and 
# addressing them each sequentially.
# 

import time                                                             # Needed for pauses in testing
import LoggingSetup as logging #noqa
import ArduinoSetup as Arduino #noqa

logger = logging.get_logger("MASTER----------------")

# LIST OF ARDUINOS
#Arduino.Arduino_List.append(["SERIAL_PORT_NAME"    , "SERIAL_#_OF_ARDUINO"                 , ""])
Arduino.Arduino_List.append (["Pressduino"        , "UniqueID: E0 22 9F D6 51 50 32 31 43 20 20 20 FF 0E 18 37"   , ""])

#Setup Serial Connections based on List above
Arduinos = Arduino.initialize_serial_connections(9600)

print("\n")

#---------------------------------------------------------------------------------------------------------------------------------
#MAIN COMMAND LOOP

while (True):

    command = input('Input "Pressurize" or Depressurize" to send the command to the arduino:\n').lower()


    if "depressurize" in command:
        # Send text Command
        try:
            print(Arduino.Pressduino.send_Command("Depressurize"))
        except:
            print("The arduino is not connected properly, try re-uploading and restarting the Python test script.\n")

    elif "pressurize" in command:
        try:
            print(Arduino.Pressduino.send_Command("Pressurize"))
        except:
            print("The arduino is not connected properly, try re-uploading and restarting the Python test script.\n")
    
    else:
        print("--Invalid command--")


    print ("\n")
    time.sleep(1)                                                      # Pause so the terminal doesnt fill instantly (only needed for testing)
#---------------------------------------------------------------------------------------------------------------------------------   
