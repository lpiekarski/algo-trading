import logging

import pandas as pd

from collector.technical_indicators.technical_indicators import add_technical_indicators
from commons.timing import step
import yfinance as yf
from dateutil import parser
from dateutil.parser import ParserError
from commons.exceptions import BotError, DataDownloadError


LOGGER = logging.getLogger(__name__)

@step
def add_indicators(file_path=None, separator=',', *args, **kwargs):
    LOGGER.info(f"Prepare data from '{file_path}'")
    LOGGER.info(f"with separator set to '{separator}'")
    df = pd.read_csv(file_path, index_col=0, parse_dates=True, sep=separator)
    df = add_technical_indicators(df, time_tag="")
    LOGGER.info(df)
    return dict(df=df)
