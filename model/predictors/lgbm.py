import pandas as pd
import numpy as np
import lightgbm as lgbm
from model.preprocessing import Preprocessor
import os

model: lgbm.Booster = None
preprocessor: Preprocessor = None

def predict(X: pd.DataFrame) -> np.ndarray:
    return model.predict(preprocessor.apply(X), predict_disable_shape_check=True)

def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
    global model, preprocessor
    if model is None or preprocessor is None:
        preprocessor = Preprocessor()
        preprocessor.fit(X)
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
        cls.fit(preprocessor.apply(X), y)
        model = cls.booster_
    else:
        preprocessor.fit(X)
        model.refit(preprocessor.apply(X), y)

def save(path: str) -> None:
    model.save_model(os.path.join(path, 'model'))
    preprocessor.save(os.path.join(path, 'preprocessor'))

def load(path: str) -> None:
    global model, preprocessor
    model = lgbm.Booster(model_file=os.path.join(path, 'model'))
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
