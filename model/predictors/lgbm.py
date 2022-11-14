import pandas as pd
import numpy as np
import lightgbm as lgbm
import os

from commons.data.preprocessor import Preprocessor

model: lgbm.Booster = None
preprocessor: Preprocessor = None


def initialize(config_path: str) -> None:
    pass


def predict(x: pd.DataFrame) -> np.ndarray:
    return model.predict(
        preprocessor.apply(x),
        predict_disable_shape_check=True)


def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    global model, preprocessor
    preprocessor = Preprocessor()
    preprocessor.fit(x)
    cls = lgbm.LGBMClassifier(
        n_estimators=1000,
        reg_alpha=0.3,
        reg_lambda=0.02,
        objective='binary',
        num_leaves=127,
        learning_rate=0.5,
        subsample_for_bin=200000,
        min_child_samples=20
    )
    cls.fit(preprocessor.apply(x), y)
    model = cls.booster_


def save_weights(path: str) -> None:
    model.save_model(os.path.join(path, 'model'))
    preprocessor.save(os.path.join(path, 'preprocessor'))


def load_weights(path: str) -> None:
    global model, preprocessor
    model = lgbm.Booster(model_file=os.path.join(path, 'model'))
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
