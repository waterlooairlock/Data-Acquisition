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

logger = logging.get_logger("Master")

# LIST OF ARDUINOS
#Arduino.Arduino_List.append(["SERIAL_PORT_NAME"    , "SERIAL_#_OF_ARDUINO"     , ""])
Arduino.Arduino_List.append (["Testduino"           , "85735313033351409161"    , ""]) 

Arduinos = Arduino.start_serial_connections()

#---------------------------------------------------------------------------------------------------------------------------------
#MAIN COMMAND LOOP

# This loop just repeatedly sends 3 different commands,
# the First being a data request, where the arduino just sends back data
# the Second being a command, where the arduino must receive a string command and then reply
# the Third being another command, could serve any purpose (possibly return the arduino information)

while (True): #Run Forever


    # Data request Command
    try:
        reply_from_arduino = Arduinos.Testduino.get_data()
        if not "ERROR" in reply_from_arduino:
            print (reply_from_arduino)
    except:
        logger.error("Arduino \"Testduino\" was not connected")
    

    # Command to send String Command
    try:
        reply_from_arduino = Arduinos.Testduino.send_command("Test Command")
        if not "ERROR" in reply_from_arduino:
            print (reply_from_arduino)
    except:
        logger.error("Arduino \"Testduino\" was not connected")



    # Get Raw Pressure Data
    try:
        reply_from_arduino = Arduinos.Testduino.send_command("Raw Pressure")
        if not "ERROR" in reply_from_arduino:
            print (reply_from_arduino)
    except:
        logger.error("Arduino \"Testduino\" was not connected")
    


    # Get Raw Temperature Data
    try:
        reply_from_arduino = Arduinos.Testduino.send_command("Raw Temperature Celsius")
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
