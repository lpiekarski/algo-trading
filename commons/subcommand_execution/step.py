import logging
import time
from abc import abstractmethod
from enum import Enum
from commons.string import BOLD, ENDC, OKCYAN, WARNING, FAIL, OKGREEN

LOGGER = logging.getLogger(__name__)


class StepLogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class StepStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    SKIPPED = "SKIPPED"


def colored_status_str(status: StepStatus):
    if status == StepStatus.SUCCESS:
        return f"{OKGREEN}SUCCESS{ENDC}"
    if status == StepStatus.FAILURE:
        return f"{FAIL}FAILURE{ENDC}"
    return f"{WARNING}{status.value}{ENDC}"


class Step:
    """
    Parent class for steps.
    """

    def __init__(self, name: str, module: str, log_level: StepLogLevel):
        """
        Step initialization.
        :param name: Name of the step.
        :param module: Module containing the step.
        :param log_level: Log level of the step. A "debug" step is only logged in debug mode, "info" step is logged
            in debug and info, etc.
        """
        self.name = name
        self.module = module
        self.log_level = log_level

    @abstractmethod
    def callback(self, *args, **kwargs):
        """
        This method specifies the callback function that is called when this step is executed.
        This function has to take *args and **kwargs as parameters and can
            return a dict of values that will be passed as a parameter input to the next step.
        """
        raise NotImplementedError("Called 'callback()' on Step parent class")

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

    @classmethod
    def get_name(cls, step) -> str:
        """
        Get name of step that is either an instance of Step class or a Callable.
        :param step: Step instance or Callable.
        :return: Name of the step.
        """
        if isinstance(step, Step):
            return step.name
        else:
            return step.__name__

    @classmethod
    def get_module(cls, step) -> str:
        """
        Get module of the step that is either an instance of Step class or a Callable.
        :param step: Step instance or Callable.
        :return: Module of the step.
        """
        if isinstance(step, Step):
            return step.module
        else:
            return step.__module__

    @classmethod
    def get_log_level(cls, step) -> StepLogLevel:
        """
        Get log level of the step that is either an instance of Step class or a Callable.
        If the step is a Callable the default "INFO" log level is returned.
        :param step: Step instance or Callable.
        :return: Log level of the step, if the step is an instance of Step class or "INFO" log level otherwise.
        """
        if isinstance(step, Step):
            return step.log_level
        else:
            return StepLogLevel.INFO

    @classmethod
    def get_callback(cls, step):
        """
        Get callback of the step that is either an instance of Step class or a Callable.
        If the step is a Callable, the step is already its own callback.
        :param step: Step instance or Callable.
        :return: Callback callable of the step.
        """
        if isinstance(step, Step):
            return step.callback
        else:
            return step


class StepExecutionTracker:
    def __init__(self, name: str, module: str, callback, log_level: StepLogLevel = StepLogLevel.INFO):
        self.name = name
        self.module = module
        self.start_clock = None
        self.end_clock = None
        self.result = StepStatus.SKIPPED
        self.log_level = log_level
        self.callback = callback
        self.resolved = False
        self.error = None

    def execute_step(self, args: tuple, kwargs: dict):
        self.start_execution()
        try:
            value = self.callback(*args, **kwargs)
            self.resolve(StepStatus.SUCCESS)
        except Exception as e:
            self.error = e
            self.resolve(StepStatus.FAILURE)
            raise e
        return value

    def start_execution(self):
        LOGGER.debug(f"Starting execution of step '{self.name}'")
        self.start_clock = time.time()

    def resolve(self, status):
        LOGGER.debug(f"Step {self.name} resolved with status '{status}'")
        self.result = status
        self.end_clock = time.time()
        self.resolved = True

    def log_title(self, logger):
        log = self.get_log_func(logger)
        log("")
        log(f"{BOLD}---{ENDC} {OKCYAN}{self.name}{ENDC} {BOLD}@{ENDC} {OKCYAN}{self.module}{ENDC} {BOLD}---{ENDC}")

    def get_log_func(self, logger: logging.Logger):
        return getattr(logger, self.log_level.value)
