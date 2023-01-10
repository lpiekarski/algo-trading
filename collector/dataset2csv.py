from click import group, argument

from collector.steps.convert_dataset_to_csv import convert_dataset_to_csv
from core.subcommand_execution.execution_flow import execution_flow

__all__ = ["dataset2csv_group"]


@group()
def dataset2csv_group():
    pass


@dataset2csv_group.command()
@argument("source")
@argument("target")
@execution_flow(
    convert_dataset_to_csv
)
def dataset2csv(*args, **kwargs):
    """
    Convert file from dataset to csv format
    """
