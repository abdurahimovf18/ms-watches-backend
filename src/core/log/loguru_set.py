from typing import Any

from loguru import logger

from .log_settings import LOGURU_SETTINGS


def remove_default():
    logger.remove(0)


def add_application_log_settings(settings: dict[str, dict[str, Any]]):

    for name, setting in settings.items():
        logger.add(**setting)
        print(f"Logging configuration: {name} has been successfully set.")


def set_loguru_settings():
    remove_default()
    add_application_log_settings(LOGURU_SETTINGS)
