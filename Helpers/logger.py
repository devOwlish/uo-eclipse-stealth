"""
    Logger module
"""
import sys
from loguru import logger


class Logger:
    """
    Loguru wrapper, more sinks to be added
    """
    _instance = None

    @staticmethod
    def get() -> object:
        """Returns configured loguru object

        Returns:
            object: loguru logger
        """
        if not Logger._instance:
            log_format = ("<level>{level: <5}</level> | "
                          "<cyan>{name: ^15}</cyan>-><cyan>{function: ^15}</cyan> | "
                          "<level>{message}</level>")

            logger_config = {
                "handlers": [
                    {"sink": sys.stdout, "format": log_format, "backtrace": True}
                ],
            }

            logger.configure(**logger_config)
            Logger._instance = logger
            Logger._instance.info("Logger initialized")

        return Logger._instance


