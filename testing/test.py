from click import group, option

from commons.steps.conditional import conditional
from commons.steps.not_interrupting import not_interrupting
from commons.timing import subcommand
from testing.steps.format_tests import format_tests
from testing.steps.shape_tests import shape_tests
from testing.steps.unit_tests import unit_tests

__all__ = ["test_group"]


@group()
def test_group():
    pass


@test_group.command()
@option("--skip-shape-tests", "-s", is_flag=True)
@option("--skip-unit-tests", "-u", is_flag=True)
@option("--skip-format-tests", "-f", is_flag=True)
@subcommand([
    conditional(not_interrupting(shape_tests), "skip_shape_tests", negation=True),
    conditional(not_interrupting(unit_tests), "skip_unit_tests", negation=True),
    conditional(not_interrupting(format_tests), "skip_format_tests", negation=True),
])
def test(*args, **kwargs):
    pass
