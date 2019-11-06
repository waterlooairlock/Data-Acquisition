import time
import logging


def get_logger(name):
    if not logging.getLogger(name).handlers:
        log_format = '%(asctime)s  %(name)30s : [%(levelname)s] > %(message)-65s [%(filename)-20s | ln:%(lineno)d]'
        logging.basicConfig(level=logging.INFO,        # NOTE: Change Log Level for RunLog.log File
                            format=log_format,
                            filename='RunLog.log',
                            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)                  # NOTE: Change Log Level for Terminal
        console.setFormatter(logging.Formatter(log_format))
        logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)

logger = get_logger("Setup")
logger.info("PROGRAM START: Time: " + str(time.localtime()))