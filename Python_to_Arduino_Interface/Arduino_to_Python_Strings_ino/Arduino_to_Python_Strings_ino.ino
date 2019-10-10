/*
 This program is a basic outline of interaction between
a Python Script and an Arduino.

The get_data function will deal with getting data from the sensor/s attached to the arduino

The parse_command function will deal with calling functions created 
*/


//---------------------------------------------------------------------------------------------------------------------------------
//Global Variables
const int Command_Limit = 40;                           //Limit of the length of the String Command inputs

const int data_array_size = 50;                         //Maximum size for Data String to be return to Python (can be increased as needed)
char data_array[data_array_size + 1];                   //Character Array for Data return (using a Character array is more stable than a String, and Character Arrays cannot be easily passed through function calls)

const int command_return_size = 30;                     //Maximum size for Reply String From Command parsing
char command_return_array[command_return_size + 1];     //Character Array for Command Parsing Reply

const int other_return_size = 30;                       //Maximum size for Reply String From other function (to add new function calls, modify the ArduinoSetup and this code)
char other_return_array[other_return_size + 1];         //Character Array for the Other Function Reply

//---------------------------------------------------------------------------------------------------------------------------------
//Setup Serial port and tell python that Arduino is ready

void setup() {
  Serial.begin(9600);                                   //Initialize serial port at 9600 bps (This speed can be increased by using standard values, but also update the value in the Serial Object Creation calls of the main code)
  while (!Serial){}                                     //Wait for Serial Connection to establish (needed for stable USB interface)
  Serial.println("Serial Connection is Ready");         //Send "System Ready" message to Serial Port to inform Python that it is ready to receive Commands
  specific_setup();
}
//---------------------------------------------------------------------------------------------------------------------------------


//#################################################################################################################################
//SPACE FOR ARDUINO SPECIFIC FUNCTIONS

void specific_setup(){
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}


//#################################################################################################################################


//#################################################################################################################################
//MAIN PARSING FUNCTIONS


//Get Data Command

void get_data(){
  String data_string = "Example data : 12 Mpa : 10:12:12.345";                  //This is a temporary String variable to store the text string of the data input
  data_string.toCharArray(data_array, data_array_size+1);                       //Convert Text Reply String into Character Array and store Globally for compatability and stability (THIS LINE IS VERY IMPORTANT)
}


//Parse Text Command

void parse_command(String command){
    String command_return = "";
    if (command  == "Test Command"){                                            //This is an example text parsing system, but anything can be used to parse the 'Command' input
      command_return = "Test Command received";                                 //Store the text Reply in the command_return variable
    }
    else if (command == "LED On"){
      digitalWrite(LED_BUILTIN, HIGH);
      command_return = "Built-In LED is set to On";
    }
    else if (command == "LED Off"){
      digitalWrite(LED_BUILTIN, LOW);
      command_return = "Built-In LED is set to Off";
    }
    else {
      command_return = "Command not recognized";
    }

    command_return.toCharArray(command_return_array, command_return_size+1);    //Convert Text Reply String into Character Array and store Globally
}


//Example basic Command Outline

void other_command(){
  String data_string = "This is the return from the other command";            //Same layout as get_data()
  data_string.toCharArray(other_return_array, other_return_size+1);
}

//#################################################################################################################################


//#################################################################################################################################
//MAIN LOOP (Should not be edited unless adding new low-level command support)

void loop() {  
  
  if (Serial.available() > 0)                           //Check of there is something in the Serial port to be read  
  {  
       int inByte = Serial.read();                      //This variable stores the low level Byte command sent from python
       
       //------------------------------------------
       //Command from Python to sent senor data
       
       if (inByte == '0'){
         get_data();
         Serial.println(data_array);                    //String to send back to Python Script (replace with data string)
       }
       //------------------------------------------



       //------------------------------------------
       // Command from python to get ready to receive a String Command

       if (inByte == '1'){
          char CommandSent[Command_Limit+1];            //Reads up to Command_Limit, change to adjust limit (larger requires more ram)
          int i = 0;                                    //Set string iterator  
          Serial.println("OK");                         //Reply "OK" to Python to confirm command

          while(true){                                  //Run Infinitely
            if(Serial.available()>0){                   //If there is a value in the Serial Port
              char input = Serial.read();               //Read Character from the Serial Port
              if (input != '1' || i != 0){              //If it is either not '1' or the first value (The Serial port on the Arduino wants to read a 1 before the text string, cant figure out why, but this ignores any 1 as the first character)
                CommandSent[i] = input;                 //Place the Character into the Character array
                if (CommandSent[i] == '~'){             //If the Character pulled from the Serial Port is a '~',
                  CommandSent[i] = 0;                   //replace it with the null character value of 0 (When the Arduino creates the string from the array of characters, it stops at the null character)
                  break;                                //Since Python finished sending the command, break the While loop
                }
                i = i + 1;                              //Interate Character count
              }
            }
          }
          String command((char*)CommandSent);           //Convert the Command Array into a Command String
          parse_command(command);                       //Call the parse_command() function
          Serial.println(command_return_array);         //Send reply string back to Python
       }
       //------------------------------------------



       //------------------------------------------
       //Extra command for example purposes
       
       if (inByte == '2'){
         other_command();
         Serial.println(other_return_array);          //String to send back to Python Script (replace with data string)
       }
       //------------------------------------------
  }  
  
}  
//#################################################################################################################################
