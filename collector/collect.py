import datetime
import pandas as pd
import click
import logging
import yfinance as yf
from dateutil import parser

__all__ = ["collect", "collect_group"]

from commons.dataset import put_dataset
from commons.exceptions import BotErrorWithoutStacktrace
from commons.timing import command_success

LOGGER = logging.getLogger(__name__)

@click.group()
def collect_group():
    pass

@collect_group.command()
@click.option("--date", "-d", help="Date for which to collect the data (can be 'latest' for last available hour)")
@click.option("--name", "-n", help="Name of the created dataset. If none is provided defaults to the yyyy-MM-dd-HH date")
def collect(date: str, name: str):
    if date == "latest":
        end_date = datetime.datetime.now()
        start_date = datetime.datetime.now() - datetime.timedelta(hours=1)
    else:
        start_date = parser.parse(date)
        end_date = start_date + datetime.timedelta(hours=1)
    start_date = start_date.replace(minute=0, second=0, microsecond=0)
    end_date = end_date.replace(minute=0, second=0, microsecond=0)
    LOGGER.info(f"Collecting data for period {start_date} - {end_date}")
    df = yf.download(tickers='^GSPC', start=start_date, end=end_date, interval='1h')
    if df.empty:
        raise BotErrorWithoutStacktrace("Failed to collect data")
    if name is None:
        name = start_date.strftime("%Y-%m-%d-%H")
    put_dataset(name, df)
    command_success(LOGGER)

if __name__ == '__main__':
    collect()