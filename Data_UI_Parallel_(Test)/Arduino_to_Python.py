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

def master(pipe):

    logger = logging.get_logger("DATA_MASTER----------------")

    # LIST OF ARDUINOS
    #Arduino.Arduino_List.append(["SERIAL_PORT_NAME"    , "SERIAL_#_OF_ARDUINO"                                         , ""])
    Arduino.Arduino_List.append (["Testduino"           , "UniqueID: 58 37 33 33 30 39 0E 0C 11"                        , ""])
    Arduino.Arduino_List.append (["Arduinot"            , "UniqueID: 27 F4 A2 EF 51 50 32 31 43 20 20 20 FF 0E 17 3C"   , ""])
    Arduino.Arduino_List.append (["Anotherduino"        , "UniqueID: E0 22 9F D6 51 50 32 31 43 20 20 20 FF 0E 18 37"   , ""])

    #Setup Serial Connections based on List above
    Arduinos = Arduino.initialize_serial_connections(9600)

    print("\n")

    #---------------------------------------------------------------------------------------------------------------------------------
    #MAIN COMMAND LOOP

    while (True):
        try:
            text = pipe.recv()
        except:
            text = ""
        if text == "Test":
            logger.error("Received: %s",text)
            pipe.send("Test Recieved")
        
        # Data request Command
        print(Arduinos.Testduino.get_data())

        # Send text Command
        print(Arduinos.Testduino.send_command("Test Command"))  



        # Data request Command
        print(Arduinos.Arduinot.get_data())
        
        # Send text Command
        print(Arduinos.Arduinot.send_command("Test Command"))
        
        
        


        if not Arduinos.Testduino.check_connection():
            Arduinos.Testduino.reconnect()

        if not Arduinos.Arduinot.check_connection():
            Arduinos.Arduinot.reconnect()

        #print(Arduinos.reconnect_all())

        print(Arduinos.check_all_connections())
        


        print ("\n")
        time.sleep(3)                                                      # Pause so the terminal doesnt fill instantly (only needed for testing)
    #---------------------------------------------------------------------------------------------------------------------------------   


if __name__ == "__main__":
    master(None)