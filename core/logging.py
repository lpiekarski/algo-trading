import os
import logging

__all__ = ["init_logging", "TempFileLogger"]

console_handler = None


def init_logging():
    global console_handler
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.NOTSET)

    logging.getLogger("split_file_reader").setLevel(logging.INFO)

    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_level = logging.getLevelName(log_level)

    # console logging
    console_formatter = logging.Formatter("%(message)s")
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


class TempFileLogger:

    def __init__(self, path, level="INFO"):
        self.path = path
        self.level = level
        self.handler = None
        self.other_handlers = None

    def __enter__(self):
        root_logger = logging.getLogger()
        self.other_handlers = root_logger.handlers.copy()
        for handler in self.other_handlers:
            root_logger.removeHandler(handler)
        file_formatter = logging.Formatter(
            "%(asctime)s [%(process)d:%(thread)d] %(pathname)s:%(funcName)s:%(lineno)d [%(levelname)s] %(message)s")
        self.handler = logging.FileHandler(self.path)
        self.handler.setFormatter(file_formatter)
        self.handler.setLevel(self.level)
        root_logger.addHandler(self.handler)

    def __exit__(self, exc_type, exc_val, exc_tb):
        root_logger = logging.getLogger()
        root_logger.removeHandler(self.handler)
        for handler in self.other_handlers:
            root_logger.addHandler(handler)
