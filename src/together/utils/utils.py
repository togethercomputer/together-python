import logging
import sys
from typing import Optional

class TogetherLogFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%m-%d-%Y %H:%M:%S")
        return formatter.format(record)

# Setup logging
def get_logger(
    name: str,
    logger: Optional[logging.Logger] = None,
    log_level: str = "WARNING",
) -> logging.Logger:
    if logger is None:
        logger = logging.getLogger(name)

        logger.setLevel(log_level)

        lg_format = logging.StreamHandler()
        lg_format.setLevel(logging.DEBUG)
        lg_format.setFormatter(TogetherLogFormatter())

        logger.addHandler(lg_format)

    return logger


def exit_1(logger: logging.Logger) -> None:
    logger.critical("Exiting with code 1")
    sys.exit(1)
