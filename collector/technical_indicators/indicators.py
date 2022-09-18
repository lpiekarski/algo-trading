from click import group, option, argument, Path
import pandas as pd

from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand
from .technical_indicators import add_technical_indicators

__all__ = ["indicators_group"]


@group()
def indicators_group(): pass


@indicators_group.command()
@option("--output", "-o", help="Name of output file. Default output filename is <original filename>_indicators.csv")
@option("--time", "-t", help="Rescale data to hours, days, month")
@option("--separator", "-s", help="By default separator is set to ','. Use this option if .csv separator is different")
@argument('file_path', type=Path(exists=True))
@subcommand([
    process_parameter("time"),
    process_parameter("output", optional=True),
    process_parameter("separator", optional=True),
])
def indicators(file_path, time='h', output=None, separator=',',  *args, **kwargs):
    """Add technical indicators to dataset from FILE_PATH."""
    df = pd.read_csv(file_path, sep=separator)
    df = add_technical_indicators(df, time_tag=time)
    if output:
        output_filename = output
    else:
        output_filename = "{0}_{2}.{1}".format(*file_path.rsplit('.', 1) + ['indicators'])

    df.to_csv(output_filename)






