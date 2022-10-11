from click import group, option, argument, Path
import pandas as pd

from collector.steps.add_resample_indicators import add_resample_indicators
from collector.steps.add_labels import add_labels
from collector.steps.save_dataset import save_dataset
from commons.steps.get_dataset import get_dataset
from commons.steps.process_parameter import process_parameter
from commons.steps.rename_parameters import rename_parameters
from commons.timing import subcommand
from collector.steps.add_indicators import add_indicators

__all__ = ["extract_group"]


@group()
def extract_group(): pass


@extract_group.command()
@option("--name", "-n", help="Name of the output dataset")
@option("--time_tag", "-t", default='1h', help="Rescale data to hours, days, month")
@option("--deviation", "-x", default=0.01, help="Deviation from price for the best decision label")
@option("--dataset", "-d", help="Dataset to extract features from")
@option("--append", "-a", default=True, help="Whether to overwrite or append to an existing dataset with the same name", is_flag=True)
@subcommand([
    process_parameter("time_tag"),
    process_parameter("name", optional=True),
    process_parameter("deviation"),
    process_parameter("dataset"),
    get_dataset,
    add_indicators,
    add_labels,
    add_resample_indicators,
    rename_parameters({'resampled_X': 'df'}),
    save_dataset
])
def extract(*args, **kwargs):
    """Add technical indicators to dataset from FILE_PATH."""






