
import time
import logging

# This sets up a logging object to use across the Python Backend.
# Just include this unit and then use:

# logger.error("message")
# logger.warning("message")
# logger.info("message")

# for the various levels of warning in the log file.

log_path = "logs/"


def get_logger(name):
    if not logging.getLogger(name).handlers:
        log_format = '%(asctime)s  %(name)18s : %(levelname)7s > %(message)-80s [%(filename)-21s | ln:%(lineno)d]'
        logging.basicConfig(level=logging.DEBUG,        # NOTE: Change Log Level for RunLog.log File
                            format=log_format,
                            filename=log_path + 'Backend_RunLog.log',
                            filemode='w')
        console = logging.StreamHandler()
        # NOTE: Change Log Level for Terminal
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(log_format))
        logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)


logger = get_logger("Setup")
logger.info("PROGRAM START: Time: " + str(time.localtime()))
