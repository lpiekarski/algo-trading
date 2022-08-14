import pandas as pd
import numpy as np

def predict(X):
    df = pd.DataFrame()
    df["y"] = np.zeros_like(X["Close"])
    return df


def train(X, y):
    pass