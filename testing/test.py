from click import group, option

from commons.steps.conditional import conditional
from commons.steps.not_interrupting import not_interrupting
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand
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
@subcommand([
    process_parameter("skip_shape_tests", optional=True),
    process_parameter("skip_unit_tests", optional=True),
    process_parameter("skip_format_tests", optional=True),
    conditional(not_interrupting(shape_tests), "skip_shape_tests", negation=True),
    conditional(not_interrupting(unit_tests), "skip_unit_tests", negation=True),
    conditional(not_interrupting(format_tests), "skip_format_tests", negation=True),
])
def test(*args, **kwargs):
    """Run tests"""
