import logging
from typing import Any, Dict, Optional

import together


class TogetherLogFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: grey + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%m-%d-%Y %H:%M:%S")
        return formatter.format(record)


# Setup logging
def get_logger(
    name: str,
    logger: Optional[logging.Logger] = None,
    log_level: str = together.log_level,
) -> logging.Logger:
    if logger is None:
        logger = logging.getLogger(name)

        logger.setLevel(log_level)

        lg_format = logging.StreamHandler()
        lg_format.setLevel(logging.DEBUG)
        lg_format.setFormatter(TogetherLogFormatter())

        logger.addHandler(lg_format)

    return logger


def verify_api_key(logger: Optional[logging.Logger] = None) -> None:
    if logger is None:
        logger = get_logger(str(__name__), log_level=together.log_level)
    if together.api_key is None:
        raise together.AuthenticationError(
            "TOGETHER_API_KEY not found. Please set it as an environment variable or set it with together.api_key"
        )


def extract_time(json_obj: Dict[str, Any]) -> int:
    try:
        return int(json_obj["created_at"])
    except KeyError:
        return 0
