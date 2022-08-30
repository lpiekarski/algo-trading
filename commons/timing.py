import logging
import time
from datetime import datetime, timedelta
from functools import wraps

from commons.exceptions import CommandInterruption
from commons.string import BOLD, BREAK, ENDC, FAIL, OKGREEN, break_padded

start_time = time.time()

steps = {}

def step(step_func):
    @wraps(step_func)
    def wrap(*args, **kwargs):
        step_name = step_func.__name__.replace('_', ' ')
        step_module = step_func.__module__
        LOGGER = logging.getLogger(step_func.__module__)
        steps[step_name]['start'] = time.time()
        LOGGER.info("")
        LOGGER.info(f"{BOLD}--- {step_name} @ {step_module} ---{ENDC}")
        try:
            result = step_func(*args, **kwargs)
            steps[step_name]['end'] = time.time()
            steps[step_name]['result'] = 'SUCCESS'
            return result
        except Exception as e:
            steps[step_name]['end'] = time.time()
            steps[step_name]['result'] = 'FAILURE'
            LOGGER.error(e, exc_info=e)
            if isinstance(e, CommandInterruption):
                raise e
    return wrap


def subcommand(step_list):
    def inner(subcommand_func):
        @wraps(subcommand_func)
        def wrapper(*args, **kwargs):
            LOGGER = logging.getLogger(subcommand_func.__module__)
            LOGGER.info(BOLD + break_padded(f"{subcommand_func.__module__}:{subcommand_func.__name__}") + ENDC)
            LOGGER.info("")
            previous_step_result = dict()

            for step_func in step_list:
                step_name = step_func.__name__.replace('_', ' ')
                steps[step_name] = {'start': None, 'end': None, 'result': None}
            for step in step_list:
                if previous_step_result is not None and isinstance(previous_step_result, dict):
                    kwargs.update(**previous_step_result)
                previous_step_result = step(*args, **kwargs)
            subcommand_func(*args, **kwargs)
            command_success(LOGGER)
        return wrapper
    return inner


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
        if summary['result'] is None:
            LOGGER.info(f"{step_name + ' ' :.<52} SKIPPED")
        else:
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