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

#Setup Serial Connections based on List above
Arduinos = Arduino.start_serial_connections()


#---------------------------------------------------------------------------------------------------------------------------------
#MAIN COMMAND LOOP

# This loop just repeatedly sends 3 different commands,
# the First being a data request, where the arduino just sends back data
# the Second being a command, where the arduino must receive a string command and then reply
# the Third being another command, could serve any purpose (possibly return the arduino information)

while (True): #Run Forever

    # Data request Command
    if (Arduino.Arduino_List[0][2] != ''):
        data_from_arduino = Arduinos.Testduino.get_data()                               # VSCode and other IDE's may dislike the use of an object that has not been created,
        print (data_from_arduino)                                                       # This is due to the dynamic creation of the Serial Objects in the code above. Ignore these errors.

    else:
        print ("Testduino Is not connected, Failed to get data")
    
    # Command to send String Command
    if (Arduino.Arduino_List[0][2] != ''):
        reply_from_arduino = Arduinos.Testduino.send_command("Test Command")
        print (reply_from_arduino)
    else:
        print ("Testduino Is not connected, Failed to send Command")
                

    #Extra third command for example
    if (Arduino.Arduino_List[0][2] != ''):
        reply_from_other = Arduinos.Testduino.other_command()
        print (reply_from_other)
    else:
        print ("Testduino Is not connected, Failed to send Command")


    time.sleep(1)                                                      # Pause so the terminal doesnt fill instantly (only needed for testing)
#---------------------------------------------------------------------------------------------------------------------------------   
