from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np
from model.preprocessing import Preprocessor
import os
import pickle

model: GaussianNB = None
preprocessor: Preprocessor = None

def predict(X: pd.DataFrame) -> np.ndarray:
    return model.predict_proba(preprocessor.apply(X))[:, 1]

def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
    global model, preprocessor
    if model is None or preprocessor is None:
        preprocessor = Preprocessor()
        preprocessor.fit(X)
        model = GaussianNB()
        model.fit(preprocessor.apply(X), y)
    else:
        preprocessor.fit(X)
        model.fit(preprocessor.apply(X), y)

def save(path: str) -> None:
    with open(os.path.join(path, 'model'), 'wb') as file:
        pickle.dump(model, file)
    preprocessor.save(os.path.join(path, 'preprocessor'))

def load(path: str) -> None:
    global model, preprocessor
    with open(os.path.join(path, 'model'), 'r') as file:
        model = pickle.load(file)
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
