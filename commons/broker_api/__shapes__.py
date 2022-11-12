import numpy as np

interface = {
    'execute_decision': {
        # array of decisions, volume, stop loss/take profit percent
        'parameter_types': [np.ndarray, float, float],
        'return_type': None
    },
}
