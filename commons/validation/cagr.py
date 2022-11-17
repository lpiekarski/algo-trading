def cagr_ratio(equity_strat, equity_end, time):
    return ((equity_end / equity_strat)**(1 / time) - 1) * 100
