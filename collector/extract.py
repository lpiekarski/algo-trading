from click import group, option

from collector.steps.add_indicators import add_indicators
from collector.steps.add_labels import add_labels
from collector.steps.add_resample_indicators import add_resample_indicators
from collector.steps.convert_to_percentages import convert_to_percentages
from collector.steps.save_dataset import save_dataset
from core.steps.conditional import Conditional
from core.steps.get_dataset import get_dataset
from core.subcommand_execution.execution_flow import execution_flow

__all__ = ["extract_group"]


@group()
def extract_group():
    pass


@extract_group.command()
@option("--output", "-o",
        help="Name of the output dataset")
@option("--percentage", "-pct",
        help="Rescale to percentage difference")
@option("--dataset", "-d",
        help="Dataset to extract features from")
@option("--append",
        "-a",
        default=False,
        help="Whether to overwrite or append to an existing dataset with the same name",
        is_flag=True)
@option("--indicators",
        "-i",
        help="Specify yaml file with chosen indicators")
@option("--labels",
        "-l",
        help="Specify yaml file with chosen labels")
@execution_flow(
    get_dataset,
    Conditional(convert_to_percentages, "percentage"),
    Conditional(add_indicators, "indicators"),
    Conditional(add_labels, "labels"),
    save_dataset
)
def extract(*args, **kwargs):
    """Add technical indicators and labels to the dataset"""
