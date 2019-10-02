# 
# This program is a basic outline of interaction between
# a Python Script and an Arduino.
# 
# The Basics of this Protocol can be expanded upon by
# setting up seperate serial ports for each Arduino and 
# andressing them each sequentially.
# 

import ArduinoSetup as Arduino                                          # API Library for WatLock Arduino Commands
import serial


# LIST OF ARDUINOS
#Arduino.Arduino_List.append(["SERIAL_PORT_NAME"    , "SERIAL_#_OF_ARDUINO"     , ""])
Arduino.Arduino_List.append (["Testduino"           , "85735313033351409161"    , ""]) 
 

#NECCESARY SETUP FOR SERIAL OBJECTS
Arduino.Match_Arduinos()                                                # Locate Arduinos based on Serial Number
i = 0
for a in range(Arduino.Arduino_List.length):
    if Arduino.Arduino_List[i][2] != "":                                # if Match_Arduino found the arduino
        exec (a[0] + " = Arduino.Create_Serial('" + a[2] + "', 9600)")  # Create Serial Objects for each Arduino in the list
    i += 1
i = 0
for a in Arduino.Arduino_List:
    if Arduino.Arduino_List[i][2] != "":                                # if Match_Arduino found the arduino
        exec ("Arduino.Start_Serial(" + a[0] + ")")                     # Start Each Serial Interface
    i += 1


#---------------------------------------------------------------------------------------------------------------------------------
#MAIN COMMAND LOOP

# This loop just repeatedly sends 3 different commands,
# the First being a data request, where the arduino just sends back data
# the Second being a command, where the arduino must receive a string command and then reply
# the Third being another command, could serve any purpose (possibly return the arduino information)

while (True): #Run Forever

    # Data request Command
    
    data_from_arduino = Testduino.get_data()                            # VSCode and other IDE's may dislike the use of an object that has not been created,
    print (data_from_arduino)                                           # This is due to the dynamic creation of the Serial Objects in the code above. Ignore these errors.
    
    # Command to send String Command
    
    reply_from_arduino = Testduino.send_command("Test Command")
    print (reply_from_arduino)
                

    #Extra third command for example
    
    reply_from_other = Testduino.other_command()
    print (reply_from_other)


    #time.sleep(1)                                                      # Pause so the terminal doesnt fill instantly (only needed for testing)
#---------------------------------------------------------------------------------------------------------------------------------   
    