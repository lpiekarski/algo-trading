import torch.optim as optim
import torch
from torch import nn
import pandas as pd
import numpy as np
from tqdm import tqdm
import logging
import os

import commons
from commons import pytorch
from model.preprocessing import Preprocessor

LOGGER = logging.getLogger(__name__)

model: nn.Module = None
preprocessor: Preprocessor = None
n_epochs = 1000

def predict(X: pd.DataFrame) -> np.ndarray:
    return model.forward(torch.tensor(preprocessor.apply(X).to_numpy().astype(np.float32))).detach().numpy()

def train(X: pd.DataFrame, y: pd.DataFrame) -> None:
    global model, preprocessor
    if model is None or preprocessor is None:
        preprocessor = Preprocessor()
        preprocessor.fit(X)
        model = nn.Sequential(
            nn.Linear(X.shape[1], 1),
            nn.ReLU(),
            nn.Linear(1, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        pytorch.train(
            model,
            preprocessor.apply(X).to_numpy().astype(np.float32),
            y.to_numpy().astype(np.float32),
            nn.BCELoss(),
            optim.Adam(model.parameters()),
            n_epochs=100,
            batch_size=256,
            metrics={
                'accuracy': lambda y_pred, y_true: (np.round(y_pred) == y_true).sum() / len(y_true)
            }
        )
    else:
        preprocessor.fit(X)
        model.refit(preprocessor.apply(X), y)

def save(path: str) -> None:
    torch.save(model.state_dict(), os.path.join(path, 'model'))
    preprocessor.save(os.path.join(path, 'preprocessor'))

def load(path: str) -> None:
    global model, preprocessor
    model = nn.Module()
    model.load_state_dict(torch.load(os.path.join(path, 'model')))
    model.eval()
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
