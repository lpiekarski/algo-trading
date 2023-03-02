from click import group, option

from collector.steps.create_dataset import create_dataset
from collector.steps.save_dataset import save_dataset
from collector.steps.wait_before_download import wait_before_download
from core.steps.conditional import Conditional
from core.subcommand_execution.execution_flow import execution_flow

__all__ = ["collect_group"]


@group()
def collect_group():
    pass


@collect_group.command()
@option("--source", "-s", multiple=True,
        help="Name of the data source")
@option("--amount", "-m",
        help="Amount of data to collect")
@option("--start-date", help="Start date of the data to collect")
@option("--interval", "-i",
        help="Dataset interval",
        default="1min")
@option("--output", "-n",
        help="Path of the created dataset. If none is provided defaults to the YYYY date")
@option("--wait",
        "-w",
        help="Wait for the next full hour to download the data",
        is_flag=True)
@option("--append",
        "-a",
        default=False,
        help="Whether to overwrite or append to an existing dataset with the same name",
        is_flag=True)
@execution_flow(
    Conditional(wait_before_download, 'wait'),
    create_dataset,
    save_dataset
)
def collect(*args, **kwargs):
    """
    Collect OHLCV data from an external source and save it as a dataset
    """
