# 
# This library is created as an API between the Python
# script and the Arduinos for the WatLock Design project
#


import time
import serial
import serial.tools.list_ports


Arduino_List = [] # [English Name, Serial #, Port]

###################################################################
def match_Arduinos ():
    ports = list(serial.tools.list_ports.comports())
    print("\n------List of Serial Ports Found------")
    for p in ports:
        print (str(p) + " | " + p.hwid)
        for a in Arduino_List:
            if a[1] in p.hwid:
                a[2] = p.device
                print ("Port " + p.device + " is " + a[0] + "\n")
    
    print("------Matches Made------")
    for a in Arduino_List:
        if a[2] != "":
            print(a[0]+ " | " + a[2])
            
    print("\n------Matches NOT Made------")
    for a in Arduino_List:
        if a[2] == "":
            print(a[0] + " was not found")
            
    print("------------------------------")
###################################################################         
def list_available_ports():
    ports = list(serial.tools.list_ports.comports())
    print("\n------List of Serial Ports Found------")
    for p in ports:
        print (str(p) + " | " + p.hwid + " | " + p.device)       
###################################################################  
def start_serial(port):
    
    port.dtr = False
    time.sleep(0.022)
    port.dtr = True
    
    while (True):
        serial = port.readline()
        print(serial)
        if (str(serial).find(" Serial Connection is ready")):
            break
###################################################################
class Arduinode(serial.Serial):
    
    def get_data(self):
        self.write(b'0')                                # Write a '0' bit to the Arduino to say "Okay, send me data"
        time.sleep(0.022)
        if(self.inWaiting()>0):                         # Wait for Arduino to post to Serial Port
            data = str(self.readline())                 # Read reply as String
            return(data)                                # Return the data
    
    def send_command(self, command):
        self.write(b'1')                                # Write a '1' bit to tell the Arduino "I want to send a Command"
        time.sleep(0.022)
        if(self.inWaiting()>0):                         # Wait for Arduino to post to serial
            verification = self.readline()              # Read the Serial line 
            #print (verification)                        # Print Serial for Debugging
            if (str(verification).find("OK")):          # Check that "OK" is in the String reply from Arduino
                for i in range(0,len(str(command))):    # For the length of the Command String
                    self.write(str(command)[i].encode())# Write the i'th character of the String to the Serial port
                self.write(b'~')                        # Once the entire string has been written, Write a '~' to the Serial Port as an end-command character (can use any Character, Just change in Arduino code)
                time.sleep(0.022)
                if(self.inWaiting()>0):                 # Wait for Arduino to send a reply in the Serial port
                    reply = str(self.readline())        # Read reply as String
                    return(reply)                       # Return the Reply
                
    def other_command(self):
        self.write(b"2")                                # Third command
        time.sleep(0.022)
        if(self.inWaiting()>0):                         # Wait for Arduino to post to Serial Port
            reply = str(self.readline())                # Read reply as String
            return(reply)                               # Retunr the reply from Arduino
            

#if __name__ == '__main__':
#    match_Arduinos()