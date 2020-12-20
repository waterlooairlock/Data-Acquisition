#!/usr/bin/env python

from config import *
from data_collection import *
from command_handler import *
from command_handler.depressurization import *

main_logger = logging.get_logger("Thread Handler")

if __name__ =="__main__":
    # Create list of threads
    threads = [
        data_collection("Data_Collection"),             # Data Collection Thread
        threading.Thread(target=command_handler.run),   # Command Handler API Thread
    ]
    # Start all the threads
    for thread in threads:
        main_logger.info("Starting Thread: " + thread.name)
        thread.start()
    # Join threads
    for thread in threads:
        thread.join()
    # Log exit of controller if Threads ends
    main_logger.error("All threads ended")
