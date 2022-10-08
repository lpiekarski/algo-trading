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
def add_resample_indicators(df=None, time='1h', output=None, file_path=None, separator=',', *args, **kwargs):
    if df is None:
        LOGGER.error("There is no Date Frame loaded!")
    LOGGER.info(f"reshape to time unit '{time}'")
    resample_df = resample_technical_indicators(df, time_tag=time)
    df = pd.concat([df, resample_df], axis=1, join='inner')
    if output is not None:
        output_filename = output
    else:
        output_filename = "{0}_{2}.{1}".format(*file_path.rsplit('.', 1) + ['indicators'])
    df.to_csv(output_filename)
    LOGGER.info(df)
    return dict(df=df)
