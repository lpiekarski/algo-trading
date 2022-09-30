import logging

import pandas as pd

from collector.technical_indicators.resample_technical_indicators import resample_technical_indicators
from collector.technical_indicators.technical_indicators import add_technical_indicators
from commons.timing import step
import yfinance as yf
from dateutil import parser
from dateutil.parser import ParserError
from commons.exceptions import BotError, DataDownloadError


LOGGER = logging.getLogger(__name__)

@step
def add_resample_indicators(df=None, time='1h', separator=',', *args, **kwargs):
    if df is None:
        LOGGER.error("There is no Date Frame loaded!")
    LOGGER.info(f"reshape to time unit '{time}'")
    df = resample_technical_indicators(df, time_tag=time)
    LOGGER.info(df)
    return dict(df=df)
