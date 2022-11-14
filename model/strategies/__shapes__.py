from backtesting import Strategy

interface = {
    'get_strategy': {
        'parameter_types': [dict],
        'return_type': Strategy
    }
}
