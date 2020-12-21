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

## How to get started
Getting started with developing for the backend application takes a few steps:
1. Configure a Ubuntu development space. This can be a stand-alone device, A Ubuntu virtual machine, or Ubuntu in WSL.
2. Open VScode in this linux environment (VScode in WSL, or VScode over SSH)
3. Install the Python and Pylance extensions for VScode
4. Open this directory directly to allwo VScode to be configured correctly.
5. In the integrated terminal, Run:
    ```bash
    sudo bash Tools/install_mysql.sh
    ```
   This will install MySQL and start the post-install config.\
   Set the root MySQL password when prompted.
6. In the integrated terminal, Run:
    ```bash
    sudo mysql -u root -p
    ```
   Input the Root password you set in step 5.
7. When the MySQL prompt is open, enter:
    ```mysql
    source Tools/configure_mysql.sh
    ```
    This will create the needed database and user for the backend to use.
8. Try running the Backend application to see if everything worked!\
    You can do this by pressing `F5` or `Start debugging` in the Control palette, the choosing the `Backend App`.\
    \
    This runs the backend application in a test configuration, where the backend uses a fake arduino interface to log the hardware interactions. Otherwise, this runs the full backend as normal.
9. Start reading the code! See how it works, The majority is commented to help guide you through what is happening.\
    Ask your team what you should be focusing on, what you can do!\