import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def log_info(message: str, **kwargs):

    logger.info(
        json.dumps({
            "level": "INFO",
            "message": message,
            **kwargs
        })
    )


def log_error(message: str, **kwargs):

    logger.error(
        json.dumps({
            "level": "ERROR",
            "message": message,
            **kwargs
        })
    )