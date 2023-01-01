import logging
import time
import os
from datetime import datetime, timedelta
from functools import wraps
from commons.exceptions import NonInterruptingError, CommandFailedError
from commons.string import BOLD, BREAK, ENDC, FAIL, OKBLUE, OKCYAN, OKGREEN, UNDERLINE, WARNING, break_padded

LOGGER = logging.getLogger(__name__)
start_time = time.time()

steps = []
execution_id = 0


class Step:
    def __init__(self, name, module, callback, invisible):
        self.name = name
        self.module = module
        self.start = None
        self.end = None
        self.result = None
        self.invisible = invisible
        self.execution_id = None
        self.id = None
        self.callback = callback
        self.resolved = False

    def start_execution(self, execution_id):
        LOGGER.debug(
            f"Starting execution of step '{self.name}', execution_id={execution_id}")
        self.start = time.time()
        self.execution_id = execution_id

    def resolve(self, status):
        LOGGER.debug(
            f"Step {self.name}, execution_id={execution_id} resolved with status '{status}'")
        self.result = status
        self.end = time.time()
        self.resolved = True

    def set_id(self, id):
        self.id = id

    def get_log_func(self, logger):
        return logger.debug if self.invisible else logger.info

    def log_title(self, logger):
        log = self.get_log_func(logger)
        log("")
        log(
            f"{BOLD}---{ENDC} {OKCYAN}{self.name}{ENDC} {BOLD}@{ENDC} {OKCYAN}{self.module}{ENDC} [{self.id}] {BOLD}---{ENDC}")


def step(step_func):
    @wraps(step_func)
    def wrap(*args, **kwargs):
        if os.getenv("UNIT_TESTING") == "True":
            return step_func(*args, **kwargs)
        global execution_id
        s = steps[execution_id]
        try:
            s.log_title(logging.getLogger(step_func.__module__))
            s.start_execution(execution_id)
            result = step_func(*args, **kwargs)
            s.resolve('SUCCESS')
            return result
        except Exception as e:
            s.resolve('FAILURE')
            LOGGER.error('Step failed:', exc_info=e)
            if not isinstance(e, NonInterruptingError):
                raise e
        finally:
            execution_id += 1
    wrap.pure = step_func
    return wrap


def initialize_steps(step_list):
    for step_func in step_list:
        s = Step(
            name=step_func.__name__.replace('_', ' '),
            module=step_func.__module__,
            invisible=hasattr(step_func, 'invisible') and step_func.invisible,
            callback=step_func
        )
        steps.append(s)


def log_execution_plan(logger, module, name):
    logger.info(BOLD + OKBLUE + break_padded(f"{module}:{name}") + ENDC)
    logger.info("")
    logger.info(f"{BOLD}{BREAK}{ENDC}")
    logger.info("\tExecution plan:")
    logger.info("")
    for s in steps:
        s.get_log_func(logger)(f"\t\t{s.name} @ {s.module}")


def set_step_ids(logger):
    visible_step_count = len([s for s in steps if not s.invisible])
    current_step_id = 1
    for s in steps:
        if s.invisible:
            s.set_id(f'hidden {current_step_id}/{visible_step_count}')
        else:
            s.set_id(f'{current_step_id}/{visible_step_count}')
            current_step_id += 1
    logger.info(f"{BOLD}{BREAK}{ENDC}")


def execute_steps(logger, args, kwargs):
    previous_step_result = dict()
    result_status = 'SUCCESS'
    for s in steps:
        if previous_step_result is not None and isinstance(
                previous_step_result, dict):
            kwargs.update(**previous_step_result)
        previous_step_result = s.callback(*args, **kwargs)
        if s.result == 'FAILURE':
            result_status = 'FAILURE'
        logger.debug(f"Step completed, kwargs:")
        logger.debug(f"\t{kwargs}")
    return result_status


def subcommand(step_list):
    def inner(subcommand_func):
        @wraps(subcommand_func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(subcommand_func.__module__)
            initialize_steps(step_list)
            log_execution_plan(
                logger, subcommand_func.__module__, subcommand_func.__name__)
            set_step_ids(logger)
            status = 'FAILURE'
            try:
                status = execute_steps(logger, args, kwargs)
                subcommand_func(*args, **kwargs)
            except Exception as e:
                logger.error('Executing steps failed with following exception:', exc_info=e)
            log_command_resolution(logger, status)
            if status == 'FAILURE':
                raise CommandFailedError(f"Command ended with status '{status}'")
        return wrapper
    return inner


def command_success(logger):
    log_command_resolution(logger, "SUCCESS")


def command_failure(logger):
    log_command_resolution(logger, "FAILURE")


def log_command_resolution(logger, status):
    end_time = time.time()
    logger.info(f"")
    logger.info(f"{BOLD}{BREAK}{ENDC}")
    logger.info(f"Results:")
    logger.info(f"")
    for s in steps:
        log_func = logger.debug if s.invisible else logger.info
        if not s.resolved:
            log_func(f"{s.name + ' ' :.<52} SKIPPED")
        else:
            log_func(
                f"{s.name + ' ' :.<52} {color_status(s.result)} [{s.end - s.start :.5f} s]")
    logger.info(f"{BOLD}{BREAK}{ENDC}")
    logger.info(f"COMMAND {color_status(status)}")
    logger.info(f"{BOLD}{BREAK}{ENDC}")
    logger.info(f"Total time: {end_time - start_time :.5f} s")
    logger.info(
        f"Finished at: {datetime.fromtimestamp(end_time).strftime('%Y-%m-%dT%H:%M:%S')}")
    logger.info(f"{BOLD}{BREAK}{ENDC}")


def color_status(status):
    if status == 'SUCCESS':
        return f"{OKGREEN}{status}{ENDC}"
    if status == 'FAILURE':
        return f"{FAIL}{status}{ENDC}"
    return f"{WARNING}{status}{ENDC}"
