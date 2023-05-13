"""
Logger module for the Bumble Private Detector
🐝 We've got our eyes on those private bees 🕵️‍♂️
"""
import os
import logging
import datetime
import sys
from pathlib import Path
from logging import Formatter
import logging.handlers

# Set some variables
date_format = "%Y-%m-%d %H:%M:%S"  # Customize date format
bee_good_emoji = "\U0001F41D\U0001F50D"  # Bee + Magnifying Glass


def _colorize_log_format(log_record: logging.LogRecord) -> str:
    log_colors = {
        logging.DEBUG: "\033[0;34m",    # Blue
        logging.INFO: "\033[0;32m",     # Green
        logging.WARNING: "\033[0;33m",  # Yellow
        logging.ERROR: "\033[0;31m",    # Red
        logging.CRITICAL: "\033[1;31m",  # Bright Red
    }

    # Reset color code
    reset_color = "\033[0m"

    # Set up a basic log format
    log_format = f"[{bee_good_emoji}] {log_colors[log_record.levelno]}%(levelname)s{reset_color} %(message)s"

    return log_format


def make_logger(name: str, directory: str = "logs") -> logging.Logger:
    """
    Create a logger that will also print to console

    Parameters
    ----------
    name : str
        String to tag the logs with.
    directory : str, optional
        Folder in which to save the logs. If not specified, this function will
        use the 'LOG_PATH' environment variable if it is set;
        otherwise, it will default to 'logs'.

    Environment Variables
    ---------------------
    LOG_PRETTY : str
        Set to 'True' if you want colored log output in the console. Defaults to 'False'.
    LOG_PATH : str
        The path to the directory where the logs will be saved.
        If not set, the default log directory is used.
    LOG_LEVEL : str
        The log level for the logger. If not set, it defaults to 'INFO'.
        Available levels: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.

    Returns
    -------
    logger : logging.Logger
        The logger object configured to write logs to the
            - console
            - specified file.
    """
    # Read environment variables
    log_pretty = os.environ.get("LOG_PRETTY", "False").lower() == "True"
    log_path = os.environ.get("LOG_PATH", directory)
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    # Set log level
    log_level = logging.getLevelName(log_level.upper())
    # Set where to store the logs and make directory, if needed
    log_dir = Path(log_path)
    log_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.datetime.today().strftime("%Y-%m-%d-%H%M")
    log_file_path = log_dir / f"{today}-{name}.log"

    logger = logging.getLogger("BeeChecker")
    logger.setLevel(log_level)

    # Set up file handler
    file_handler = logging.FileHandler(log_file_path)
    logger.addHandler(file_handler)

    # Set up console handler with the custom log format
    stdout_handler = logging.StreamHandler(sys.stdout)

    # Set the log format according to the LOG_PRETTY variable
    if log_pretty:
        formatter = logging.Formatter(
            fmt=_colorize_log_format, style="%", datefmt=date_format
        )
    else:
        # Boring logs
        boring_logs = " %(levelname)s %(message)s"
        formatter = Formatter(fmt=boring_logs, datefmt=date_format)

    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    logger.info(
        f"The [{bee_good_emoji}] logs are buzzing to @{log_file_path} 💘")

    return logger