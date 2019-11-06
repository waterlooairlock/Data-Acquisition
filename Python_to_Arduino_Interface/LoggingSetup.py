import time
import logging


def get_logger(name):
    log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s   %(filename)25s | ln:%(lineno)d'
    logging.basicConfig(level=logging.DEBUG,        # Change Log Level for RunLog.log File
                        format=log_format,
                        filename='RunLog.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)                  # Change Log Level for Terminal
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)

logger = get_logger("Setup")
logger.info("PROGRAM START: Time: " + str(time.localtime()))