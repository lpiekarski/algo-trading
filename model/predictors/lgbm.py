import pandas as pd
import numpy as np
import lightgbm as lgbm
import os

from core.data.preprocessor import Preprocessor
from core.exceptions import AtfError

model: lgbm.Booster = None
preprocessor: Preprocessor = None


def initialize(num_features: int, config: dict) -> None:
    global model, preprocessor, params
    params = config['hyperparams']
    ppargs = config['preprocessor']
    if isinstance(ppargs, list):
        preprocessor = Preprocessor(*ppargs, num_features=num_features)
    elif isinstance(ppargs, dict):
        preprocessor = Preprocessor(**ppargs, num_features=num_features)
    else:
        raise AtfError(f"Invalid preprocessor arguments type")


def predict(x: pd.DataFrame) -> np.ndarray:
    return model.predict(
        preprocessor.apply(x),
        predict_disable_shape_check=True)


def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    global model
    preprocessor.fit(x)
    cls = lgbm.LGBMClassifier(**params)
    cls.fit(preprocessor.apply(x), y)
    model = cls.booster_


def save_weights(path: str) -> None:
    model.save_model(os.path.join(path, 'model'))
    preprocessor.save(os.path.join(path, 'preprocessor'))


def load_weights(path: str) -> None:
    global model, preprocessor
    model = lgbm.Booster(model_file=os.path.join(path, 'model'))
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
