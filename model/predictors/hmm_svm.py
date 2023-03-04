from sklearn.svm import SVC
import pandas as pd
import numpy as np
import os
import pickle
from core.data.preprocessor import Preprocessor
import warnings
from ..utils.hmm import hmm_predict

model: SVC = None
preprocessor: Preprocessor = None


def initialize(num_features: int, config: dict) -> None:
    global preprocessor, model
    warnings.filterwarnings("ignore")
    model = SVC(C=0.5, kernel='rbf', degree=1, probability=True)


def predict(x: pd.DataFrame, y) -> np.ndarray:
    predict = hmm_predict(x)
    x = pd.concat([x, predict], axis=1)
    return model.predict_proba(preprocessor.apply(x))[:, 1]


def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    global model
    predict = hmm_predict(x)
    x = pd.concat([x, predict], axis=1)

    preprocessor.fit(x)
    model.fit(preprocessor.apply(x), y)  # sample_weight=weight


def save_weights(path: str) -> None:
    with open(os.path.join(path, 'model'), 'wb') as file:
        pickle.dump(model, file)
    preprocessor.save(os.path.join(path, 'preprocessor'))


def load_weights(path: str) -> None:
    global model, preprocessor
    with open(os.path.join(path, 'model'), 'rb') as file:
        model = pickle.load(file)
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
