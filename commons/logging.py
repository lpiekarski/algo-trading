import os
import logging

__all__ = ["init_logging"]


def init_logging():
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.NOTSET)

    LOG_LEVEL = os.getenv("LOG_LEVEL")
    if LOG_LEVEL is None:
        LOG_LEVEL = logging.INFO
    else:
        LOG_LEVEL = logging.getLevelName(LOG_LEVEL)

    # console logging
    consoleFormatter = logging.Formatter("[%(levelname)s] %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(consoleFormatter)
    consoleHandler.setLevel(LOG_LEVEL)
    rootLogger.addHandler(consoleHandler)

    # file logging
    LOG_FILE = os.getenv("LOG_FILE")
    if LOG_FILE is not None:
        if os.getenv("LOG_LEVEL") is None:
            FILE_LOG_LEVEL = os.getenv("FILE_LOG_LEVEL")
            if FILE_LOG_LEVEL is None:
                FILE_LOG_LEVEL = logging.INFO
            else:
                FILE_LOG_LEVEL = logging.getLevelName(FILE_LOG_LEVEL)
        else:
            FILE_LOG_LEVEL = LOG_LEVEL
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        fileFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        fileHandler = logging.FileHandler(LOG_FILE)
        fileHandler.setFormatter(fileFormatter)
        fileHandler.setLevel(FILE_LOG_LEVEL)
        rootLogger.addHandler(fileHandler)

    LOGGER = logging.getLogger(__name__)

    LOGGER.debug(f"Logging initialized {rootLogger.handlers}")