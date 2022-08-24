import time
from datetime import datetime, timedelta

from commons.string import BREAK

start_time = time.time()

def command_success(LOGGER):
    log_command_resolution(LOGGER, "SUCCESS")

def command_failure(LOGGER):
    log_command_resolution(LOGGER, "FAILURE")

def log_command_resolution(LOGGER, status):
    end_time = time.time()
    delta = timedelta(seconds=end_time - start_time)
    LOGGER.info(f"{BREAK}")
    LOGGER.info(f"COMMAND {status}")
    LOGGER.info(f"{BREAK}")
    LOGGER.info(f"Total time: {str(delta)}")
    LOGGER.info(f"Finished at: {datetime.fromtimestamp(end_time).strftime('%Y-%m-%dT%H:%M:%S')}")
    LOGGER.info(f"{BREAK}")