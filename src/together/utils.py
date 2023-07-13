import logging
import sys
from typing import Optional


# Setup logging
def get_logger(
    name: str,
    logger: Optional[logging.Logger] = None,
    log_level: str = "WARNING",
) -> logging.Logger:
    if logger is None:
        logger = logging.getLogger(name)
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            handlers=[logging.StreamHandler(sys.stdout)],
        )

        logger.setLevel(log_level)

    return logger


def exit_1(logger: logging.Logger) -> None:
    logger.critical("Exiting with code 1...")
    sys.exit(1)
