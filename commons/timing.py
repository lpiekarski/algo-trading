import time

start_time = time.time()

def command_success(LOGGER):
    LOGGER.info(f"\tSUCCESS in {(time.time() - start_time)} seconds")

def command_failure(LOGGER):
    LOGGER.error(f"\tFAILURE in {(time.time() - start_time)} seconds")