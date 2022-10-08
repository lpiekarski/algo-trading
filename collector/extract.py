from click import group, option, argument, Path
import pandas as pd

from collector.steps.add_resample_indicators import add_resample_indicators
from collector.steps.label_short_long import label_long_short
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand
from collector.steps.add_indicators import add_indicators

__all__ = ["extract_group"]


@group()
def extract_group(): pass


@extract_group.command()
@option("--output", "-o", help="Name of output file. Default output filename is <original filename>_indicators.csv")
@option("--time", "-t", help="Rescale data to hours, days, month")
@option("--separator", "-s", help="By default separator is set to ','. Use this option if .csv separator is different")
@argument('file_path', type=Path(exists=True))
@subcommand([
    process_parameter("file_path"),
    process_parameter("time"),
    process_parameter("output", optional=True),
    process_parameter("separator", optional=True),
    add_indicators,
    label_long_short,
    add_resample_indicators,

])
def extract(file_path,  *args, **kwargs):
    """Add technical indicators to dataset from FILE_PATH."""






