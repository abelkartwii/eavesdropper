import time
import os
import logging
from pathlib import Path

HOME_PATH = Path(__file__).parents[0]
LOG_PATH = os.path.join(HOME_PATH, "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
LOGFILE_PATH = os.path.join(LOG_PATH, "{}.log")

def current_time():
    return int(round(time.time()))

def init_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.info) # ignores debugs
    formatter = logging.Formatter("%(asctime)s: %(levelname)s %(message)s")

    file_handler = logging.FileHandler(LOGFILE_PATH.format(logger_name))
    file_handler.setLevel(logging.info)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    return logger