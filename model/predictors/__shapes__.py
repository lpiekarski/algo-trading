import pandas as pd

interface = {
    'predict': {
        'parameter_types': [pd.DataFrame],
        'return_type': pd.DataFrame
    },
    'train': {
        'parameter_types': [pd.DataFrame, pd.DataFrame],
        'return_type': None
    }
}