import logging
from loans_billing_legacy.middleware.context import get_request_id


logger = logging.getLogger("api-logger")


def build_log_message(message: str) -> str:
    request_id = get_request_id()

    log_message = f"request_id={request_id} " + message

    return log_message


def info(message) -> None:
    logger.info(build_log_message(message))


def warn(message) -> None:
    logger.warn(build_log_message(message))


def error(message) -> None:
    logger.error(build_log_message(message))


def critical(message) -> None:
    logger.critical(build_log_message(message))
