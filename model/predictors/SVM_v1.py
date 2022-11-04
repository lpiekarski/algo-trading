import pandas as pd
import numpy as np

# other
from sklearn.svm import SVC

model = None

# data edit
def predictors(x: pd.DataFrame):
    predictors = x[['Open', 'High']]
    return predictors.copy()

def data_edit(x: pd.DataFrame):
    x['Open'] = x['Open'] * 2

def predict(x: pd.DataFrame) -> np.ndarray:
    x = predictors(x)
    data_edit(x)
    return model.predict(x)

def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    global model
    x = predictors(x)
    data_edit(x)
    model = SVC().fit(x, y)

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
