import pandas as pd
import numpy as np

interface = {
    'predict': {
        'parameter_types': [pd.DataFrame],
        'return_type': np.ndarray
    },
    'train': {
        'parameter_types': [pd.DataFrame, pd.DataFrame],
        'return_type': None
    },
    'save': {
        'parameter_types': [str],
        'return_type': None
    },
    'load': {
        'parameter_types': [str],
        'return_type': None
    }
}