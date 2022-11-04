from click import group, argument

from collector.steps.convert_dataset_to_csv import convert_dataset_to_csv
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand

__all__ = ["dataset2csv_group"]


@group()
def dataset2csv_group(): pass


@dataset2csv_group.command()
@argument("source")
@argument("target")
@subcommand([
    process_parameter("source"),
    process_parameter("target"),
    convert_dataset_to_csv
])
def dataset2csv(*args, **kwargs): pass






