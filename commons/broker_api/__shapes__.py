import numpy as np

interface = {
    'execute_decision': {
        'parameter_types': [np.ndarray, float, float],  # array of decisions, volume, stop loss/take profit percent
        'return_type': None
    },
}