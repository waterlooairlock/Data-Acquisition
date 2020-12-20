# Python Backend

The python backend handles interactions between the Arduino and the server.

## Tasks
The tasks of the backend include:
1. Request data from the Arduinos and store it into the MySQL Database
2. Serve an API for the js frontend to call with commands
3. Forward API commands to the arduinos
4. Handle logging of actions/errors for easy troubleshooting

## How its constructed
Currently, the Backend Python file consists of 3 primary parts:
1. The `data_collection` thread
   - The `data_collection` thread contains a set of `multitimers` (found in [data_collection.py](data_collection.py))
   - Each `multitimer` calls an arduino-specific data collection function at a given time interval
   - These function send the data to MySQL server
   - These timers repeat forever
   - Arduino interactions are made thread-safe using the `thread_lock` object

2. The `command_handler` thread
    - The `command_handler` thread hosts a Flask API on a `localhost` port (number TBD) (found in [command_handler.py](./command_handler.py))
    - The Flask API provides options for the JS frontend to send commands to the Arduinos
    - The Flask API handles API calls by forwarding messages to the Arduinos
    - Arduino interactions are made thread-safe using the `thread_lock` object

3. The `Thread Handler`, or the main thread
    - This is the thread that runs when the program is started
    - This thread creates the `data_collection` and `command_handler`
    - This thread starts the other 2 threads and waits patiently to see of they fail, In which case it logs the error (All in the [Python_Backend.py](./Python_Backend.py) file)