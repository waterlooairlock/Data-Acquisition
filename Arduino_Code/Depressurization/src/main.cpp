/**
 * @file main.cpp
 * @author Austin W. Milne (austin.milne@uwaterloo.ca)
 * @brief Primary source file for the Depressurization Arduino
 * @version 0.1
 * @date 2020-12-19
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
    Watlock_Interface::setup_interface(Serial, 11);
}

void loop(){
    pressure_hold = sensor.getPressure(ADC_4096);
    Serial.print("Pressure reading: "); Serial.println(pressure_hold);
    temperature_hold = sensor.sensor.getTemperature(CELSIUS, ADC_512);
    Serial.print("Temperature reading: "); Serial.println(temperature_hold);

    delay(1000); // Pause for 1 Second
}

/**
 * @brief Sensor 1 Configured as Pressure Sensor
 * 
 * @return float The absolute pressure in Pascals
 */
float Watlock_Interface::get_sensor_1(){ // Overwrite the Sensor 1 function from Watlock_Interface
    return pressure_hold;
}

/**
 * @brief Sensor 2 Configured as Temperature sensor
 * 
 * @return float The temperature in units of Degrees Celsius
 */
float Watlock_Interface::get_sensor_2(){ // Overwrite the Sensor 2 function from Watlock_Interface
    return temperature_hold;
}