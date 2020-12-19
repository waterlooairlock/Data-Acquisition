/**
 * Template Project for Control Arduinos in the WatLock Airlock
 * ────────────────────────────────────────────────────────────
 * This is the primary source file. Place all
 * needed code in this file. If there are multiple
 * large functions, additional source files can be #included.
 * 
 * If you need to add a library for sensor interfaces or
 * other things, place the libraries into the 'lib' directory.
 * 
 * Created on: 12/14/2020
 * Written by: Austin W. Milne (@awbmilne)
 */

#include <arduino.h>
#include "data_acquisition_lib.h"

void setup(){
    Serial.begin(9600);
    Watlock_Interface::setup_interface(Serial, 69);
}

void loop(){
    Serial.println("");
}

float get_sensor_1(){
    float test_val = 1.2345;
    return test_val;
}

void handle_command(uint8_t code, uint8_t length, uint8_t data[]){
    switch(code){
        case 1:
            // Do something when the code is 1
            break;
        case 2:
            // Do something when the code is 2
            break;
        break;
            return; // Handle outlying cases by doing nothing
    }
}