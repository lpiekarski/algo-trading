def perform_trade(trades, broker_module, **kwargs):
    """
    Performs the most recent trade only
    """
    trade = trades[-1]
    broker_module.open_position(trade)
