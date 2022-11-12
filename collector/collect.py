from click import group, option

from collector.steps.create_dataset import create_dataset
from collector.steps.save_dataset import save_dataset
from collector.steps.wait_before_download import wait_before_download
from commons.steps.conditional import conditional
from commons.steps.process_parameter import process_parameter
from commons.timing import subcommand

__all__ = ["collect_group"]


@group()
def collect_group(): pass


@collect_group.command()
@option("--date", "-d", default="latest",
        help="Date for which to collect the data (can be 'latest' for last available hour)")
@option("--output", "-n",
        help="Path of the created dataset. If none is provided defaults to the YYYY-mm-dd-HH-MM date")
@option("--wait",
        "-w",
        help="Wait for the next full hour to download the data",
        is_flag=True)
@option("--append",
        "-a",
        default=False,
        help="Whether to overwrite or append to an existing dataset with the same "
        "name",
        is_flag=True)
@subcommand([
    process_parameter("date"),
    process_parameter("output"),
    process_parameter("wait"),
    process_parameter("append"),
    conditional(wait_before_download, 'wait'),
    create_dataset,
    save_dataset
])
def collect(*args, **kwargs): pass
