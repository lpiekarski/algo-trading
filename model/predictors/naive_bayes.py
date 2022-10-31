from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np
import os
import pickle
from commons.data.preprocessor import Preprocessor

model: GaussianNB = None
preprocessor: Preprocessor = None

def predict(x: pd.DataFrame) -> np.ndarray:
    return model.predict_proba(preprocessor.apply(x))[:, 1]

def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    global model, preprocessor
    preprocessor = Preprocessor()
    preprocessor.fit(x)
    model = GaussianNB()
    model.fit(preprocessor.apply(x), y)

def save(path: str) -> None:
    with open(os.path.join(path, 'model'), 'wb') as file:
        pickle.dump(model, file)
    preprocessor.save(os.path.join(path, 'preprocessor'))

def load(path: str) -> None:
    global model, preprocessor
    with open(os.path.join(path, 'model'), 'rb') as file:
        model = pickle.load(file)
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
