from core.exceptions import DataDownloadError
import logging
import yfinance as yf
import re 

LOGGER = logging.getLogger(__name__)


def get_data(amount, interval, start_date):
    df = yf.download(tickers="^GSPC", period=f"{amount}m", interval=format(interval), prepost=True)
    if df.empty:
        raise DataDownloadError("Failed to collect data")
    LOGGER.debug(f"Downloaded yfinance data: {df.head()}")
    # df = df[df.Volume != 0].tail(1)
    df.drop(columns=["Adj Close"], inplace=True)
    return df

def format(interval): 
    dictionary = {"min":"m", "m":"mo","w":"wk", "h":"h", "d":"d"}
    interval_split = re.split('(\d+)', interval) 
    if interval_split[2] not in dictionary.keys(): 
        raise DataDownloadError(f"yfinance does not accept such interval code: {interval_split[2]}")
    return interval_split[1] + dictionary[interval_split[2]]