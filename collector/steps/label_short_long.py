import logging

import pandas as pd

from collector.technical_indicators.Add_long_short import add_long_short
from collector.technical_indicators.technical_indicators import add_technical_indicators
from commons.timing import step
import yfinance as yf
from dateutil import parser
from dateutil.parser import ParserError
from commons.exceptions import BotError, DataDownloadError


LOGGER = logging.getLogger(__name__)

@step
def label_long_short(df=None, sigma=0.01, *args, **kwargs):
    if df is None:
        LOGGER.error("There is no Date Frame loaded!")
    df['time'] = pd.to_datetime(df.index)
    df = add_long_short(df, sigma)
    LOGGER.info(df)
    return dict(df=df)
