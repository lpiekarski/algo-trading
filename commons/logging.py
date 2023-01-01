import os
import logging

__all__ = ["init_logging"]


def init_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.NOTSET)

    logging.getLogger("split_file_reader").setLevel(logging.INFO)

    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_level = logging.getLevelName(log_level)

    # console logging
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # file logging
    log_file = os.getenv("LOG_FILE")
    if log_file is not None:
        if os.getenv("LOG_LEVEL") is None:
            file_log_level = os.getenv("FILE_LOG_LEVEL", "INFO")
            file_log_level = logging.getLevelName(file_log_level)
        else:
            file_log_level = log_level
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_formatter = logging.Formatter(
            "%(asctime)s [%(process)d:%(thread)d] %(pathname)s:%(funcName)s:%(lineno)d [%(levelname)s] %(message)s")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(file_log_level)
        root_logger.addHandler(file_handler)

    logger = logging.getLogger(__name__)
    logger.debug(f"Logging initialized {root_logger.handlers}")
