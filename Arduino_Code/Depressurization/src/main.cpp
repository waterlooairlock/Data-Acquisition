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
#include <SparkFun_MS5803_I2C.h> // Click here to get the library: http://librarymanager/All#SparkFun_MS5803-14BA

MS5803 sensor(ADDRESS_HIGH);
float pressure_hold = 0;
float temperature_hold = 0;

void setup(){
    sensor.reset();
    sensor.begin();

    Serial.begin(9600);
    Watlock_Interface::setup_interface(Serial, 69);
}

void loop(){
    pressure_hold = sensor.getPressure(ADC_4096);
    temperature_hold = sensor.getPressure(ADC_4096);

    delay(1000); // Pause for 1 Second
}

float Watlock_Interface::get_sensor_1(){ // Overwrite the Sensor 1 function from Watlock_Interface
    return pressure_hold;
}

float Watlock_Interface::get_sensor_2(){
    return temperature_hold;
}
