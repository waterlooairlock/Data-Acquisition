# 
# This library is created as an API between the Python
# script and the Arduinos for the WatLock Design project
#


import time
import LoggingSetup as logging  #noqa
import serial
import serial.tools.list_ports


Arduino_List = [] # [English Name, Serial #, Port]
logger = logging.get_logger("Arduino Setup")

max_wait_time = .05
global_baud_rate = 9600
standard_sleep_time = 0.022 * (9600/global_baud_rate)

test_command_reply = "Test Command Reply"

###################################################################
def Match_Arduinos(output_log_level = "info"):
    logger = logging.get_logger("Match_Arduinos()")                     # Create Logger object for this function
    ports = list(serial.tools.list_ports.comports())                    # Creates list of Available Serial Ports on the System
    exec(f'logger.{output_log_level}("------List of Serial Ports Found------")')               # Log Formatting Text
    for p in ports:                                                     # For every available port
        logger.debug("%s | %s", str(p), p.hwid)                         # Log the available ports
        for a in Arduino_List:                                          # For every Arduino Specified in the main code
            if f"SER={a[1]}" in p.hwid:                                          # Check of the Serial Number matches the Serial Number of the Port
                a[2] = p.device                                         # If it does, Set the 3rd value of the Serial Port List array to the Port location
                exec(f'logger.{output_log_level}("Port %s is %s ", p.device, a[0])')           # Log the connections made

    exec(f'logger.{output_log_level}("------Matches Made------")')                            # Log formatting text
    for a in Arduino_List:
        if a[2] != "":                                                  # If the Port location in the Arduino_List is not blank
            exec(f'logger.{output_log_level}("%s | %s", a[0], a[2])')                          # Log the Arduino name and location of the paired arduino
            
    exec(f'logger.{output_log_level}("------Matches NOT Made------")')                         # Log formatting text
    for a in Arduino_List:
        if a[2] == "":                                                  # If the Port location in the Arduino_List is blank
            exec(f'logger.{output_log_level}("%s was not found", a[0])')                       # Log the Arduino name as not found
            
    exec(f'logger.{output_log_level}("-----------------------------")')                        # Log formatting text
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

    port.serial.dtr = False                                                # Force Disable the Port
    time.sleep(0.022)                                               # Pause (VERY IMPORTANT)
    port.serial.dtr = True                                                 # Force re-enable the Port (Forcing the port to restart allows us to not reboot the arduino every time we re-connect)

    port.serial.write(b'0')                                                # Send initial bit to force the serial port on MKR1000 to start

    
    while (True):
        serial = port.serial.readline()                                    # Continue to read the output of the Serial Port,
        logger.debug("Reply from serial port: %s", str(serial)[2:-5])
        if (str(serial)[2:-5] == "Serial Connection is Ready" or str(serial)[2:-5] == test_command_reply):        # Until the Arduino says it is ready to Communicate
            break                                                   # At which point, Stop reading the Serial Port
        port.serial.write(b'2')
###################################################################
class Create_Serial():                                                 # Create Serial Object with custom Methods (Custom)

    def __init__(self, name, port, baud):
        self.connected = False
        self.__name__ = name
        try:
            self.serial = serial.Serial(port, baud)
            self.connected = True
        except:
            None

    def check_if_connected(self):
        if self.connected == True:
            return True
        else:
            return "ERROR: Arduino is not connected"

    def get_data(self):
        logger = logging.get_logger("get_data()")                                   # Create Logger object for this function

        reply = self.check_if_connected()
        if reply != True:
            logger.debug("Arduino is not Connected")
            return reply

        try:    
            logger.debug("Writing   \"0\"  to Arduino")
            self.serial.write(b'0')                                                        # Write a '0' bit to the Arduino to say "Send me data"
            start_time = time.time()                                                # Set timer for wait amount
            while(True):            
                if(self.serial.inWaiting()>0):                                             # Wait for Arduino to post to Serial Port
                    data = str(self.serial.readline())                                     # Read reply as String
                    if "ERROR" in data:
                        logger.warning("Reply from Arduino: %s", data[2:-5])
                    else:
                        logger.debug("Reply from Arduino: %s", data[2:-5])
                    return data[2:-5]                                               # Return the data
                if(time.time() >= start_time + max_wait_time):
                    logger.warning("TIMEOUT - Arduino did not reply in time")
                    return "ERROR: TIMEOUT"                                       # Returns TIMEOUT if arduino didn't reply in time
        except:
            logger.warning("Serial Communication Error")
            return "ERROR: Serial Communication Error"

                
    def send_command(self, command):
        logger = logging.get_logger("send_command()")

        reply = self.check_if_connected()
        if reply != True:
            logger.debug("Arduino is not Connected")
            return reply

        command_string = command + "~"
        try:
            logger.debug("Sending   \"1\"  to arduino")
            self.serial.write(b'1')                                            # Write a '1' bit to tell the Arduino "I want to send a Command"
            time.sleep(standard_sleep_time)           
            if(self.serial.inWaiting()>0):                                     # Wait for Arduino to post to serial
                verification = self.serial.readline()                          # Read the Serial line 
                if (str(verification).find("OK")):                      # Check that "OK" verification is in the String reply from Arduino.
                    logger.debug("Receieved \"OK\" from Arduino")
                    self.serial.write(command_string.encode())
                    start_time = time.time()                            # Set timer for wait amount
                    while(True):
                        if(self.serial.inWaiting()>0):                         # Check if Arduino Wrote anything       
                            data = str(self.serial.readline())                 # Read the Data Arduino Wrote
                            if "ERROR" in data:
                                logger.warning("Reply from Arduino: %s", data[2:-5])
                            else:
                                logger.debug("Reply from Arduino: %s", data[2:-5])
                            return data[2:-5]
                        if(time.time() >= start_time + max_wait_time):       # If max_wait_time exceeded
                            logger.warning("TIMEOUT - Arduino did not reply in time")
                            return"ERROR: TIMEOUT"                    # Return "TIMEOUT" instead of the data (This allows the program to move on if an arduino has issues)
        except:
            logger.warning("Serial Communication Error")
            return "ERROR: Serial Communication Error"
                
                            
    def test_command(self):
        logger = logging.get_logger("test_command()")

        reply = self.check_if_connected()
        if reply != True:
            logger.debug("Arduino is not Connected")
            return reply
       
        try:
            logger.debug("Writing   \"2\"  to Arduino")
            self.serial.write(b"2")                                            # Third command
            start_time = time.time()
            while(True):
                if(self.serial.inWaiting()>0):                                 # Wait for Arduino to post to Serial Port
                    reply = str(self.serial.readline())                        # Read reply as String
                    if "ERROR" in reply:
                        logger.warning("Reply from Arduino: \"%s\"", reply[2:-5])
                    else:
                        logger.debug("Reply from Arduino: \"%s\"", reply[2:-5])
                    return reply[2:-5]                                       # Return the reply from Arduino
                if(time.time() >= start_time + max_wait_time):
                    logger.warning("TIMEOUT - Arduino did not reply in time")
                    return"ERROR: TIMEOUT"
        except:
            logger.warning("Serial Communication Error")
            return "ERROR: Serial Communication Error"


    def check_connection(self):
        logger = logging.get_logger("check_connection()")                     # Create Logger object for this function
        logger.debug("Checking connection for %s", self.__name__)

        for a in Arduino_List:
            if a[0] == self.__name__:
                old_port = a[2]
                serial_num = a[1]
        
                ports = serial.tools.list_ports.comports()
                for p in ports:
                    logger.debug("%s | %s", str(p), p.hwid)
                    if f"SER={serial_num}" in p.hwid :
                        a[2] = p.device
                        exec(f'logger.debug("Port %s is %s ", p.device, a[0])')

                if a[2] != old_port:
                    if a[2] == "":
                        self.connected = False
                        logger.warning("%s has disconnected", self.__name__)
                    else:
                        logger.info("The port for %s has updated/changed", self.__name__)
                        logger.info("Connecting to %s", self.__name__)

                        logger.debug("--- creating %s", self.__name__)
                        self.__init__

                        logger.debug("--- starting %s", self.__name__)
                        exec (f"Start_Serial(self)")


    def reconnect(self):
        logger = logging.get_logger("reconnect()--------")
        logger.debug("Running reconnect attempt for %s", self.__name__)
        try:
            if  self.serial.is_open == True:
                self.serial.close()
        except:
            logger.debug("Arduino is not connected")
            return False
        
        try:
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                for a in Arduino_List:
                    if a[0] == self.__name__:
                        if ("SER:"+a[1]) in p.hwid:
                            if a[2] != p.device:
                                a[2] = p.device
                                logger.warning("Port location for %s has been changed to %s", a[0], a[2])
            i = 0
            for a in Arduino_List:
                if Arduino_List[i][2] != "" and Arduino_List[i][0] == self.__name__:
                    self.serial = serial.Serial(a[2], global_baud_rate)
                    Start_Serial(self)
                    logger.debug("Re-connect Successful")
                    return True
                i += 1
            logger.warning("Re-connect Failed")
            return False

        except:
            raise
            logger.warning("Re-connect Failed")
            return False

###################################################################
class initialize_serial_connections():


    def __init__(self, baud_rate=global_baud_rate):
        logger = logging.get_logger("start_serial_connections()")

        global global_baud_rate
        global standard_sleep_time

        if baud_rate is not global_baud_rate:
            global_baud_rate = baud_rate
            standard_sleep_time = 0.022 * (9600/global_baud_rate)
        
        Match_Arduinos()                                                # Locate Arduinos based on Serial Number

        i = 0
        logger.info("--- Creating Serial Objects ---")
        for a in Arduino_List:
            logger.debug("--- creating %s", a[0])
            exec (f"self.{a[0]} = Create_Serial('{a[0]}','{a[2]}', {baud_rate})")   # Create Serial Objects for each Arduino in the list    
            i += 1
        logger.info("--- Starting Serial objects ---")
        i = 0
        for a in Arduino_List:
            if Arduino_List[i][2] != "":                                # if Match_Arduino found the arduino
                logger.debug("--- starting %s", a[0])
                exec (f"Start_Serial(self.{a[0]})")                     # Start Each Serial Interface
            i += 1


    def check_connections(self):
        logger = logging.get_logger("check_connections()")                     # Create Logger object for this function
        logger.debug("##### Checking Serial Ports #####")

        old_Arduino_List = [("","","")] * len(Arduino_List)

        for i in range(0, len(Arduino_List)):
            old_Arduino_List[i] = Arduino_List[i].copy()
            Arduino_List[i][2] = ""
        
        Match_Arduinos("debug")

        for i in range(0, len(Arduino_List)):

            logger.debug("Checking %s", Arduino_List[i][0])

            if Arduino_List[i] != old_Arduino_List[i]:
                if Arduino_List[i][2] == "":
                    #exec(f"del self.{Arduino_List[i][0]}")
                    exec(f"self.{Arduino_List[i][0]}.connected = False")
                    print(eval(f"self.{Arduino_List[i][0]}.connected"))
                    logger.warning("%s has disconnected", Arduino_List[i][0])
                else:
                    logger.info("The port for %s has updated/changed", Arduino_List[i][0])
                    logger.info("Connecting to %s", Arduino_List[i][0])

                    logger.debug("--- creating %s", Arduino_List[i][0])
                    exec (f"self.{Arduino_List[i][0]} = Create_Serial({Arduino_List[i][0]},'{Arduino_List[i][2]}', {global_baud_rate})")   # Create Serial Objects for each Arduino in the list

                    logger.debug("--- starting %s", Arduino_List[i][0])
                    exec (f"Start_Serial(self.{Arduino_List[i][0]})")                     # Start Each Serial Interface
            
            if eval(f"self.{Arduino_List[i][0]}.connected"):
                try:
                    logger.debug("Checking communication of \"%s\"",Arduino_List[i][0])
                    reply_from_arduino = eval(f"self.{Arduino_List[i][0]}.test_command()")
                    if "ERROR" in reply_from_arduino:
                        logger.error("Arduino \"%s\" is not communicating properly", Arduino_List[i][0])
                        self.reconnect(Arduino_List[i][0])
                    else:
                        logger.debug("Arduino \"%s\" is communicating properly", Arduino_List[i][0])
                except:
                    logger.debug("Arduino \"%s\" was not connected",Arduino_List[i][0])


    def reconnect_all(self):
        logger = logging.get_logger("reconnect_all()")                     # Create Logger object for this function
        logger.debug("Reconnecting all Arduinos")
        for a in Arduino_List:
            exec(f"self.{a[0]}.reconnect()")


###################################################################

if __name__ == '__main__':
    list_available_ports()