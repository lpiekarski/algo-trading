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


def initialize(num_features: int, config_json: Any) -> None:
    global model, preprocessor, params
    if config_json is not None:
        layers = []
        for layer_config in config_json['architecture']:
            layer_name = layer_config.pop(0)
            layers.append(getattr(nn, layer_name)(
                *list(map(lambda x: x if x is not None else num_features, layer_config))))
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
