"""
This file contains utility functions for logging.
"""
import logging


def create_logger(name: str, level: logging = logging.DEBUG) -> logging.Logger:
    """
    Create a new logger for a file to use.

    Args:
        name (str): Name for the logger.
        level (logging._Level): Minimum logging level.

    Returns:
        logging.Logger: The logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
