# Python Backend

The python backend handles interactions between the Arduino and the server.

## Tasks
The tasks of the backend include:
1. Request data from the Arduinos and store it into the Mongo database
2. Serve an API for the js frontend to call with commands
3. Forward API commands to the arduinos
4. Handle logging of actions/errors for easy troubleshooting

## How its constructed
Currently, the Backend Python file consists of 3 primary parts:
1. The `data_collection` thread
   - The `data_collection` thread contains a set of `multitimers` (found in [data_collection.py](data_collection.py))
   - Each `multitimer` calls an arduino-specific data collection function at a given time interval
   - These function send the data to the MongoDB server
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
1. First, in order to run this Python script and test it, You will need a linux environment (This is due to Linux specific packages for SMBUS/I2C), Debian based Distros are recommended (Ubuntu), though the same functionality could be achieved on other distrinutions with some script rewrites.
2. Open your IDE of choice in the Linux environment (My choice is Vscode with Ubuntu on WSL)
3. Clone this project from github and open it in your IDE
4. If you dont already have Python installed, install it now.\
    (*Preferably version 3.8+*)
5. In the same terminal, run:
    ```bash
    pip install -r /Python_Backend/Tools/requirements.txt
    ```
    or, if that doesnt work
    ```bash
    pip3 install -r /Python_Backend/Tools/requirements.txt
    ```
    This will install the needed Python packages to run the Backend App.
7. Ask someone on the electrical team for the Mongo uri. Once you have it, create a file called `secret.py`
and paste in this code:
```python
MONGOURI = '<Mongo URI>'
```
6. Try running the Backend application to see if everything worked!
    ```bash
    python --no_i2c Python_Backend/Python_Backend.py
    ```
    or
    ```bash
    python3 --no_i2c Python_Backend/Python_Backend.py
    ```
    This will run the Python Backend app with the dummy Arduino interface. This means you dont need arduino hooked up and configured to test the backend. All the simulated interactions are logged in the `Python_Backend\logs` directory. Look for the lod data there.

7. Start reading the code! See how it works, The majority is commented to help guide you through what is happening.\
    Ask your team what you should be focusing on, what you can do!\