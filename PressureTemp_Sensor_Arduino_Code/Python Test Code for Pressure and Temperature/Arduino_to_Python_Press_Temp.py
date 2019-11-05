# 
# This program is a basic outline of interaction between
# a Python Script and an Arduino.
# 
# The Basics of this Protocol can be expanded upon by
# setting up seperate serial ports for each Arduino and 
# addressing them each sequentially.
# 

import time                                                             # Needed for pauses in testing
import ArduinoSetup as Arduino                                          # API Library for WatLock Arduino Commands


# LIST OF ARDUINOS
#Arduino.Arduino_List.append(["SERIAL_PORT_NAME"    , "SERIAL_#_OF_ARDUINO"     , ""])
Arduino.Arduino_List.append (["Testduino"           , "85735313033351409161"    , ""]) 

Arduinos = Arduino.start_serial_connections()
print ("\n")

#---------------------------------------------------------------------------------------------------------------------------------
#MAIN COMMAND LOOP

# This loop just repeatedly sends 3 different commands,
# the First being a data request, where the arduino just sends back data
# the Second being a command, where the arduino must receive a string command and then reply
# the Third being another command, could serve any purpose (possibly return the arduino information)

while (True): #Run Forever


    # Data request Command
    if (Arduino.Arduino_List[0][2] != ''):
        reply_from_arduino = Arduinos.Testduino.get_data() # noqa     
        print (reply_from_arduino)                                           # This is due to the dynamic creation of the Serial Objects in the code above. Ignore these errors.
    else:
        print ("ERROR: No Connection")
    

    # Command to send String Command
    if (Arduino.Arduino_List[0][2] != ''):
        reply_from_arduino = Arduinos.Testduino.send_command("Test Command") # noqa
        print (reply_from_arduino)
    else:
        print ("ERROR: No Connection")



    # Get Raw Pressure Data
    if (Arduino.Arduino_List[0][2] != ''):
        reply_from_arduino = Arduinos.Testduino.send_command("Raw Pressure") # noqa
        print (reply_from_arduino)
    else:
        print ("ERROR: No Connection")
    


    # Get Raw Temperature Data
    if (Arduino.Arduino_List[0][2] != ''):
        reply_from_arduino = Arduinos.Testduino.send_command("Raw Temperature Celsius") # noqa
        print (reply_from_arduino)
    else:
        print ("ERROR: No Connection")
                


    #Extra third command for example
    if (Arduino.Arduino_List[0][2] != ''):
        reply_from_arduino = Arduinos.Testduino.other_command() # noqa
        print (reply_from_arduino)
    else:
        print ("ERROR: No Connection")



    print ("\n")
    time.sleep(0.5)                                                      # Pause so the terminal doesnt fill instantly (only needed for testing)
#---------------------------------------------------------------------------------------------------------------------------------   
