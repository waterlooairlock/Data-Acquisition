/**
 * @file main.cpp
 * @author Austin W. Milne (@Awbmilne)
 * @brief Template Source file for Python controlled Arduino
 * @version 0.1
 * @date 2020-12-19
 * 
 * @copyright Copyright (c) 2020
 * 
 * This is the primary source file for the Arduino's firmware.
 * This template source shows the use of the `data_acquisition_lib`.
 * Specifically, how to setup the interface and configure sensor and
 * command handling.
 */

#include <Arduino.h>
#include "data_acquisition_lib.h"

void setup(){
    Serial.begin(9600);
    Watlock_Interface::setup_interface(Serial, 69);
}

void loop(){
    Serial.println("");
}

// Overwrite the Sensor 1 function
float get_sensor_1(){
    float test_val = 1.2345;
    return test_val;
}

// Overwrite the command handing function
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