import pandas as pd
import numpy as np
import lightgbm as lgbm

model: lgbm.Booster = None

def predict(X: pd.DataFrame) -> np.ndarray:
    return model.predict(X.drop(['Date', 'Datetime', 'time', 'Datetime.1'], axis=1), predict_disable_shape_check=True)

def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
    global model
    if model is None:
        model = lgbm.Booster(train_set=lgbm.Dataset(X.drop(['Date', 'Datetime', 'time', 'Datetime.1'], axis=1), y))
    else:
        model.refit(X.drop(['Date', 'Datetime', 'time', 'Datetime.1'], axis=1), y)

def save(path: str) -> None:
    model.save_model(path)

def load(path: str) -> None:
    global model
    model = lgbm.Booster(model_file=path)
