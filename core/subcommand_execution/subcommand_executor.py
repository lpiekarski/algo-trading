import logging
from datetime import datetime

from core.exceptions import NonInterruptingError
from core.string import BOLD, break_padded, ENDC, OKBLUE, BREAK, FAIL, OKCYAN
from core.subcommand_execution.step import StepStatus, Step, StepExecutionTracker, colored_status_str

LOGGER = logging.getLogger(__name__)


class SubcommandExecutor:
    """
    A helper class for managing the execution of a subcommand.
    """

    def __init__(self, name: str, module: str, steps, logger: logging.Logger):
        """
        SubcommandExecutor initializer.
        :param name: Subcommand name as string.
        :param module: Subcommand module as string.
        :param steps: List of step functions that are to be executed during the subcommand.
        :param logger: Logger used as output.
        """
        LOGGER.debug(f"Initializing subcommand executor")
        self.logger = SubcommandExecutorLogger(logger, name, module)
        self.steps = [
            StepExecutionTracker(
                name=Step.get_name(step),
                module=Step.get_module(step),
                log_level=Step.get_log_level(step),
                callback=Step.get_callback(step)
            ) for step in steps
        ]

    def log_execution_plan(self) -> None:
        """
        Output subcommand execution plan to the logger.
        """
        self.logger.log_module_and_name()
        self.logger.log_horizontal_line()
        self.logger.log_execution_plan_str()
        for step in self.steps:
            self.logger.log_step_execution_plan(step)

    def log_command_resolution(self, status: StepStatus, start_clock: float, end_clock: float) -> None:
        """
        Output subcommand summary to the logger.
        :param status: Subcommand resolution status.
        :param start_clock: Unix start time in seconds.
        :param end_clock: Unix end time in seconds.
        """
        self.logger.log_empty_line()
        if any([step.error is not None for step in self.steps]):
            self.logger.log_horizontal_line()
            self.logger.log_detailed_errors_str()
            for step in filter(lambda s: s.error is not None, self.steps):
                self.logger.log_step_detailed_error(step)
        self.logger.log_horizontal_line()
        self.logger.log_results_str()
        for step in self.steps:
            self.logger.log_step_resolution(step)
        self.logger.log_horizontal_line()
        self.logger.log_command_status(status)
        self.logger.log_horizontal_line()
        self.logger.log_total_time(start_clock, end_clock)
        self.logger.log_end_time(end_clock)
        self.logger.log_horizontal_line()
        self.logger.log_empty_line()

    def execute_steps(self, args: tuple, kwargs: dict) -> StepStatus:
        """
        This method is responsible for the actual execution of subcommand steps.
        :param args: Arguments passed to the subcommand.
        :param kwargs: Keyword arguments passed to the subcommand.
        :return: Status of the subcommand.
        """
        LOGGER.debug(f"Executing subcommand steps with args: {args} and kwargs: {kwargs}")
        previous_step_return_value = dict()
        status = StepStatus.SUCCESS
        for step in self.steps:
            if previous_step_return_value is not None and isinstance(previous_step_return_value, dict):
                kwargs |= previous_step_return_value
            try:
                self.logger.log_step_title(step)
                previous_step_return_value = step.execute_step(args, kwargs)
            except Exception as e:
                status = StepStatus.FAILURE
                if not isinstance(e, NonInterruptingError):
                    raise e
            finally:
                self.logger.log_step_completion(kwargs)
        return status


class SubcommandExecutorLogger:
    """
    This class defines methods that are useful for logging information about subcommand workflow and steps.
    """

    def __init__(self, logger: logging.Logger, name: str, module: str):
        """
        Instance initialization.
        :param logger: Logger that will be used as an output.
        :param name: Name of the subcommand.
        :param module: Module containing the subcommand.
        """
        self.logger = logger
        self.name = name
        self.module = module

    def log_horizontal_line(self) -> None:
        """
        Output horizontal line of '-' signs.
        """
        self.logger.info(f"{BOLD}{BREAK}{ENDC}")

    def log_module_and_name(self) -> None:
        """
        Output subcommand module and name as a title line
        """
        self.logger.info(BOLD + OKBLUE + break_padded(f"{self.module}:{self.name}") + ENDC)
        self.log_empty_line()

    def log_execution_plan_str(self) -> None:
        """
        Log "\tExecution plan:" followed by an empty line.
        """
        self.logger.info("\tExecution plan:")
        self.log_empty_line()

    def log_step_execution_plan(self, step) -> None:
        """
        Log using the logger that is appropriate for this step:
        step name followed by "@" sign, followed by step module.
        :param step: Step from which the name and module values are extracted.
        """
        step.get_log_func(self.logger)(f"\t\t{step.name} @ {step.module}")

    def log_empty_line(self) -> None:
        """
        Log single empty line.
        """
        self.logger.info("")

    def log_results_str(self) -> None:
        """
        Log "Results:" followed by an empty line.
        """
        self.logger.info(f"Results:")
        self.log_empty_line()

    def log_detailed_errors_str(self) -> None:
        """
        Log "Detailed Errors:" followed by an empty line.
        """
        self.logger.info(f"Detailed Errors:")
        self.log_empty_line()

    def log_step_resolution(self, step) -> None:
        """
        Log a line containing information about the step' resolution e.g.
        step name, result status, duration and error summary if any occurred.
        :param step: Step for which to create this log line.
        """
        log_func = step.get_log_func(self.logger)
        step_name = step.name + ' '
        if len(step_name) >= 68:
            step_name = f"{step_name[:64]}... "
        if step.result == StepStatus.SKIPPED:
            message = f"{step_name:.<68} {colored_status_str(step.result)}"
        else:
            message = f"{step_name:.<68} {colored_status_str(step.result)} [{step.end_clock - step.start_clock :.5f} s]"
        if step.error is not None:
            message += f"{FAIL} {type(step.error).__name__}: {step.error}{ENDC}"
        log_func(message)

    def log_step_detailed_error(self, step) -> None:
        """
        Log detailed error information for given step.
        Assumes that an error occurred during the execution of the step i.e. step.error is not None.
        :param step: Step for which to create this log line.
        """
        self.logger.error(f"Error in step {step.name} @ {step.module}:", exc_info=step.error)

    def log_command_status(self, status: StepStatus) -> None:
        """
        Log given command status.
        :param status: Status of the subcommand to log.
        """
        self.logger.info(f"COMMAND {colored_status_str(status)}")

    def log_total_time(self, start_clock: float, end_clock: float) -> None:
        """
        Log the total time of the subcommand.
        :param start_clock: Unix start clock time in seconds.
        :param end_clock: Unix end clock time in seconds.
        """
        self.logger.info(f"Total time: {end_clock - start_clock :.5f} s")

    def log_end_time(self, end_clock: float) -> None:
        """
        Log formatted time at which the subcommand was completed.
        :param end_clock: Unix end clock time in seconds.
        """
        self.logger.info(f"Finished at: {datetime.fromtimestamp(end_clock).strftime('%Y-%m-%dT%H:%M:%S')}")

    def log_step_title(self, step) -> None:
        """
        Log the title of the step consisting of step name and module, pretty printed.
        :param step: Step for which to create this log line.
        """
        log = step.get_log_func(self.logger)
        log("")
        log(f"{BOLD}---{ENDC} {OKCYAN}{step.name}{ENDC} {BOLD}@{ENDC} {OKCYAN}{step.module}{ENDC} {BOLD}---{ENDC}")

    def log_step_completion(self, kwargs: dict) -> None:
        """
        Log the debug information after the step is completed.
        :param kwargs: Keyword arguments extracted after the execution of the step.
        """
        self.logger.debug(f"Step completed, kwargs:")
        self.logger.debug(f"\t{kwargs}")
