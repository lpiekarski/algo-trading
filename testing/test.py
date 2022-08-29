from click import group, option
from commons.timing import subcommand
from testing.steps.drive_tests import drive_tests
from testing.steps.shape_tests import shape_tests

__all__ = ["test_group"]

@group()
def test_group():
    pass

@test_group.command()
@option("--skip_shapes", "-s", is_flag=True)
@option("--skip_drives", "-d", is_flag=True)
@subcommand([
    shape_tests,
    drive_tests
])
def test(*args, **kwargs):
    pass

if __name__ == '__main__':
    test()
