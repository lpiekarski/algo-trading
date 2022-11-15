from typing import Any, Type

import numpy as np
from backtesting import Strategy

interface = {
    'get_strategy': {
        'parameter_types': [np.ndarray, Any],
        'return_type': Type[Strategy]
    }
}
