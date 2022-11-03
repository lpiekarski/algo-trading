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








"""
#model: SVM_v1 = None
df = pd.read_csv('M1.csv', index_col=0, dayfirst=True, parse_dates=True)
add_labels(df)
pint(df)


#### Create predictor variables
df_30min['Open-Close'] = df_30min.Open - df_30min.Close
df_30min['High-Low'] = df_30min.High - df_30min.Low

# RSI
df_30min['Rsi_14'] = pta.rsi(df_30min['Close'], length=14)
df_30min['Rsi_26'] = pta.rsi(df_30min['Close'], length=26)

# SMA
df_30min['SMA_10'] = pta.sma(df_30min["Close"], length=10)
df_30min['SMA_20'] = pta.sma(df_30min["Close"], length=20)
df_30min['SMA_50'] = pta.sma(df_30min["Close"], length=50)

# Average True Range
df_30min['Average_True_Range_14'] = pta.atr(df_30min['High'], df_30min['Low'], df_30min['Close'], length=14)

# Bolinger Bands
bbands_result = pta.bbands(df_30min["Close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
df_30min['Upperband'] = bbands_result['BBL_5_2.0']
df_30min['Middleband'] = bbands_result['BBM_5_2.0']
df_30min['Lowerband'] = bbands_result['BBU_5_2.0']
df_30min['Bandwidth'] = bbands_result['BBB_5_2.0']
df_30min['Percent_Column_BBands'] = bbands_result['BBP_5_2.0']

# Store all predictor variables in a variable X
X = df_30min[['Open-Close', 'High-Low', 'Rsi_14', 'Rsi_26', 'SMA_10', 'SMA_20', 'SMA_50', 'Average_True_Range_14',
        'Upperband', 'Middleband', 'Lowerband', 'Bandwidth', 'Percent_Column_BBands']]
X.head()

# Target variables
y = df_30min["Long_short_0.01"]


split_percentage = 0.8
split = int(split_percentage * len(df))

# Train data set
X_train = X[:split]
y_train = y[:split]

# Test data set
X_test = X[split:]
y_test = y[split:]

''''''
# Support vector classifier
cls = SVC().fit(X_train, y_train)

def predict(X:pd.DataFrame) -> np.ndarray:
    cls = SVC().fit(X_train, y_train)
    return cls



def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
#    global model
#    if model is None:
#        model = lgbm.Booster(train_set=lgbm.Dataset(X.drop(['Date'], axis=1), y))
#    else:
#        model.refit(X.drop(['Date'], axis=1), y)




def save(path: str) -> None:
#    model.save_model(path)





def load(path: str) -> None:
#    global model
#    model = lgbm.Booster(model_file=path)
"""