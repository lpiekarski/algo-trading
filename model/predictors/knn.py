from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
import os
import pickle
from core.data.preprocessor import Preprocessor
from core.exceptions import AtfError

model: KNeighborsClassifier = None
preprocessor: Preprocessor = None


def initialize(num_features: int, config: dict) -> None:
    global model, preprocessor
    ppargs = config['preprocessor']
    if isinstance(ppargs, list):
        preprocessor = Preprocessor(*ppargs, num_features=num_features)
    elif isinstance(ppargs, dict):
        preprocessor = Preprocessor(**ppargs, num_features=num_features)
    else:
        raise AtfError(f"Invalid preprocessor arguments type")


def predict(x: pd.DataFrame) -> np.ndarray:
    return model.predict_proba(preprocessor.apply(x))[:, 1]


def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    global model
    preprocessor.fit(x)
    model = KNeighborsClassifier()
    model.fit(preprocessor.apply(x), y)


def save_weights(path: str) -> None:
    with open(os.path.join(path, 'model'), 'wb') as file:
        pickle.dump(model, file)
    preprocessor.save(os.path.join(path, 'preprocessor'))


def load_weights(path: str) -> None:
    global model, preprocessor
    with open(os.path.join(path, 'model'), 'rb') as file:
        model = pickle.load(file)
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
