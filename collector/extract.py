from click import group, option

from collector.steps.add_indicators import add_indicators
from collector.steps.add_labels import add_labels
from collector.steps.add_resample_indicators import add_resample_indicators
from collector.steps.save_dataset import save_dataset
from commons.steps.get_dataset import get_dataset
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand

__all__ = ["extract_group"]


@group()
def extract_group(): pass


@extract_group.command()
@option("--name", "-n", help="Name of the output dataset")
@option("--time-tag", "-t", default='1h', help="Rescale data to hours, days, month")
@option("--dataset", "-d", help="Dataset to extract features from")
@option("--append", "-a", default=True, help="Whether to overwrite or append to an existing dataset with the same name", is_flag=True)
@option("--indicators", "-i", help="Path to the indicators configuration json file")
@subcommand([
    process_parameter("time_tag"),
    process_parameter("name", optional=True),
    process_parameter("dataset"),
    process_parameter("indicators", optional=True),
    get_dataset,
    add_indicators,
    add_labels,
    add_resample_indicators,
    save_dataset
])
def extract(*args, **kwargs):
    """Add technical indicators to dataset from FILE_PATH."""






