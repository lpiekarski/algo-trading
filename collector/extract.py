from click import group, option

from collector.steps.add_indicators import add_indicators
from collector.steps.add_labels import add_labels
from collector.steps.add_resample_indicators import add_resample_indicators
from collector.steps.save_dataset import save_dataset
from commons.steps.conditional import conditional
from commons.steps.get_dataset import get_dataset
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand

__all__ = ["extract_group"]


@group()
def extract_group():
    pass


@extract_group.command()
@option("--output", "-o",
        help="Name of the output dataset")
@option("--time-tag", "-t",
        help="Rescale data to hours, days, month")
@option("--dataset", "-d",
        help="Dataset to extract features from")
@option("--append",
        "-a",
        default=True,
        help="Whether to overwrite or append to an existing dataset with the same name",
        is_flag=True)
@option("--indicators",
        "-i",
        help="Specify yaml file with chosen indicators")
@option("--labels",
        "-l",
        help="Specify yaml file with chosen labels")
@subcommand([
    process_parameter("time_tag", optional=True),
    process_parameter("name", optional=True),
    process_parameter("dataset"),
    process_parameter("indicators", optional=True),
    process_parameter("labels", optional=True),
    get_dataset,
    conditional(add_indicators, "time_tag", negation=True),
    conditional(add_resample_indicators, "time_tag"),
    add_labels,
    save_dataset
])
def extract(*args, **kwargs):
    """Add technical indicators to dataset from FILE_PATH."""
