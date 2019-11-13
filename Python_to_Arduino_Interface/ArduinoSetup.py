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

data_bit = b'0'
command_bit = b'1'
test_bit = b'2'
unique_id_bit = b'#'
test_command_reply = "Test Command Reply"

###################################################################
def Match_Arduinos(Arduinos, output_log_level = "info"):
    logger = logging.get_logger("Match_Arduinos()")                     # Create Logger object for this function
    ports = list(serial.tools.list_ports.comports())                    # Creates list of Available Serial Ports on the System
    logger.debug("------List of Serial Ports Found------")              # Log Formatting Text
    for p in ports:                                                     # For every available port
        if "Arduino" in str(p):
            logger.debug("Arduino found at %s", p.device)
            verified = False
            for a in Arduino_List:
                if a[2] == p.device and eval(f"Arduinos.{a[0]}.connected"):
                    exec(f"Arduinos.{a[0]}.serial.write(unique_id_bit)")
                    serial_return = eval(f"Arduinos.{a[0]}.serial.readline")
                    if serial_return == a[1]:
                        logger.debug("Port %s already defined for %s", p.device, )
                        verified = True
                    else:
                        exec(f"Arduinos.{a[0]}.serial.close")
                        exec(f"Arduinos.{a[0]}.connected = False")
            if not verified:
                _serial = serial.Serial(p.device, global_baud_rate)
                Start_Serial(_serial)
                _serial.write(unique_id_bit)
                paired = False
                for i in range(50):
                    serial_return = str(_serial.readline())
                    logger.debug("Reported ID is: %s", str(serial_return)[2:-5])
                    if ("UniqueID: " in serial_return[2:-5]):
                        for a in Arduino_List:
                            if a[1] in serial_return:
                                logger.debug("%s paired to %s", p.device, a[0])
                                a[2] = p.device
                                _serial.close()
                                paired = True
                                break
                    if paired:
                        break
                    _serial.write(unique_id_bit)

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
def Start_Serial(port):                                             # Start-Up a serial interface
    logger = logging.get_logger("Start_Serial()")                   # Create Logger object for this function
    logger.debug("Starting Serial port")

    port.dtr = False                                                # Force Disable the Port
    time.sleep(0.022)                                               # Pause (VERY IMPORTANT)
    port.dtr = True                                                 # Force re-enable the Port (Forcing the port to restart allows us to not reboot the arduino every time we re-connect)

    port.write(data_bit)                                                # Send initial bit to force the serial port on MKR1000 to start

    
    for i in range(50):
        serial = port.readline()                                    # Continue to read the output of the Serial Port,
        logger.debug("Reply from serial port: %s", str(serial)[2:-5])
        if (str(serial)[2:-5] == "Serial Connection is Ready" or str(serial)[2:-5] == test_command_reply):        # Until the Arduino says it is ready to Communicate
            return True                                                   # At which point, Stop reading the Serial Port
        port.write(test_bit)
    
    logger.warning("Arduino did not reply properly")
    return False
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
            self.serial.write(data_bit)                                                        # Write a '0' bit to the Arduino to say "Send me data"
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
            logger.warning("%s Serial Communication issue, Serial disconnected", self.__name__)
            self.connected = False
            try:
                self.serial.close()
            except:
                logger.debug("%s Serial disconnect failed", self.__name__)
            return "ERROR: Serial Communication issue"

                
    def send_command(self, command):
        logger = logging.get_logger("send_command()")

        reply = self.check_if_connected()
        if reply != True:
            logger.debug("Arduino is not Connected")
            return reply

        command_string = command + "~"
        try:
            logger.debug("Sending   \"1\"  to arduino")
            self.serial.write(command_bit)                                            # Write a '1' bit to tell the Arduino "I want to send a Command"
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
            logger.warning("%s Serial Communication issue, Serial disconnected", self.__name__)
            self.connected = False
            try:
                self.serial.close()
            except:
                logger.debug("%s Serial disconnect failed", self.__name__)
            return "ERROR: Serial Communication issue"
                
                            
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
            logger.warning("%s Serial Communication issue, Serial disconnected", self.__name__)
            self.connected = False
            try:
                self.serial.close()
            except:
                logger.debug("%s Serial disconnect failed", self.__name__)
            return "ERROR: Serial Communication issue"


    def check_connection(self):
        logger = logging.get_logger("check_connection()")                     # Create Logger object for this function
        logger.debug("Checking connection for %s", self.__name__)

        if (reply := self.check_if_connected()) != True:
            logger.debug("Arduino is not Connected")
            return False

        try:
            self.serial.write(test_bit)
            if str(self.serial.readline())[2:-5] == test_command_reply:
                self.serial.write(unique_id_bit)
                for a in Arduino_List:
                    if a[0] == self.__name__:
                        if a[1] in str(self.serial.readline()):
                            logger.debug("%s communcating properly and Unique ID verified", self.__name__)
                            return True
                        else:
                            logger.debug("Unique ID for %s didn't match, Serial disconnected", self.__name__)
                            self.connected = False
                            self.serial.close()
                            a[2] = ""
                            return False
            else:
                logger.debug("%s is not communcating properly, Serial disconnected", self.__name__)
                self.connected = False
                try:
                    self.serial.close()
                except:
                    logger.debug("Failed to properly close serial port")
                return False
        except:
            logger.warning("%s Serial Communication issue, Serial disconnected", self.__name__)
            self.connected = False
            try:
                self.serial.close()
            except:
                logger.debug("%s Serial disconnect failed", self.__name__)
            return False


    def reconnect(self):
        logger = logging.get_logger("reconnect()--------")
        logger.debug("Running reconnect attempt for %s", self.__name__)
        if self.connected:
            try:
                if  self.serial.is_open == True:
                    self.serial.close()
            except:
                logger.debug("%s is not connected", self.__name__)
                return False
        
        try:
            for a in Arduino_List:
                if a[0] == self.__name__:
                    a[2] = ""
                ports = list(serial.tools.list_ports.comports())
            found = False
            for p in ports:
                if "Arduino" in str(p) and found == False:
                    paired = False
                    for a in Arduino_List:
                        if a[2] == p.device:
                            paired = True
                    for a in Arduino_List:
                        if a[0] == self.__name__ and not paired:
                            _serial = serial.Serial(p.device,global_baud_rate)
                            Start_Serial(_serial)
                            _serial.write(unique_id_bit)
                            if  a[1] in str(_serial.readline()):
                                a[2] = p.device
                                found = True
                            _serial.close()

            for i, a in enumerate(Arduino_List):
                if Arduino_List[i][2] != "" and Arduino_List[i][0] == self.__name__:
                    self.serial = serial.Serial(a[2], global_baud_rate)
                    Start_Serial(self.serial)
                    self.connected = True
                    logger.debug("Re-connect Successful")
                    return True
            logger.warning("%s Re-connect Failed", self.__name__)
            return False

        except:
            raise
            logger.warning("%s Re-connect Failed", self.__name__)
            return False

###################################################################
class initialize_serial_connections():

    def __init__(self, baud_rate=global_baud_rate):
        logger = logging.get_logger("start_serial_connections()")

        global global_baud_rate

        if baud_rate is not global_baud_rate:
            global_baud_rate = baud_rate
        
        Match_Arduinos(self)                                                # Locate Arduinos based on Serial Number

        logger.info("--- Creating Serial Objects ---")
        
        for i, a in enumerate(Arduino_List):
            logger.debug("--- creating %s", a[0])
            exec (f"self.{a[0]} = Create_Serial('{a[0]}','{a[2]}', {baud_rate})")   # Create Serial Objects for each Arduino in the list    

        logger.info("--- Starting Serial objects ---")

        for i, a in enumerate(Arduino_List):
            if Arduino_List[i][2] != "":                                # if Match_Arduino found the arduino
                logger.debug("--- starting %s", a[0])
                exec (f"Start_Serial(self.{a[0]}.serial)")                     # Start Each Serial Interface
            i += 1


    def check_all_connections(self):
        logger = logging.get_logger("check_connections()")                     # Create Logger object for this function
        logger.debug("##### Checking Serial Ports #####")
        all = True
        for a in Arduino_List:
            if not eval(f"self.{a[0]}.check_connection()"):
                all = False
        return all


    def reconnect_all(self):
        logger = logging.get_logger("reconnect_all()")                     # Create Logger object for this function
        logger.debug("Reconnecting all Arduinos")
        for a in Arduino_List:
            a[2] = ""
        success = True
        for a in Arduino_List:
            if eval(f"self.{a[0]}.reconnect()") != True:
                success = False
        return success
###################################################################       
def list_available_ports():                                         # A setup tool used to show the Name, Location, and Information of the available Serial Ports (usefull for getting the Serial Number of an Arduino)
    logger = logging.get_logger("######## List Ports ########")
    ports = list(serial.tools.list_ports.comports())                    # Creates list of Available Serial Ports on the System
    for p in ports:                                                     # For every available port
        if "Arduino" in str(p):
            _serial = serial.Serial(p.device, global_baud_rate)
            Start_Serial(_serial)
            _serial.write(unique_id_bit)
            serial_return = str(_serial.readline())
            #print (str(p) + " | " + serial_return[2:-5] + " | " + p.hwid)
            logger.info("%s | %s | %s", str(p), serial_return[2:-5], p.hwid)
            _serial.close()
###################################################################

if __name__ == '__main__':
    print("\n--- ARDUINOS ---")
    list_available_ports()
