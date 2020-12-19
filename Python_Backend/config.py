
import threading
import mysql.connector

import Custom_Logging as logging
from Watlock_Interface import arduino_interface

logger = logging.get_logger("Process Handler")

arduinos = arduino_interface(1)
thread_lock = threading.Lock()
threads = []
db = mysql.connector.connect(
    host="localhost",
    user="sql_user",
    password="sql_password",
    database="airlock"
)

if (db):
    logger.debug("Database Connection Succeded")
    db.autocommit(True)
else:
    logger.error("Database Connection Failed!")

