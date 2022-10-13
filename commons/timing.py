import logging
import time
from datetime import datetime, timedelta
from functools import wraps

from commons.exceptions import NotInterruptingError
from commons.string import BOLD, BREAK, ENDC, FAIL, OKBLUE, OKCYAN, OKGREEN, UNDERLINE, WARNING, break_padded

start_time = time.time()

steps = {}

def step(step_func):
    @wraps(step_func)
    def wrap(*args, **kwargs):
        step_name = step_func.__name__.replace('_', ' ')
        step_module = step_func.__module__
        LOGGER = logging.getLogger(step_func.__module__)
        steps[step_name]['start'] = time.time()
        if not steps[step_name]['invisible']:
            LOGGER.info("")
            LOGGER.info(f"{BOLD}---{ENDC} {OKCYAN}{step_name}{ENDC} {BOLD}@{ENDC} {OKCYAN}{step_module}{ENDC} {BOLD}---{ENDC}")
        try:
            result = step_func(*args, **kwargs)
            steps[step_name]['end'] = time.time()
            steps[step_name]['result'] = 'SUCCESS'
            return result
        except Exception as e:
            steps[step_name]['end'] = time.time()
            steps[step_name]['result'] = 'FAILURE'
            if not isinstance(e, NotInterruptingError):
                raise e
    return wrap


def subcommand(step_list):
    def inner(subcommand_func):
        @wraps(subcommand_func)
        def wrapper(*args, **kwargs):
            LOGGER = logging.getLogger(subcommand_func.__module__)
            LOGGER.info(BOLD + OKBLUE + break_padded(f"{subcommand_func.__module__}:{subcommand_func.__name__}") + ENDC)
            LOGGER.info("")
            LOGGER.info(f"{BOLD}{BREAK}{ENDC}")
            LOGGER.info("\tExecution plan:")
            LOGGER.info("")
            previous_step_result = dict()

            for step_func in step_list:
                step_name = step_func.__name__.replace('_', ' ')
                steps[step_name] = {
                    'start': None,
                    'end': None,
                    'result': None,
                    'invisible': hasattr(step_func, 'invisible') and step_func.invisible
                }
                log_func = LOGGER.debug if steps[step_name]['invisible'] else LOGGER.info
                log_func(f"\t\t{step_name} @ {step_func.__module__}")
            LOGGER.info(f"{BOLD}{BREAK}{ENDC}")

            for step in step_list:
                if previous_step_result is not None and isinstance(previous_step_result, dict):
                    kwargs.update(**previous_step_result)
                previous_step_result = step(*args, **kwargs)
                LOGGER.debug(f"Step completed, kwargs:")
                LOGGER.debug(f"\t{kwargs}")
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
        log_func = LOGGER.debug if summary['invisible'] else LOGGER.info
        if summary['result'] is None:
            log_func(f"{step_name + ' ' :.<52} SKIPPED")
        else:
            log_func(f"{step_name + ' ' :.<52} {color_status(summary['result'])} [{summary['end'] - summary['start'] :.5f} s]")
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
    return f"{WARNING}{status}{ENDC}"