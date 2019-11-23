
#include <Wire.h>
#include <ArduinoUniqueID.h>
#include <SparkFun_MS5803_I2C.h> // Click here to get the library: http://librarymanager/All#SparkFun_MS5803-14BA


const int baud_rate = 9600;
const float pause = .022 * (9600/baud_rate);

MS5803 sensor(ADDRESS_HIGH);

//---------------------------------------------------------------------------------------------------------------------------------
//Global String Arrays
const int Command_Limit = 40;                           //Limit of the length of the String Command inputs

const int data_array_size = 100;                         //Maximum size for Data String to be return to Python (can be increased as needed)
char data_array[data_array_size + 1];                   //Character Array for Data return (using a Character array is more stable than a String, and Character Arrays cannot be easily passed through function calls)

const int command_return_size = 50;                     //Maximum size for Reply String From Command parsing
char command_return_array[command_return_size + 1];     //Character Array for Command Parsing Reply


//Global Specific Variables
double pressure_baseline;

const int pressure_data_size = 40;
char pressure_data_array[pressure_data_size+1];

const int temperature_data_size = 40;
char temperature_data_array[pressure_data_size+1];


//---------------------------------------------------------------------------------------------------------------------------------
// Arduino Specific Variables

// int door_state = 0;                                  // 0 = closed, 1 = open, 2 = closing/opening



//---------------------------------------------------------------------------------------------------------------------------------
//Setup Serial port and tell python that Arduino is ready

void setup() {
  Serial.begin(baud_rate);                                   //Initialize serial port at 9600 bps (This speed can be increased by using standard values, but also update the value in the Serial Object Creation calls of the main code)
  Serial.println("Serial Connection is Ready");         //Send "System Ready" message to Serial Port to inform Python that it is ready to receive Commands
  specific_setup();
}
//---------------------------------------------------------------------------------------------------------------------------------





//#################################################################################################################################
//SPACE FOR ARDUINO SPECIFIC FUNCTIONS

void specific_setup(){

  Wire.begin();
  sensor.reset();
  sensor.begin();

  pressure_baseline = sensor.getPressure(ADC_4096);
}


void get_pressure(){
  double pressure_abs = sensor.getPressure(ADC_4096);
  String pressure_data = "Pressure: " + String(pressure_abs);
  //String pressure_data = "Test Pressure";
  pressure_data.toCharArray(pressure_data_array, pressure_data_size+1);
}

void get_temperature(){
  float temperature_c = sensor.getTemperature(CELSIUS, ADC_512);
  String temperature_data = "Temperature: " + String(temperature_c);
  //String temperature_data = "Test Temperature";
  temperature_data.toCharArray(temperature_data_array, temperature_data_size+1);
}

double read_pressure(){
  return sensor.getPressure(ADC_4096);
}

void start_depressurization(){

}


//#################################################################################################################################






//#################################################################################################################################
//MAIN PARSING FUNCTIONS

void constant_checks(){


                                                                                /*
                                                                                Stuff that needs to run constantly...

                                                                                For example, if you receive a command to close the door, the function "close_door()" would turn the motor on and set variable "door_closing" to TRUE.
                                                                                In this function, you would put:

                                                                                  if(door_closing == TRUE && door_closed == TRUE){
                                                                                    stop_door();
                                                                                  }

                                                                                This way, it can continue to run other processes as the door is closeing and doesn't stop communicating for the time the door is closing.
                                                                                */
}



//Get Data Command
void get_data(){
  get_pressure();
  get_temperature();

  strcpy(data_array,pressure_data_array);
  strcat(data_array," | ");
  strcat(data_array,temperature_data_array);
}



//Parse Text Command
void parse_command(String command){
    String command_return = "";
    if (command  == "Test Command"){                                            //This is an example text parsing system, but anything can be used to parse the 'Command' input
      command_return = "Test Command received";                                 //Store the text Reply in the command_return variable
    }
    else if (command == "Raw Pressure"){
      command_return = String(sensor.getPressure(ADC_4096));
    }
    else if (command == "Raw Temperature Celsius"){
      command_return = String(sensor.getTemperature(CELSIUS,ADC_512));
    }
    else if (command == "Depressurize"){
      start_depressurization();
    }
    else if (command == "Pressurize"){
      
    }
    else {
      command_return = "Command not recognized";
    }

    command_return.toCharArray(command_return_array, command_return_size+1);    //Convert Text Reply String into Character Array and store Globally
}



//#################################################################################################################################







//#################################################################################################################################
//MAIN LOOP (Should not be edited unless adding new low-level command support)

void loop() {

  data_array[0] = '\0';                                    //Set first character of the Character arrays to the end-string character (functionally empties the string)
  command_return_array[0] = '\0';

  constant_checks();

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
          Serial.println("OK");                         //Reply "OK" to Python to confirm command
          
          delay(pause);                                 //Necessary Pause          

          parse_command(Serial.readStringUntil('~'));                       //Call the parse_command() function
          Serial.println(command_return_array);         //Send reply string back to Python
       }
       //------------------------------------------



       //------------------------------------------
       //Extra command for example purposes
       
       if (inByte == '2'){
         char return_array[] = "Test Command Reply";
         Serial.println(return_array);          //String to send back to Python Script (replace with data string)
       }
       //------------------------------------------


       //------------------------------------------
       // Output the processor serial #
       if (inByte == '#'){
         UniqueIDdump(Serial);
       }
       //------------------------------------------
  }  
  
}  
//#################################################################################################################################
