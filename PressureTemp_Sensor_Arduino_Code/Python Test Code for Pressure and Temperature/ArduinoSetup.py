# 
# This library is created as an API between the Python
# script and the Arduinos for the WatLock Design project
#


import time
import LoggingSetup as logging
import serial
import serial.tools.list_ports


Arduino_List = [] # [English Name, Serial #, Port]
logger = logging.get_logger("Arduino Setup")

###################################################################
def Match_Arduinos ():
    logger = logging.get_logger("Match_Arduinos()")                     # Create Logger object for this function
    ports = list(serial.tools.list_ports.comports())                    # Creates list of Available Serial Ports on the System
    logger.info("------List of Serial Ports Found------")               # Log Formatting Text
    for p in ports:                                                     # For every available port
        logger.debug("%s | %s", str(p), p.hwid)                         # Log the available ports
        for a in Arduino_List:                                          # For every Arduino Specified in the main code
            if a[1] in p.hwid:                                          # Check of the Serial Number matches the Serial Number of the Port
                a[2] = p.device                                         # If it does, Set the 3rd value of the Serial Port List array to the Port location
                logger.info("Port %s is %s ", p.device, a[0])           # Log the connections made

    logger.info("------Matches Made------")                             # Log formatting text
    for a in Arduino_List:
        if a[2] != "":                                                  # If the Port location in the Arduino_List is not blank
            logger.info("%s | %s", a[0], a[2])                          # Log the Arduino name and location of the paired arduino
            
    logger.info("------Matches NOT Made------")                         # Log formatting text
    for a in Arduino_List:
        if a[2] == "":                                                  # If the Port location in the Arduino_List is blank
            logger.info("%s was not found", a[0])                       # Log the Arduino name as not found
            
    logger.info("-----------------------------")                        # Log formatting text
###################################################################         
def list_available_ports():                                         # A setup tool used to show the Name, Location, and Information of the available Serial Ports (usefull for getting the Serial Number of an Arduino)
    ports = list(serial.tools.list_ports.comports())
    print("\n------List of Serial Ports Found------")
    for p in ports:
        print (str(p) + " | " + p.hwid + " | " + p.device)       
###################################################################  
def Start_Serial(port):                                             # Start-Up a serial interface
    logger = logging.get_logger("Start_Serial()")                   # Create Logger object for this function
    logger.debug("Starting Serial port")

    port.dtr = False                                                # Force Disable the Port
    time.sleep(0.022)                                               # Pause (VERY IMPORTANT)
    port.dtr = True                                                 # Force re-enable the Port (Forcing the port to restart allows us to not reboot the arduino every time we re-connect)

    
    while (True):
        serial = port.readline()                                    # Continue to read the output of the Serial Port,
        logger.debug("Reply from serial port: %s", str(serial)[2:-5])
        if (str(serial).find("Serial Connection is Ready")):        # Until the Arduino says it is ready to Communicate
            break                                                   # At which point, Stop reading the Serial Port
###################################################################
class Create_Serial(serial.Serial):                                                 # Create Serial Object with custom Methods (Custom)

    def get_data(self): 
        logger = logging.get_logger("get_data()")                                   # Create Logger object for this function
        try:    
            logger.debug("Writing   \"0\"  to Arduino")
            self.write(b'0')                                                        # Write a '0' bit to the Arduino to say "Send me data"
            start_time = time.time()                                                # Set timer for wait amount
            wait_max = 0.5                                                          # Wait up to 0.5 Seconds for arduino to reply (CHANGE THIS VALUE WITH CARE)
            while(True):            
                if(self.inWaiting()>0):                                             # Wait for Arduino to post to Serial Port
                    data = str(self.readline())                                     # Read reply as String
                    if "ERROR" in data:
                        logger.warning("Reply from Arduino: %s", data[2:-5])
                    else:
                        logger.debug("Reply from Arduino: %s", data[2:-5])
                    return(data[2:-5])                                              # Return the data
                if(time.time() >= start_time + wait_max):
                    logger.warning("TIMEOUT - Arduino did not reply in time")
                    return("ERROR")                                        # Returns TIMEOUT if arduino didn't reply in time
        except:
            logger.warning("Serial Communication Error")
            return ("ERROR")

                
    def send_command(self, command):
        logger = logging.get_logger("send_command()")
        try:
            logger.debug("Sending   \"1\"  to arduino")
            self.write(b'1')                                            # Write a '1' bit to tell the Arduino "I want to send a Command"
            time.sleep(0.022)           
            if(self.inWaiting()>0):                                     # Wait for Arduino to post to serial
                verification = self.readline()                          # Read the Serial line 
                if (str(verification).find("OK")):                      # Check that "OK" verification is in the String reply from Arduino.
                    logger.debug("Receieved \"OK\" from Arduino")
                    for i in range(0,len(str(command))):                # For the length of the Command String
                        self.write(str(command)[i].encode())            # Write the i'th character of the String to the Serial port
                    self.write(b'~')                                    # Once the entire string has been written, Write a '~' to the Serial Port as an end-command character (can use any Character, Just change in Arduino code)
                    start_time = time.time()                            # Set timer for wait amount
                    wait_max = 0.5                                      # Wait up to 0.5 Seconds for arduino to reply (CHANGE THIS VALUE WITH CARE)           
                    while(True):
                        if(self.inWaiting()>0):                         # Check if Arduino Wrote anything       
                            data = str(self.readline())                 # Read the Data Arduino Wrote
                            if "ERROR" in data:
                                logger.warning("Reply from Arduino: %s", data[2:-5])
                            else:
                                logger.debug("Reply from Arduino: %s", data[2:-5])
                            return(data[2:-5])
                        if(time.time() >= start_time + wait_max):       # If wait_max exceeded
                            logger.warning("TIMEOUT - Arduino did not reply in time")
                            return("ERROR")                    # Return "TIMEOUT" instead of the data (This allows the program to move on if an arduino has issues)
        except:
            logger.warning("Serial Communication Error")
            return ("ERROR")
                
                            
    def test_command(self):       
        logger = logging.get_logger("test_command()")     
        try:
            logger.debug("Writing   \"2\"  to Arduino")
            self.write(b"2")                                            # Third command
            start_time = time.time()
            wait_max = 0.5
            while(True):
                if(self.inWaiting()>0):                                 # Wait for Arduino to post to Serial Port
                    reply = str(self.readline())                        # Read reply as String
                    if "ERROR" in reply:
                        logger.warning("Reply from Arduino: \"%s\"", reply[2:-5])
                    else:
                        logger.debug("Reply from Arduino: \"%s\"", reply[2:-5])
                    return(reply[2:-5])                                       # Return the reply from Arduino
                if(time.time() >= start_time + wait_max):
                    logger.warning("TIMEOUT - Arduino did not reply in time")
                    return("ERROR")
        except:
            logger.warning("Serial Communication Error")
            return ("ERROR")
###################################################################
class start_serial_connections():


    def __init__(self):
        logger = logging.get_logger("start_serial_connections()")
        Match_Arduinos()                                                # Locate Arduinos based on Serial Number
        i = 0
        logger.info("--- Creating Serial Objects ---")
        for a in Arduino_List:
            if Arduino_List[i][2] != "":                                # if Match_Arduino found the arduino
                logger.debug("--- creating %s", a[0])
                exec (f"self.{a[0]} = Create_Serial('{a[2]}', 9600)")   # Create Serial Objects for each Arduino in the list
            i += 1
        logger.info("--- Starting Serial objects ---")
        i = 0
        for a in Arduino_List:
            if Arduino_List[i][2] != "":                                # if Match_Arduino found the arduino
                logger.debug("--- starting %s", a[0])
                exec (f"Start_Serial(self.{a[0]})")                     # Start Each Serial Interface
            i += 1


    def reconnect_all(self):
        logger = logging.get_logger("reconnect_all()")
        logger.warning("Reconnecting all Arduinos")
        self.__init__()


    def reconnect(self, arduino_name):
        logger = logging.get_logger("reconnect()--------")
        logger.warning("Running reconnect attempt for %s", arduino_name)
        logger.debug("Attempting test command for %s", arduino_name)
        if eval(f"self.{arduino_name}.test_command()") == "Test Command Reply":
            logger.warning("Port for %s is functioning properly, no reconnect needed", arduino_name)
            return (True)
        logger.debug("Test Command failed, reconnecting for %s", arduino_name)
        try:
            if  eval(f"self.{arduino_name}.is_open") == True:
                exec(f"self.{arduino_name}.close()")
        except:
            None
        
        try:
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                for a in Arduino_List:
                    if a[0] == arduino_name:
                        if a[1] in p.hwid:
                            if a[2] != p.device:
                                a[2] = p.device
                                logger.warning("Port location for %s has been changed to %s", arduino_name, a[2])

            i = 0
            for a in Arduino_List:
                if Arduino_List[i][2] != "" and Arduino_List[i][0] == arduino_name:
                    exec (f"self.{a[0]} = Create_Serial('{a[2]}', 9600)")
                    exec (f"Start_Serial(self.{a[0]})")
                    logger.debug("Re-connect Successful")
                    return (True)
                i += 1
            logger.warning("Re-connect Failed")
            return (False)

        except:
            logger.warning("Re-connect Failed")
            return (False)
###################################################################

#if __name__ == '__main__':
#    match_Arduinos()