import importlib
import logging
from core.env import require_env

LOGGER = logging.getLogger(__name__)


def get_broker_module(name=None):
    if name is None:
        name = require_env('broker')
    LOGGER.debug(f"Getting broker module '{name}'")
    broker = importlib.import_module(f"trader.broker_apis.{name}")
    return broker


class Signal(object):
    BUY = 0
    SELL = 1
    NO_ACTION = 2


class Trade:
    def __init__(
            self,
            trade_type: Signal,
            price: float,
            volume: float,
            take_profit: float | None = None,
            stop_loss: float | None = None,
            close_after: float | None = None,
            comment: str = ""):
        self.trade_type = trade_type
        self.price = price
        self.volume = volume
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.close_after = close_after
        self.comment = comment

    def __repr__(self):
        return f"Trade(type={self.trade_type}, price={self.price}, volume={self.volume}, tp={self.take_profit}, sl={self.stop_loss}, close_after={self.close_after}, comment={self.comment})"
