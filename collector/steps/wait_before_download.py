import datetime
from time import sleep
from commons.timing import step
import logging

LOGGER = logging.getLogger(__name__)

@step
def wait_before_download(skip_wait=None, *args, **kwargs):
    if skip_wait:
        LOGGER.info("Skipping.")
        return
    LOGGER.info("Waiting for the correct time to download the data")
    time = datetime.datetime.now()
    sleep_time_in_sec = 3600 - (time.minute * 60 + time.second)
    LOGGER.info(f"Sleeping for a total of {sleep_time_in_sec} seconds.")
    while sleep_time_in_sec > 0:
        if sleep_time_in_sec < 60:
            sleep(sleep_time_in_sec)
        else:
            sleep(60)
            sleep_time_in_sec -= 60
            LOGGER.info(f"\t\t{sleep_time_in_sec} seconds left.")
    LOGGER.info(f"Sleep is complete.")
