from click import group, option

from core.steps.conditional import Conditional
from core.steps.non_interrupting import NonInterrupting
from core.subcommand_execution.execution_flow import execution_flow
from testing.steps.format_tests import format_tests
from testing.steps.integration_tests import integration_tests
from testing.steps.unit_tests import unit_tests

__all__ = ["test_group"]


@group()
def test_group():
    pass


@test_group.command()
@option("--skip-unit-tests", "-u", is_flag=True, required=False, default=None)
@option("--skip-integration-tests", "-i", is_flag=True, required=False, default=None)
@option("--skip-format-tests", "-f", is_flag=True, required=False, default=None)
@execution_flow(
    Conditional(NonInterrupting(unit_tests), "skip_unit_tests", False),
    Conditional(NonInterrupting(integration_tests), "skip_integration_tests", False),
    Conditional(NonInterrupting(format_tests), "skip_format_tests", False),
)
def test(*args, **kwargs):
    """
    Run tests
    """
