"""
Logger module for training the private detector
"""
import datetime
import os
import logging
import sys
from pathlib import Path


def make_logger(name: str, directory: str = 'logs') -> logging.Logger:
    """
    Create a logger that will also print to console

    Parameters
    ----------
    name: str
        String to tag the logs with.
    directory: str, optional
        Folder in which to save the logs. If not specified, this function will
        use the 'LOG_PATH' environment variable if it is set;
        otherwise, it will default to 'logs'.

    Environment Variables
    ---------------------
    LOG_LEVEL: str
        The log level for the logger. If not set, it defaults to 'INFO'.
        Available levels: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
    LOG_PATH: str
        The path to the directory where the logs will be saved.
        If not set, the default log directory is used.

    Returns
    -------
    logger: logging.Logger
        The logger object configured to write logs to the console and the specified file.
    """
    # Read environment variables for log level and log path
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_path = os.environ.get('LOG_PATH', directory)

    logger = logging.getLogger("BeeTeacher")
    logger.setLevel(logging.getLevelName(log_level))

    directory = Path(log_path)
    directory.mkdir(parents=True, exist_ok=True)

    today = datetime.datetime.today().strftime('%Y-%m-%d-%H%M')
    log_file_path = directory / f"{today}-{name}.log"

    # Set up file handler
    file_handler = logging.FileHandler(log_file_path)
    logger.addHandler(file_handler)

    # Also print log output to console
    stdout_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stdout_handler)

    logger.info(f'The logs will bee @: {log_file_path}')

    return logger