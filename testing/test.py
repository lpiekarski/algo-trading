from click import group, option

from commons.steps.conditional import conditional
from commons.timing import subcommand
from testing.steps.shape_tests import shape_tests
from testing.steps.unit_tests import unit_tests

__all__ = ["test_group"]


@group()
def test_group(): pass

@test_group.command()
@option("--skip-shapes", "-s", is_flag=True)
@option("--skip-unit", "-u", is_flag=True)
@subcommand([
    conditional(shape_tests, "skip-shapes", negation=True),
    conditional(unit_tests, "skip-unit", negation=True),
])
def test(*args, **kwargs): pass
