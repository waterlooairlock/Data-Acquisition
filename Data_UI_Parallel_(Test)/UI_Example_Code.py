import time                                                             # Needed for pauses in testing
import LoggingSetup as logging #noqa

logger = logging.get_logger("UI_MASTER----------------")

def master(pipe):
    while(True):
        try:
            pipe.send("Test")
            text = pipe.recv()
            print(text)
            logger.error("Received: %s",text)
        except:
            None
        time.sleep(1)

if __name__ == "__main__":
    master(None)