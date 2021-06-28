/**
 * @file main.cpp
 * @author Justin Llanos (jllanos@uwaterloo.ca)
 * @brief Main source file for controlling RTD temperature sensors
 * @version 0.1
 * @date 2021-06-27
 */

#include <arduino.h>
#include "data_acquisition_lib.h"
#include <Adafruit_MAX31865.h>

// SPI Pins - can be set to any digital output pins
#define  SPI_CS 10
#define  SPI_DI 11
#define  SPI_DO 12
#define SPI_CLK 13

// Resistance of RTD at 0C
#define RTD_NOM 100.0f
// Resistance of reference resistor
#define    RREF 430.0f

Adafruit_MAX31865 sensor(SPI_CS, SPI_DI, SPI_DO, SPI_CLK);

float temperature_hold = 0.0f;

void setup() {
    // TODO - choose the a configuration for the sensor
    sensor.begin(MAX31865_4WIRE);

    Serial.begin(9600);
    Watlock_Interface::setup_interface(Serial, 12);
}

void loop() {
    temperature_hold = sensor.temperature(RTD_NOM, RREF);
    Serial.print("Temperature reading: "); Serial.println(temperature_hold);

    delay(1000); // wait 1 second between measurements
}

/**
 * @brief Sensor 1 Configured as RTD Temperature Sensor
 * 
 * @return The temperature in Degrees Celsius
 */
float Watlock_Interface::get_sensor_1() {
    return temperature_hold;
}
