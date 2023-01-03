from click import group, argument

from commons.subcommand_execution.execution_flow import execution_flow
from collector.steps.convert_csv_to_dataset import convert_csv_to_dataset

__all__ = ["csv2dataset_group"]


@group()
def csv2dataset_group():
    pass


@csv2dataset_group.command()
@argument("source")
@argument("target")
@execution_flow(
    convert_csv_to_dataset
)
def csv2dataset(*args, **kwargs):
    """
    Convert file from csv to dataset format
    """
