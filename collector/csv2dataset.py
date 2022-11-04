from click import group, argument

from collector.steps.convert_csv_to_dataset import convert_csv_to_dataset
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand

__all__ = ["csv2dataset_group"]


@group()
def csv2dataset_group(): pass


@csv2dataset_group.command()
@argument("source")
@argument("target")
@subcommand([
    process_parameter("source"),
    process_parameter("target"),
    convert_csv_to_dataset
])
def csv2dataset(*args, **kwargs): pass






