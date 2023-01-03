import logging
from datetime import datetime

from commons.exceptions import NonInterruptingError
from commons.string import BOLD, break_padded, ENDC, OKBLUE, BREAK, FAIL
from commons.subcommand_execution.step import StepStatus, Step, StepExecutionTracker, colored_status_str

LOGGER = logging.getLogger(__name__)


class SubcommandExecutor:
    """
    A helper class for managing the execution of a subcommand.
    """

    def __init__(self, steps):
        """
        SubcommandExecutor initializer.
        :param steps: List of step functions that are to be executed during the subcommand.
        """
        LOGGER.debug(f"Initializing subcommand executor")
        self.steps = [
            StepExecutionTracker(
                name=Step.get_name(step),
                module=Step.get_module(step),
                log_level=Step.get_log_level(step),
                callback=Step.get_callback(step)
            ) for step in steps
        ]

    def log_execution_plan(self, logger: logging.Logger, module: str, name: str):
        logger.info(BOLD + OKBLUE + break_padded(f"{module}:{name}") + ENDC)
        logger.info("")
        logger.info(f"{BOLD}{BREAK}{ENDC}")
        logger.info("\tExecution plan:")
        logger.info("")
        for step in self.steps:
            step.get_log_func(logger)(f"\t\t{step.name} @ {step.module}")

    def log_command_resolution(self, logger: logging.Logger, status: StepStatus, start_clock, end_clock):
        logger.info(f"")
        logger.info(f"{BOLD}{BREAK}{ENDC}")
        logger.info(f"Results:")
        logger.info(f"")
        for step in self.steps:
            log_func = step.get_log_func(logger)
            if step.result == StepStatus.SKIPPED:
                message = f"{step.name + ' ' :.<52} {colored_status_str(step.result)}"
            else:
                message = f"{step.name + ' ' :.<52} {colored_status_str(step.result)} [{step.end_clock - step.start_clock :.5f} s]"
            if step.error is not None:
                message += f"{FAIL} {type(step.error).__name__}: {step.error}{ENDC}"
            log_func(message)
        if any([step.error is not None for step in self.steps]):
            logger.info(f"{BOLD}{BREAK}{ENDC}")
            logger.info(f"Detailed Errors:")
            for step in self.steps:
                if step.error is None:
                    continue
                logger.error(f"Error in step {step.name} @ {step.module}:", exc_info=step.error)
        logger.info(f"{BOLD}{BREAK}{ENDC}")
        logger.info(f"COMMAND {colored_status_str(status)}")
        logger.info(f"{BOLD}{BREAK}{ENDC}")
        logger.info(f"Total time: {end_clock - start_clock :.5f} s")
        logger.info(f"Finished at: {datetime.fromtimestamp(end_clock).strftime('%Y-%m-%dT%H:%M:%S')}")
        logger.info(f"{BOLD}{BREAK}{ENDC}")

        logger.info(f"")

    def execute_steps(self, logger: logging.Logger, args: tuple, kwargs: dict):
        previous_step_return_value = dict()
        status = StepStatus.SUCCESS
        for step in self.steps:
            if previous_step_return_value is not None and isinstance(
                    previous_step_return_value, dict):
                kwargs |= previous_step_return_value
            try:
                step.log_title(logger)
                previous_step_return_value = step.execute_step(args, kwargs)
            except Exception as e:
                status = StepStatus.FAILURE
                if not isinstance(e, NonInterruptingError):
                    raise e
            finally:
                logger.debug(f"Step completed, kwargs:")
                logger.debug(f"\t{kwargs}")
        return status
