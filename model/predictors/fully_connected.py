from typing import Any

import torch.optim as optim
import torch
from torch import nn
import pandas as pd
import numpy as np
import logging
import os
from commons import pytorch
from commons.data.preprocessor import Preprocessor
from commons.data.utils import accuracy

LOGGER = logging.getLogger(__name__)

model: nn.Module = None
preprocessor: Preprocessor = None
params: dict = dict()


def get_head(size_in, size_out):
    return [
        nn.Linear(size_in, size_out),
        nn.Dropout(0.5),
        nn.Sigmoid(),
        nn.BatchNorm1d(size_out)
    ]


def initialize(num_features: int, config_json: Any) -> None:
    global model, preprocessor, params
    if config_json is not None:
        arch = config_json['architecture']
        layers = get_head(num_features, arch[0])
        prev_size = arch[0]
        for size in range(1, len(arch)):
            layers.extend(get_head(prev_size, size))
            prev_size = size
        layers.append(nn.Linear(prev_size, 1))
        layers.append(nn.Sigmoid())
        model = nn.Sequential(*layers)
        params = config_json['hyperparams']
    preprocessor = Preprocessor(num_features=num_features)


def predict(x: pd.DataFrame) -> np.ndarray:
    model.eval()
    return model.forward(
        torch.tensor(
            preprocessor.apply(x).to_numpy().astype(
                np.float32))).detach().numpy()


def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    sample_weights = np.flipud(np.power(0.9999, np.arange(x.shape[0]))).astype(np.float32)
    preprocessor.fit(x)
    pytorch.train(
        model,
        preprocessor.apply(x).to_numpy().astype(np.float32),
        y.to_numpy().astype(np.float32),
        nn.BCELoss(),
        optim.Adam(model.parameters(), weight_decay=params['weight_decay']),
        n_epochs=params['n_epochs'],
        batch_size=params['batch_size'],
        metrics={'accuracy': accuracy},
        sample_weights=sample_weights.copy()
    )


def save_weights(path: str) -> None:
    torch.save(model.state_dict(), os.path.join(path, 'model'))
    preprocessor.save(os.path.join(path, 'preprocessor'))


def load_weights(path: str) -> None:
    global model, preprocessor
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
    model.load_state_dict(torch.load(os.path.join(path, 'model')))
