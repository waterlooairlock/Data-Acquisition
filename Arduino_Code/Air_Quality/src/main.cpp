/**
 * @file main.cpp
 * @author Justin Llanos (jllanos@uwaterloo.ca)
 * @brief Template Source file for Python controlled Arduino
 * @version 0.1
 * @date 2021-07-09
 * 
 * @copyright Copyright (c) 2020
 */

#include <Arduino.h>
#include "data_acquisition_lib.h"
#include <SoftwareSerial.h>

#define CO2_RX_PIN 5
#define CO2_TX_PIN 6
#define  O2_RX_PIN 7
#define  O2_TX_PIN 8

SoftwareSerial co2_mx_board( CO2_RX_PIN, CO2_TX_PIN );
SoftwareSerial  o2_mx_board(  O2_RX_PIN,  O2_TX_PIN );

uint16_t co2_comp = 0, o2_comp = 0;

void get_mx_board_val( SoftwareSerial*, uint16_t& );

void setup(){
    Serial.begin(9600);
    Watlock_Interface::setup_interface(Serial, 13);

    pinMode(CO2_RX_PIN,  INPUT);
    pinMode(CO2_TX_PIN, OUTPUT);
    pinMode( O2_RX_PIN,  INPUT);
    pinMode( O2_TX_PIN, OUTPUT);

    co2_mx_board.begin(9600);
    o2_mx_board.begin(9600);

    // set polling mode
    co2_mx_board.println("K 2");
    o2_mx_board.println("K 2");
}

void loop() {
    get_mx_board_val(&co2_mx_board, co2_comp);
    get_mx_board_val( &o2_mx_board,  o2_comp);

    Serial.print("CO2 composittion: "); Serial.println(co2_comp);
    Serial.print( "O2 composittion: "); Serial.println( o2_comp);

    delay(1000); // pause 1 sec
}

void get_mx_board_val( SoftwareSerial* mx_board, uint16_t& val_hold ) {
    while ( mx_board->read() != -1 )
        /* Serial.println("I hope this doesn't lock the board") */; // clear input buffer
    mx_board->listen();
    mx_board->println("Z");
    char response_code = mx_board->peek();
    switch (response_code) {
    case 'Z':
        val_hold = 0;
        mx_board->read(); // clear 'Z'
        mx_board->read(); // clear ' '
        for ( uint8_t i = 0; i < 5; ++i ) {
            val_hold *= 10;
            val_hold += ( mx_board->read() - '0' );
        }
        break;
    case 'E': // error
        for ( char c = mx_board->read(); c != -1; c = mx_board->read() )
            Serial.print(c); // log error message as is for now
        break;
    default:
        Serial.print("Unexpected response: "); Serial.println(mx_board->read());
        break;
    }
}

/**
 * @brief Sensor 1 configured as CO2 sensor
 * 
 * @return Carbon Dioxide composition in ppm
 */
float get_sensor_1(){
    return (float) co2_comp;
}

/**
 * @brief Sensor 2 configured as O2 sensor
 * 
 * @return Oxygen composition in ppm
 */
float get_sensor_2(){
    return (float) o2_comp;
}
