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

#define VALVE1_PIN 1
#define VALVE2_PIN 2
#define VALVE3_PIN 3
#define VALVE4_PIN 4
#define VALVE5_PIN 5

#define VALVE_CLOSE LOW
#define VALVE_OPEN HIGH

#define NUM_VALVES 5

const pin_size_t VALVE_PIN[NUM_VALVES] {
    VALVE1_PIN,
    VALVE2_PIN,
    VALVE3_PIN,
    VALVE4_PIN,
    VALVE5_PIN
};

void setup() {
    Serial.begin(9600);
    Watlock_Interface::setup_interface(Serial, 14);

    for (uint8_t i = 0;  i < NUM_VALVES; ++i)
        pinMode(VALVE_PIN[i], OUTPUT);
}

void loop() {}

// Overwrite the command handing function
void handle_command(uint8_t code, uint8_t length, uint8_t data[]){
    if (!data) {
        Serial.println("[ERROR] No valve pin received");
        return;
    }

    switch(code) {
        case 0: // close
            digitalWrite(VALVE_PIN[data[0] - 1], VALVE_CLOSE);
            Serial.print("Closing valve "); Serial.println(data[0]);
            break;
        case 1: // open
            digitalWrite(VALVE_PIN[data[0] - 1], VALVE_OPEN);
            Serial.print("Opening valve "); Serial.println(data[0]);
            break;
        default:
            Serial.println("[ERROR] Received unrecognized command");
            break;
    }
}