import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime, timedelta

# connect to MetaTrader 5
if not mt5.initialize():
    print('initialize() failed')
    mt5.shutdown()

# request tick data
ticks = mt5.copy_ticks_range(
    'BOVA11',
    datetime(2021, 1, 1),
    datetime(2021, 1, 7),
    mt5.COPY_TICKS_TRADE
)
ticks = pd.DataFrame(ticks)
ticks.to_csv('BOVA11_ticks.csv', index=False)

# shut down connection to MetaTrader 5
mt5.shutdown()


# Machine learning SVM

# libraries
# Machine learning SVM
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import torch.optim as optim
import torch
from torch import nn
import pandas as pd
import numpy as np
import logging
import os
from commons import pytorch
from commons.data.preprocessor import Preprocessor

# For data manipulation
import pandas as pd
import numpy as np

# To plot
import matplotlib.pyplot as plt

# To ignore warnings
import warnings

warnings.filterwarnings("ignore")

# libraries to make features
#import pandas_ta as pta

LOGGER = logging.getLogger(__name__)

model: nn.Module = None
preprocessor: Preprocessor = None

# RSI
df_30min['Rsi_14_SVM'] = pta.rsi(df_30min['Close'], length=14)
df_30min['Rsi_26_SVM'] = pta.rsi(df_30min['Close'], length=26)



def predict(x: pd.DataFrame) -> np.ndarray:
    cls = SVC().fit(X_train, y_train)
    return cls

X = df_30min[['Open-Close', 'High-Low', 'Rsi_14', 'Rsi_26', 'SMA_10', 'SMA_20', 'SMA_50', 'Average_True_Range_14',
        'Upperband', 'Middleband', 'Lowerband', 'Bandwidth', 'Percent_Column_BBands']]

# Target variables
y = df_30min["Long_short_0.01"]

def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
    cls = SVC().fit(X, y)
    return cls
    pass

def save(path: str) -> None:
    pass

def load(path: str) -> None:
    pass




