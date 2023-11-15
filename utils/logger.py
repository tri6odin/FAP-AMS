import logging
from logging.handlers import RotatingFileHandler
import os

from config import BACKUPS, LOG_SIZE_BYTES

# Create logger


def get_logger():
    log_directory = "./logs"
    log_file_path = os.path.join(log_directory, "logfile.log")

    # Create dir
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Config RotatingFileHandler
    handler = RotatingFileHandler(
        log_file_path,
        maxBytes=LOG_SIZE_BYTES,
        backupCount=BACKUPS
    )

    # Create a logging format with timestamps
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


# Export logger
logger = get_logger()
