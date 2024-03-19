import logging
from logging.config import dictConfig
from config import LogConfig


dictConfig(LogConfig().model_dump())
logger = logging.getLogger("blue_logger")

filehandler = logging.FileHandler('blue-logger.log')
filehandler.setLevel(logging.INFO)
logger.addHandler(filehandler)

logger.setLevel(logging.INFO)
