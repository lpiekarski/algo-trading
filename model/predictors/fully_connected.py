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
import torch.nn.functional as F

LOGGER = logging.getLogger(__name__)


class Head(nn.Module):
    def __init__(self, in_features, out_features, dropout=0.5):
        super(Head, self).__init__()
        self.fc = nn.Linear(in_features, out_features)
        self.drop = nn.Dropout(dropout)
        self.sigmoid = nn.ReLU()
        self.bn = nn.BatchNorm1d(out_features)

    def forward(self, x):
        x = self.fc(x)
        x = self.drop(x)
        x = self.sigmoid(x)
        x = self.bn(x)
        return x


class ResidualHead(nn.Module):
    def __init__(self, features, dropout=0.5):
        super(ResidualHead, self).__init__()
        self.head = Head(features, features, dropout)

    def forward(self, x):
        return self.head(x) + x


def head(in_features, out_features, dropout=0.5):
    if in_features == out_features:
        return ResidualHead(in_features, dropout)
    else:
        return Head(in_features, out_features, dropout)


class FocalLoss(nn.Module):
    def __init__(self, gamma=2, weight=None):
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.weight = weight

    def forward(self, input, target):
        logpt = F.log_softmax(input, dim=1)
        pt = torch.exp(logpt)
        logpt = (1 - pt)**self.gamma * logpt
        loss = F.nll_loss(logpt, target, self.weight)
        return loss


model: nn.Sequential = None
preprocessor: Preprocessor = None
params: dict = dict()


def initialize(num_features: int, config_json: Any) -> None:
    global model, preprocessor, params
    if config_json is not None:
        architecture = config_json['architecture']
        layers = [head(num_features, architecture[0])]
        prev_size = architecture[0]
        for size in range(1, len(architecture)):
            layers.append(head(prev_size, size))
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
        FocalLoss(),
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
