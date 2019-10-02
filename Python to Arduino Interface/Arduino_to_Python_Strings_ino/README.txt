Austin W. Milne | Fall 2019

This code is to be used as a basic outline for communication 
between a Python script running on Debian Linux and a set of Arduinos.

On the Python side, here is what you need to do:
--------------------------------------------------------------------------

1.  Install the pySerial library on the system running the python script:

    [In system terminal]
    >>> pip install pySerial

2.  Place the ArduinoSetup.py file into the same folder as the main script

3.  import ArduinoSetup (I prefer to import as Arduino for easier reference)

    [In python code]
    >>> import ArduinoSetup as Arduino

4.  Add your connections to the list of Arduinos by using the command below:

    >>> Arduino.Arduino_List.append(["SERIAL_PORT_NAME", "SERIAL_#_OF_ARDUINO", ""])

5.  Call the match_Arduinos() function to locate the serial ports for each 
    Arduino's Serial Number:

    >>> Arduino.match_Arduinos()

6.  Run these two for loops to create the Serial Port objects using the names
    in Arduino_List, and to initialize each Serial Object Communication:

    >>> for a in Arduino.Arduino_List:
    >>>     if Arduino.Arduino_List[a][2] != "":
    >>>         exec (a[0] + " = Arduino.Create_Serial('" + a[2] + "', 9600)")
    >>>
    >>> for a in Arduino.Arduino_List:
    >>>     if Arduino.Arduino_List[a][2] != "":
    >>>         exec ("Arduino.Start_Serial(" + a[0] + ")") 

    Note: To change the data transfer rate, change the '9600' to another standard value:
          [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200]
          using a Higher Baud rate can increase data transfer speeds, but may cause issues 
          with communication timing

7.  At this point, there should be an object for each serial connection with the arduinos in the list

    Note: There is no validation check to see if all/any of the connections worked.
          There is a terminal output showing the successful and failed connections.
          To manually check the connections, check if the 3rd array value for each 
          item in the Arduino_List is blank or filled. If it is blank,
          Match_Arduinos failed to find that arduino and will not not attempt to 
          make a connection (this shows in the for loops stated above).

8.  Finally, you can use the object methods to communicate with the arduinos!

    A.  To get data from the Arduino, the get_data() method returns a data text string
        of data from the arduino:

        >>> Data_Ouput = Arduino_Name.get_data()

    B.  To send a Text Command to the Arduino, use the send_command() method.
        Send the command as a text string argument in the method and the return
        will be the reply from the arduino.

        >>> Command_Reply = Arduino_Name.send_command("Command_To_Send")

        Note:   This command text string argument is limited to a length defined in
                in the Arduino Code. To change the limitation, refer to the 
                Arduino Code.

Extra Notes: The Arduino Interface objects are a re-statement of the serial.Serial
class defined in the pySerial library. pyLibrary must be installed on the system
running the python script. This also means that these serial objects can be used
as they normally would be with the pySerial library. They can write and read directly
without the formatting of the ArduinoSetup code. (This is not recommended as it is
far more difficult to use and has been simplified by the send_command() method).
