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
def add_indicators(dataset, **kwargs):
    add_technical_indicators(dataset, time_tag="") #TODO: is this time_tag correct?
