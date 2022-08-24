import logging

from commons.timing import run_step
import yfinance as yf
from dateutil import parser
from dateutil.parser import ParserError
from commons.exceptions import BotError, DataDownloadError

LOGGER = logging.getLogger(__name__)

@run_step
def download_data(date="latest", *args, **kwargs):
    if date == "latest":
        LOGGER.info(f"Collecting latest data")
        df = yf.download(tickers='^GSPC', period='2h', interval='1h', prepost=True)
        if df.empty:
            raise DataDownloadError("Failed to collect data")
        LOGGER.debug(f"Downloaded yfinance data: {df.head()}")
        df = df[df.Volume != 0].tail(1)
        start_date = df.index[0]
        LOGGER.info(f"Collection start date is '{start_date}'")
        return df, start_date
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
        return df, start_date