"""
    Logger module
"""
import sys
from loguru import logger


class Logger:
    """
    Loguru wrapper, more sinks to be added
    """

    def __init__(self) -> None:
        """
            Initialize and configure loguru
        """

        log_format = ("<green>{time: YYYY-MM-DD HH:mm:ss}</green> | "
                      "<level>{level: <5}</level> | "
                      "<cyan>{name: ^15}</cyan>-><cyan>{function: ^15}</cyan> | "
                      "<level>{message}</level>")

        logger_config = {
            "handlers": [
                {"sink": sys.stdout, "format": log_format, "backtrace": True}
            ],
        }

        logger.configure(**logger_config)

        self._logger = logger

    def get(self) -> object:
        """Returns configured loguru object

        Returns:
            object: loguru logger
        """
        return self._logger
