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

/**
 * @brief Watlock Server Interface
 * 
 * This is the namespace for all the Watlock Server Interface
 * functions.
 * 
 * Setup as a namespace with closed local variables.
 * This could have been a class instead, but would have created
 * complex function pointer garbage with the I2C function handling.
 * 
 */
namespace Watlock_Interface{
    // Specified Integer values of message types (aligns with code in python backend)
    enum class message_type{
    none            = 0,
    command         = 1,
    };

    // Specified Integer values of sensors (aligns with code in python backend)
    enum class sensor_list{
        none    = 0,
        _1      = 1,
        _2      = 2,
        _3      = 3,
        _4      = 4,
        _5      = 5,
    };

    // This functions have the GCC compiler attribute "weak".
    // This means they can be overwritten by a definition somewhere else.
    // The intention behind this being that you can define the function in
    // the main arduino code and this library will use that version instead
    // of this one. The GCC weak attribute allows this to happen without
    // throwing nasty errors with the Compiler and Linker. 
    float get_sensor_1()                                              __attribute__((weak));
    float get_sensor_2()                                              __attribute__((weak));
    float get_sensor_3()                                              __attribute__((weak));
    float get_sensor_4()                                              __attribute__((weak));
    float get_sensor_5()                                              __attribute__((weak));
    void handle_command(uint8_t code, uint8_t length, uint8_t data[]) __attribute__((weak));

    // Function for setting up the Interface with the python backend
    void setup_interface(Stream& _log_stream, uint8_t ID, unsigned int speed = 100000);

    // INTERNAL FUNCTIONS, DO NOT USE IN MAIN CODE
    void handle_request();
    void handle_message(int numBytes);
};