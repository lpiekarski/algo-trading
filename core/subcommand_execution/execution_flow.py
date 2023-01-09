import logging
import time
from functools import wraps

from core.exceptions import CommandFailedError
from core.steps.process_parameter import ProcessParameter
from core.subcommand_execution.step import StepStatus
from core.subcommand_execution.subcommand_executor import SubcommandExecutor

LOGGER = logging.getLogger(__name__)

subcommands_steps = dict()


def execution_flow(*step_list):
    """
    Specifies a list of functions that will be called during the execution of the subcommand. If the return value of a
    function is a dict, its keys and values are merged with the previous parameters and passed to the next function.
    :param step_list: A list of function "steps" that will be executed when this subcommand is run.
    :return: The execution flow function for the subcommand.
    """
    def inner(subcommand_func):
        @wraps(subcommand_func)
        def wrapper(*args, **kwargs):
            execute_subcommand(subcommand_func.__name__, *args, **kwargs)
        # Register subcommand
        subcommands_steps[subcommand_func.__name__] = (subcommand_func.__module__, step_list)
        return wrapper
    return inner


def execute_subcommand(subcommand, *args, **kwargs):
    if subcommand not in subcommands_steps:
        raise ValueError(f"Subcommand '{subcommand}' is not registered")
    subcommand_module, step_list = subcommands_steps[subcommand]
    logger = logging.getLogger(subcommand_module)
    parameter_processing_steps = tuple([ProcessParameter(key) for key, _ in kwargs.items()])
    executor = SubcommandExecutor(
        name=subcommand,
        module=subcommand_module,
        steps=parameter_processing_steps + step_list,
        logger=logger
    )
    executor.log_execution_plan()
    status = StepStatus.FAILURE
    start_clock = time.time()
    try:
        status = executor.execute_steps(args, kwargs)
    except Exception as e:
        logger.debug('Executing steps failed with following exception:', exc_info=e)
    end_clock = time.time()

    executor.log_command_resolution(status, start_clock, end_clock)
    if status == StepStatus.FAILURE:
        raise CommandFailedError(f"Command ended with status '{status}'")
