import datetime
from time import sleep
from commons.timing import step
import logging

LOGGER = logging.getLogger(__name__)

@step
def wait_before_download(**kwargs):
    LOGGER.info("Waiting for the correct time to download the data")
    while True:
        time = datetime.datetime.now()
        sleep_time_in_sec = 3600 - (time.minute * 60 + time.second)
        LOGGER.info(f"\t\t{sleep_time_in_sec} seconds left.")
        if sleep_time_in_sec <= 60:
            sleep(sleep_time_in_sec)
            LOGGER.info(f"Sleep is complete.")
            break
        else:
            sleep(60)
