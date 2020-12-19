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

    /**
     * @brief Set the up Server interface
     * 
     * @param _log_stream Serial object for use as Log Output (general just `Serial`)
     * @param ID The desired ID of the specific Arduino. Should be different for each Arduino, Otherwise collisions occur.
     * @param speed Optional: The interface speed for I2C, defaults to 100000
     */
    void setup_interface(Stream& _log_stream, uint8_t ID, unsigned int speed){
        Wire.begin(ID);
        Wire.setClock(speed);
        Wire.onReceive(handle_message);
        Wire.onRequest(handle_request);
        log_stream = &_log_stream;
        log_stream->print("Configured Interface: ID set to "); log_stream->println(ID);
    }

    /**
     * @brief Directly handles I2C message from the Server
     * Takes I2C commands and converts them into the necessary
     * actions on the arduino. Sends command messages to the
     * `handle_command()` function or stores the value of the
     * next sensor to be read from.
     * 
     * Only used internally, DO NOT USE
     * @param numBytes The number of bytes available over the I2C interface
     */
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
        for (int i=0; i<numBytes; i++){
            message[i] = Wire.read();
        }

        // Limit the range to the enumerator size
        message[0] = (message[0] <= 1) ? message[0] : 0;

        // Cast to enum and handle cases
        switch( static_cast<message_type>(message[0]) ){
            // Call Command Function
            case message_type::command:
                log_stream->print("Calling command function: Code "); log_stream->println(message[1]);
                handle_command(message[1], sizeof(message)-2, message+2);
                break;
            // Could have additional cases here for something other than commands to be sent over I2C
            default:
                return;
        }
    }

    /**
     * @brief Directly handles the I2C data requests
     * Handles the cases of `next_sensor` and calls the relevant
     * get function. Will default to the weak function unless
     * the function is overwritten in the project source files.
     * 
     * Only used internally, DO NOT USE
     */
    void handle_request(){
        // Read the first Byte as the Sensor Number and cast to Enumerator
        uint8_t sensor_num = Wire.read();
        sensor_num = (sensor_num <= 5) ? sensor_num : 0;
        sensor_list next_sensor = static_cast<sensor_list>(sensor_num);

        // Get the sensor reading
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
        
        // Send the data over I2C
        Wire.write((uint8_t*)&output, sizeof(output));

        // Log Information
        log_stream.print("Send sensor data: Value = "); log_stream.println(output, 6);
    }

    /**
     * @brief Get Data for Sensor #1
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @return float Sensor value 
     */
    float get_sensor_1(){
        return 0;
    };

    /**
     * @brief Get Data for Sensor #2
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @return float Sensor value
     */
    float get_sensor_2(){
        return 0;
    };

    /**
     * @brief Get Data for Sensor #3
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @return float Sensor value 
     */
    float get_sensor_3(){
        return 0;
    };

    /**
     * @brief Get Data for Sensor #4
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @return float Sensor value 
     */
    float get_sensor_4(){
        return 0;
    };

    /**
     * @brief Get Data for Sensor #5
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @return float Sensor value 
     */
    float get_sensor_5(){
        return 0;
    };

    /**
     * @brief Handle Incoming command from Server
     * This is intended as a "weak" function, It should be overwritten
     * in the main source file to get the actual data for that sensor.
     * @param code The command code sent from the server
     * @param length Length of extra data array
     * @param data Pointer to start of extra data array
     */
    void handle_command(uint8_t code, uint8_t length, uint8_t data[]){
        return;
    }
}