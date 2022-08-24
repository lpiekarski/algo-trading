import time
from datetime import datetime, timedelta

from commons.string import BOLD, BREAK, ENDC, FAIL, OKGREEN

start_time = time.time()

steps = {}

def start_step(LOGGER, step_name):
    steps[step_name] = {'start': time.time(), 'end': None, 'result': None}
    LOGGER.info("")
    LOGGER.info(f"--- {step_name} ---")

def step_success(step_name):
    steps[step_name]['end'] = time.time()
    steps[step_name]['result'] = 'SUCCESS'

def step_failure(step_name):
    steps[step_name]['end'] = time.time()
    steps[step_name]['result'] = 'FAILURE'

def command_success(LOGGER):
    log_command_resolution(LOGGER, "SUCCESS")

def command_failure(LOGGER):
    log_command_resolution(LOGGER, "FAILURE")

def log_command_resolution(LOGGER, status):
    end_time = time.time()
    LOGGER.info(f"")
    LOGGER.info(f"{BOLD}{BREAK}{ENDC}")
    LOGGER.info(f"Results:")
    LOGGER.info(f"")
    for step_name, summary in steps.items():
        LOGGER.info(f"{step_name + ' ' :.<52} {color_status(summary['result'])} [{summary['end'] - summary['start'] :.5f} s]")
    LOGGER.info(f"{BOLD}{BREAK}{ENDC}")
    LOGGER.info(f"COMMAND {color_status(status)}")
    LOGGER.info(f"{BOLD}{BREAK}{ENDC}")
    LOGGER.info(f"Total time: {end_time - start_time :.5f} s")
    LOGGER.info(f"Finished at: {datetime.fromtimestamp(end_time).strftime('%Y-%m-%dT%H:%M:%S')}")
    LOGGER.info(f"{BOLD}{BREAK}{ENDC}")

def color_status(status):
    if status == 'SUCCESS':
        return f"{OKGREEN}{status}{ENDC}"
    if status == 'FAILURE':
        return f"{FAIL}{status}{ENDC}"
    return f"{BOLD}{status}{ENDC}"