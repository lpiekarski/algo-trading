import pandas as pd
import numpy as np

interface = {
    'initialize': {
        'parameter_types': [str],
        'return_type': None
    },
    'predict': {
        'parameter_types': [pd.DataFrame],
        'return_type': np.ndarray
    },
    'train': {
        'parameter_types': [pd.DataFrame, pd.DataFrame],
        'return_type': None
    },
    'save_weights': {
        'parameter_types': [str],
        'return_type': None
    },
    'load_weights': {
        'parameter_types': [str],
        'return_type': None
    }
}
