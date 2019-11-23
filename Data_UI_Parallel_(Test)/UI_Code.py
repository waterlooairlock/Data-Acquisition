import time                                                             # Needed for pauses in testing
import LoggingSetup as logging #noqa

logger = logging.get_logger("UI_MASTER----------------")

def master(pipe):
    while(True):
        try:
            if pipe.poll():
                text = pipe.recv()
                pipe.send("Reconnect Sensors")
                print(text)
                logger.error("Received: %s",text)
        except:
            None
        time.sleep(3)

if __name__ == "__main__":
    master(None)