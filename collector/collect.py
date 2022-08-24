import datetime
import click
import logging
import yfinance as yf
from dateutil import parser
from dateutil.parser import ParserError
from commons.dataset import put_dataset
from commons.exceptions import BotError, DataDownloadError
from commons.string import BREAK, break_padded
from commons.timing import command_success

__all__ = ["collect", "collect_group"]

LOGGER = logging.getLogger(__name__)

@click.group()
def collect_group():
    pass

@collect_group.command()
@click.option("--date", "-d", help="Date for which to collect the data (can be 'latest' for last available hour)")
@click.option("--name", "-n", help="Name of the created dataset. If none is provided defaults to the YYYY-mm-dd-HH-MM date")
def collect(date: str, name: str):
    LOGGER.info(break_padded(f"collector:collect"))
    if date == "latest":
        LOGGER.info(f"Collecting latest data")
        df = yf.download(tickers='^GSPC', period='2h', interval='1h', prepost=True)
        if df.empty:
            raise DataDownloadError("Failed to collect data")
        LOGGER.debug(f"Downloaded yfinance data: {df.head()}")
        df = df[df.Volume != 0].tail(1)
        start_date = df.index[0]
    else:
        LOGGER.info(f"Collecting data starting from '{date}'")
        try:
            start_date = parser.parse(date)
        except ParserError as e:
            raise BotError(f"Failed to parse date '{date}'")
        end_date = start_date + datetime.timedelta(hours=1)
        start_date = start_date.replace(minute=0, second=0, microsecond=0)
        end_date = end_date.replace(minute=0, second=0, microsecond=0)
        LOGGER.info(f"Collecting data for period '{start_date}' - '{end_date}'")
        df = yf.download(tickers='^GSPC', start=start_date, end=end_date, prepost=True)
        if df.empty:
            raise DataDownloadError("Failed to collect data")
        df = df[df.Volume != 0].tail(1)
    LOGGER.info(f"Collection start date is '{start_date}'")
    if name is None:
        name = start_date.strftime("%Y-%m-%d-%H-%M")
    put_dataset(name, df)
    command_success(LOGGER)

if __name__ == '__main__':
    collect()