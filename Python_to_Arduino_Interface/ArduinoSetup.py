# 
# This library is created as an API between the Python
# script and the Arduinos for the WatLock Design project
#


import time
import serial
import serial.tools.list_ports


Arduino_List = [] # [English Name, Serial #, Port]

###################################################################
def Match_Arduinos ():
    ports = list(serial.tools.list_ports.comports())                # Creates list of Available Serial Ports on the System
    print("\n------List of Serial Ports Found------")               # Formatting Text
    for p in ports:                                                 # For every available port
        print (str(p) + " | " + p.hwid)                             # Print the Name and the port location
        for a in Arduino_List:                                      # For every Arduino Specified in the main code
            if a[1] in p.hwid:                                      # Check of the Serial Number matches the Serial Number of the Port
                a[2] = p.device                                     # If it does, Set the 3rd value of the Serial Port List array to the Port location
                print ("Port " + p.device + " is " + a[0] + "\n")   # Print that it was found and where it was found
    
    print("------Matches Made------")                               # List valid Matches
    for a in Arduino_List:
        if a[2] != "":
            print(a[0]+ " | " + a[2])
            
    print("\n------Matches NOT Made------")                         # List Matches not made
    for a in Arduino_List:
        if a[2] == "":
            print(a[0] + " was not found")
            
    print("-----------------------------")                          # Terminal output formatting
###################################################################         
def list_available_ports():                                         # A setup tool used to show the Name, Location, and Information of the available Serial Ports (usefull for getting the Serial Number of an Arduino)
    ports = list(serial.tools.list_ports.comports())
    print("\n------List of Serial Ports Found------")
    for p in ports:
        print (str(p) + " | " + p.hwid + " | " + p.device)       
###################################################################  
def Start_Serial(port):                                             # Start-Up a serial interface
    
    port.dtr = False                                                # Force Disable the Port
    time.sleep(0.022)                                               # Pause (VERY IMPORTANT)
    port.dtr = True                                                 # Force re-enable the Port (Forcing the port to restart allows us to not reboot the arduino every time we re-connect)

    
    while (True):                                                   
        serial = port.readline()                                    # Continue to read the output of the Serial Port,
        print(serial)                                               
        if (str(serial).find("Serial Connection is Ready")):        # Until the Arduino says it is ready to Communicate
            break                                                   # At which point, Stop reading the Serial Port
###################################################################
class Create_Serial(serial.Serial):                                 # Create Serial Object with custom Methods (Custom)


    def get_data(self):         
        self.write(b'0')                                            # Write a '0' bit to the Arduino to say "Send me data"
        start_time = time.time()                                    # Set timer for wait amount
        wait_max = 0.5                                              # Wait up to 0.5 Seconds for arduino to reply (CHANGE THIS VALUE WITH CARE)
        while(True):
            if(self.inWaiting()>0):                                 # Wait for Arduino to post to Serial Port
                data = str(self.readline())                         # Read reply as String
                return(data)                                        # Return the data
            if(time.time() >= start_time + wait_max):
                return("TIMEOUT")                                   # Returns TIMEOUT if arduino didn't reply in time

                
    def send_command(self, command):            
        self.write(b'1')                                            # Write a '1' bit to tell the Arduino "I want to send a Command"
        time.sleep(0.022)           
        if(self.inWaiting()>0):                                     # Wait for Arduino to post to serial
            verification = self.readline()                          # Read the Serial line 
            #print (verification)                                   
            if (str(verification).find("OK")):                      # Check that "OK" verification is in the String reply from Arduino.
                for i in range(0,len(str(command))):                # For the length of the Command String
                    self.write(str(command)[i].encode())            # Write the i'th character of the String to the Serial port
                self.write(b'~')                                    # Once the entire string has been written, Write a '~' to the Serial Port as an end-command character (can use any Character, Just change in Arduino code)
                start_time = time.time()                            # Set timer for wait amount
                wait_max = 0.5                                      # Wait up to 0.5 Seconds for arduino to reply (CHANGE THIS VALUE WITH CARE)           
                while(True):
                    if(self.inWaiting()>0):                         # Check if Arduino Wrote anything       
                        data = str(self.readline())                 # Read the Data Arduino Wrote
                        return(data)
                    if(time.time() >= start_time + wait_max):       # If wait_max exceeded
                        return("TIMEOUT")                           # Return "TIMEOUT" instead of the data (This allows the program to move on if an arduino has issues)

                            
    def other_command(self):            
        self.write(b"2")                                            # Third command
        start_time = time.time()
        wait_max = 0.5
        while(True):
            if(self.inWaiting()>0):                                     # Wait for Arduino to post to Serial Port
                reply = str(self.readline())                            # Read reply as String
                return(reply)                                           # Return the reply from Arduino
            if(time.time() >= start_time + wait_max):
                return("TIMEOUT")

#if __name__ == '__main__':
#    match_Arduinos()