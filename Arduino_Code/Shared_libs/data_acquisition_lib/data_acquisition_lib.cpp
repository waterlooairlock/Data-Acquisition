/**
 * @file data_acquisition_lib.cpp
 * @author Austin W. Milne (awbmilne@gmail.com)
 * @brief Library for Python to Arduino I2C interfacing.
 * @version 0.1
 * @date 2020-12-18
 * 
 * @copyright Copyright (c) 2020
 * 
 */

#include "./data_acquisition_lib.h"

namespace Watlock_Interface{
    static Stream* log_stream = nullptr;
    static sensor_list next_sensor = sensor_list::none;

    void setup_interface(Stream& _log_stream, uint8_t ID, unsigned int speed){
        Wire.begin(ID);
        Wire.setClock(speed);
        Wire.onReceive(handle_message);
        Wire.onRequest(handle_request);
        log_stream = &_log_stream;
        log_stream->print("Configured Interface: ID set to "); log_stream->println(ID);
    }

    void handle_message(int numBytes){
        log_stream->println("I2C message received");

        // Check if the message carries enough bytes to be processed
        if (numBytes < 2){
            for (int i=0; i<numBytes; i++){
                Wire.read();
            }
        }

        // Read the message into an array
        uint8_t message[numBytes] = {0};
        for (int i=0; i<numBytes && Wire.available(); i++){
            message[i] = Wire.read();
        }

        // Limit the range to the enum size
        message[0] = (message[0] <= 2) ? message[0] : 0;

        // Cast to enum and handle cases
        switch( static_cast<message_type>(message[0]) ){
            // Call Command Function
            case message_type::command:
                log_stream->print("Calling command function: Code "); log_stream->println(message[0]);
                handle_command(message[0], sizeof(message)-1, message+1);
                break;
            // Set next_sensor for data request
            case message_type::read_sensor:
                message[1] = (message[1] <= 5) ? message[1] : 0;
                next_sensor = static_cast<sensor_list>(message[1]);
                log_stream->print("Set next sensor to read: Sensor "); log_stream->println(message[1]);
                break;
            default:
                return;
        }
    }

    void handle_request(){
        float output = 0;
        switch(next_sensor){
            case sensor_list::_1:
                output = get_sensor_1();
            case sensor_list::_2:
                output = get_sensor_2();
            case sensor_list::_3:
                output = get_sensor_3();
            case sensor_list::_4:
                output = get_sensor_4();
            case sensor_list::_5:
                output = get_sensor_5();
            default:
                output = 0;
        }

        Wire.write((uint8_t*)&output, sizeof(output));
    }

    /**
     * @brief Get Data for Sensor #1
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @return float 
     */
    float get_sensor_1(){
        return 0;
    };

    /**
     * @brief Get Data for Sensor #2
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @return float 
     */
    float get_sensor_2(){
        return 0;
    };

    /**
     * @brief Get Data for Sensor #3
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @return float 
     */
    float get_sensor_3(){
        return 0;
    };

    /**
     * @brief Get Data for Sensor #4
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @return float 
     */
    float get_sensor_4(){
        return 0;
    };

    /**
     * @brief Get Data for Sensor #5
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @return float 
     */
    float get_sensor_5(){
        return 0;
    };

    /**
     * @brief Run command on Arduino
     * 
     * @param code The command code sent from the server
     */
    void handle_command(uint8_t code, uint8_t length, uint8_t data[]){
        return;
    }
}