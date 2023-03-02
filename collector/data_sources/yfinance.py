from core.exceptions import DataDownloadError
import logging
import yfinance as yf

LOGGER = logging.getLogger(__name__)


def get_data(amount, interval, start_date):
    df = yf.download(tickers="^GSPC", period=f"{amount}m", interval=interval, prepost=True)
    if df.empty:
        raise DataDownloadError("Failed to collect data")
    LOGGER.debug(f"Downloaded yfinance data: {df.head()}")
    # df = df[df.Volume != 0].tail(1)
    df.drop(columns=["Adj Close"], inplace=True)
    return df
