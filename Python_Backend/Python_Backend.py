#!/usr/bin/env python

from config import *
from data_collection import data_collection

logger = logging.get_logger("Process Handler")

if __name__ =="__main__":
    # Create list of threads
    threads = [
               data_collection("Data_Collection"),
              ]
    # Start all the threads
    for thread in threads:
        logger.info("Starting Thread: " + thread.name)
        thread.start()
    # Join threads
    for thread in threads:
        thread.join()
    # Log exit of controller if Threads ends
    logger.error("All threads ended")
