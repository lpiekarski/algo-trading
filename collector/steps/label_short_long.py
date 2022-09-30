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
def label_long_short(df=None, sigma=0.01, output=None, file_path=None, *args, **kwargs):
    if df is None:
        LOGGER.error("There is no Date Frame loaded!")
    df['time'] = pd.to_datetime(df.index)
    df = add_long_short(df, sigma)
    LOGGER.info(df)
    if output is not None:
        output_filename = output
    else:
        output_filename = "{0}_{2}.{1}".format(*file_path.rsplit('.', 1) + ['indicators'])
    df.to_csv(output_filename)
    return dict(df=df)
