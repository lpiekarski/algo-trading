from click import group, option

from commons.steps.conditional import conditional
from commons.timing import subcommand
from testing.steps.drive_tests import drive_tests
from testing.steps.shape_tests import shape_tests

__all__ = ["test_group"]

@group()
def test_group(): pass

@test_group.command()
@option("--skip_shapes", "-s", is_flag=True)
@option("--skip_drives", "-d", is_flag=True)
@subcommand([
    conditional(shape_tests, "skip_shapes", negation=True),
    conditional(drive_tests, "skip_drives", negation=True)
])
def test(*args, **kwargs): pass
