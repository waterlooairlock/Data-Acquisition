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

#define PUMP_PIN   0
#define VALVE1_PIN 1
#define VALVE2_PIN 2
#define VALVE3_PIN 3
#define VALVE4_PIN 4
#define VALVE5_PIN 5

#define NUM_CONTROLS 6

const pin_size_t CONTROL_PINS[NUM_CONTROLS] {
    PUMP_PIN,
    VALVE1_PIN,
    VALVE2_PIN,
    VALVE3_PIN,
    VALVE4_PIN,
    VALVE5_PIN
};

void setup() {
    Serial.begin(9600);
    Watlock_Interface::setup_interface(Serial, 14);

    for (uint8_t i = 0;  i < NUM_CONTROLS; ++i)
        pinMode(CONTROL_PINS[i], OUTPUT);
}

void loop() {}

// Overwrite the command handing function
// ! Confirm high/low states
void handle_command(uint8_t code, uint8_t length, uint8_t data[]){
    if (!data) {
        Serial.println("[ERROR] No control pin received");
        return;
    }

    switch(code) {
        case 0: // "close" for valves, "off" for pump
            digitalWrite(CONTROL_PINS[data[0]], LOW);
            Serial.print("Closing valve "); Serial.println(data[0]);
            break;
        case 1: // "open" for valves, "on" for pump
            digitalWrite(CONTROL_PINS[data[0]], HIGH);
            Serial.print("Opening valve "); Serial.println(data[0]);
            break;
        default:
            Serial.println("[ERROR] Received unrecognized command");
            break;
    }
}