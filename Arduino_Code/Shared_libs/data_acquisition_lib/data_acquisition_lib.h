/**
 * @file data_acquisition_lib.h
 * @author Austin W. Milne (awbmilne@gmail.com)
 * @brief Library for Python to Arduino I2C interfacing.
 * @version 0.1
 * @date 2020-12-18
 * 
 * @copyright Copyright (c) 2020
 * 
 */

#include <Wire.h>

namespace Watlock_Interface{
    enum class message_type{
    none            = 0,
    read_sensor     = 1,
    command         = 2,
    };

    enum class sensor_list{
        none    = 0,
        _1      = 1,
        _2      = 2,
        _3      = 3,
        _4      = 4,
        _5      = 5,
    };

    float get_sensor_1()                                              __attribute__((weak));
    float get_sensor_2()                                              __attribute__((weak));
    float get_sensor_3()                                              __attribute__((weak));
    float get_sensor_4()                                              __attribute__((weak));
    float get_sensor_5()                                              __attribute__((weak));
    void handle_command(uint8_t code, uint8_t length, uint8_t data[]) __attribute__((weak));

    void setup_interface(Stream& _log_stream, uint8_t ID, unsigned int speed = 100000);
    void handle_request();
    void handle_message(int numBytes);
};