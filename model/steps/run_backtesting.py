import datetime
import logging
from backtesting import Backtest, Strategy
import numpy as np
from trader.broker_apis import Signal

LOGGER = logging.getLogger(__name__)


def run_backtesting(
        trades,
        dataset,
        commission,
        leverage,
        starting_cash,
        trade_every_n,
        **kwargs):
    class BacktestStrategy(Strategy):
        def init(self):
            self.id = 1

        def next(self):
            if self.id % trade_every_n != 0:
                self.id += 1
                return
            if self.id == len(trades) - 1:
                self.position.close()
                return
            # for trade in self.trades:
            #    trade_time = self.data.index[-1] - trade.entry_time
            #    if trade_time > datetime.timedelta(minutes=180):
            #        tp = abs(trade.tp - trade.entry_price) / trade.entry_price
            #        sl = abs(trade.sl - trade.entry_price) / trade.entry_price
            #        tp *= 0.8
            #        sl *= 0.8
            #        if trade.is_long:
            #            trade.tp = trade.entry_price * (1 + tp)
            #            trade.sl = trade.entry_price * (1 - sl)
            #        else:
            #            trade.tp = trade.entry_price * (1 - tp)
            #            trade.sl = trade.entry_price * (1 + sl)
            trade = trades[self.id]
            real_volume = int(trade.volume * 100)
            if trade.trade_type == Signal.BUY:
                self.buy(size=real_volume,
                         tp=trade.take_profit,
                         sl=trade.stop_loss)
            elif trade.trade_type == Signal.SELL:
                self.sell(size=real_volume,
                          tp=trade.take_profit,
                          sl=trade.stop_loss)
            self.id += 1

    LOGGER.info("Backtesting predictions")

    stock_data = dataset.get_x()
    mask = (~stock_data["Close"].isna()).tolist()
    stock_data = stock_data[mask]
    trades = np.array(trades)[mask]

    bt = Backtest(
        stock_data,
        BacktestStrategy,
        commission=commission,
        margin=(1. / leverage),
        exclusive_orders=False,
        cash=starting_cash,
        trade_on_close=True,
        hedging=True
    )

    backtest_results = bt.run()
    LOGGER.info(backtest_results)
    bt.plot(resample=False)
    return dict(backtest=bt, backtest_results=backtest_results)
