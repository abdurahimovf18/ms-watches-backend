import sys
from typing import Any

# Importing base settings and constants, like the BASE_DIR and DEBUG flag.
from src.core.base_settings import BASE_DIR, BaseEnvConsumer, DEBUG

# LogEnvConsumer is designed to consume environment settings related to logging.
class LogEnvConsumer(BaseEnvConsumer):
    """
    LogEnvConsumer class extends the BaseEnvConsumer class to manage logging-related environment settings.
    This class can be used to fetch and handle environment-specific logging configurations.
    """
    pass


# Default Loguru settings for different environments (Production and Debug).
LOGURU_DEFAULT_SETTINGS: dict[str, dict[str, dict[str, Any]]] = {
    # Settings for the "PRODUCTION" environment
    "PRODUCTION": {
        "file": {
            "sink": str(BASE_DIR / "logs" / "production.log"),  # File path for production logs
            "level": "INFO",  # Log level set to WARNING for production
            "rotation": "1 week",  # Rotate logs every week
            "compression": "zip",  # Compress rotated logs with zip format
            "retention": "4 weeks",  # Retain logs for 4 weeks before deletion
            "backtrace": False,  # Disable backtrace in production logs
            "diagnose": False,  # Disable diagnostic information in production logs
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # Log format
        }
    },
    # Settings for the "DEBUG" environment
    "DEBUG": {
        "file": {
            "sink": str(BASE_DIR / "logs" / "debug.log"),  # File path for debug logs
            "level": "DEBUG",  # Log level set to DEBUG for detailed output
            "rotation": "1 day",  # Rotate logs every day
            "compression": "zip",  # Compress rotated logs with gzip format
            "retention": "4 weeks",  # Retain logs for 4 weeks before deletion
            "backtrace": True,  # Enable backtrace for debugging purposes
            "diagnose": True,  # Enable diagnostic information for debugging
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} | {extra}",  # Log format for debug logs
        },
        "console": {
            "sink": sys.stdout,  # Log output to console (stdout)
            "level": "DEBUG",  # Log level for console set to DEBUG
            "backtrace": True,  # Enable backtrace in console logs
            "diagnose": True,  # Enable diagnostic information in console logs
            "colorize": True,  # Colorize console output for readability
            "format": "<level>{level}</level>\t | <cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | <white>{message}</white> | <green>{extra}</green>",  # Colorized log format
        }
    }
}


# A lambda function to retrieve the appropriate Loguru settings based on the environment (DEBUG or PRODUCTION).
@lambda func: func()
def LOGURU_SETTINGS() -> dict[str, dict[str, Any]]:
    """
    Returns the Loguru logging configuration based on the current environment.
    If DEBUG is set to True, it returns the debug-specific settings, otherwise, it returns production settings.

    Returns:
        dict: Loguru logging configuration (DEBUG or PRODUCTION settings).
    """
    if DEBUG is True:
        return LOGURU_DEFAULT_SETTINGS["DEBUG"]
    else:
        return LOGURU_DEFAULT_SETTINGS["PRODUCTION"]
