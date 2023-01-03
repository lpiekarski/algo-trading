from click import group, option

from commons.steps.conditional import Conditional
from commons.steps.non_interrupting import NonInterrupting
from commons.subcommand_execution.execution_flow import execution_flow
from testing.steps.format_tests import format_tests
from testing.steps.shape_tests import shape_tests
from testing.steps.unit_tests import unit_tests

__all__ = ["test_group"]


@group()
def test_group():
    pass


@test_group.command()
@option("--skip-shape-tests", "-s", is_flag=True, required=False, default=None)
@option("--skip-unit-tests", "-u", is_flag=True, required=False, default=None)
@option("--skip-format-tests", "-f", is_flag=True, required=False, default=None)
@execution_flow(
    Conditional(NonInterrupting(shape_tests), "skip_shape_tests", False),
    Conditional(NonInterrupting(unit_tests), "skip_unit_tests", False),
    Conditional(NonInterrupting(format_tests), "skip_format_tests", False),
)
def test(*args, **kwargs):
    """
    Run tests
    """
