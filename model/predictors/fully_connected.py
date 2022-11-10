import torch.optim as optim
import torch
from torch import nn
import pandas as pd
import numpy as np
import logging
import os
from commons import pytorch
from commons.data.preprocessor import Preprocessor

LOGGER = logging.getLogger(__name__)

model: nn.Module = None
preprocessor: Preprocessor = None

def model_definition(preprocessor):
    return nn.Sequential(
        nn.Linear(preprocessor.num_features, 128),
        nn.Sigmoid(),
        nn.BatchNorm1d(128),
        nn.Linear(128, 128),
        nn.Dropout(0.5),
        nn.Sigmoid(),
        nn.BatchNorm1d(128),
        nn.Linear(128, 128),
        nn.Dropout(0.5),
        nn.Sigmoid(),
        nn.BatchNorm1d(128),
        nn.Linear(128, 128),
        nn.Dropout(0.5),
        nn.Sigmoid(),
        nn.BatchNorm1d(128),
        nn.Linear(128, 128),
        nn.Dropout(0.5),
        nn.Sigmoid(),
        nn.BatchNorm1d(128),
        nn.Linear(128, 128),
        nn.Dropout(0.5),
        nn.Sigmoid(),
        nn.BatchNorm1d(128),
        nn.Linear(128, 128),
        nn.Dropout(0.5),
        nn.Sigmoid(),
        nn.BatchNorm1d(128),
        nn.Linear(128, 128),
        nn.Dropout(0.5),
        nn.Sigmoid(),
        nn.BatchNorm1d(128),
        nn.Linear(128, 64),
        nn.Dropout(0.5),
        nn.Sigmoid(),
        nn.BatchNorm1d(64),
        nn.Linear(64, 32),
        nn.Dropout(0.5),
        nn.Sigmoid(),
        nn.BatchNorm1d(32),
        nn.Linear(32, 1),
        nn.Sigmoid()
    )

def predict(x: pd.DataFrame) -> np.ndarray:
    model.eval()
    return model.forward(torch.tensor(preprocessor.apply(x).to_numpy().astype(np.float32))).detach().numpy()

def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    global model, preprocessor
    preprocessor = Preprocessor()
    preprocessor.fit(x)
    model = model_definition(preprocessor)
    pytorch.train(
        model,
        preprocessor.apply(x).to_numpy().astype(np.float32),
        y.to_numpy().astype(np.float32),
        nn.BCELoss(),
        optim.Adam(model.parameters(), weight_decay=0.1),
        n_epochs=100,
        batch_size=256,
        metrics={
            'accuracy': lambda y_pred, y_true: (np.round(y_pred) == y_true).sum() / len(y_true)
        }
    )

def save(path: str) -> None:
    torch.save(model.state_dict(), os.path.join(path, 'model'))
    preprocessor.save(os.path.join(path, 'preprocessor'))

def load(path: str) -> None:
    global model, preprocessor
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
    model = model_definition(preprocessor)
    model.load_state_dict(torch.load(os.path.join(path, 'model')))
    model.eval()
