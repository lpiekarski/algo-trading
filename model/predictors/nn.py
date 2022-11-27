import torch.optim as optim
import torch
import sys
from torch import nn
import pandas as pd
import numpy as np
import logging
import os
import commons.torch as pytorch
from commons.data.preprocessor import Preprocessor
from commons.data.utils import accuracy, precision, recall
import commons.torch.modules as commons_modules
from commons.exceptions import AtfError

LOGGER = logging.getLogger(__name__)


model: nn.Sequential = None
preprocessor: Preprocessor = None
params: dict = dict()


def has_nested_attr(_obj, _nested_attr):
    if '.' not in _nested_attr:
        return hasattr(_obj, _nested_attr)
    _attr, rest = _nested_attr.split('.', 1)
    if hasattr(_obj, _attr):
        return has_nested_attr(getattr(_obj, _attr), rest)
    else:
        return False


def get_nested_attr(_obj, _nested_attr):
    if '.' not in _nested_attr:
        return getattr(_obj, _nested_attr)
    _attr, rest = _nested_attr.split('.', 1)
    return get_nested_attr(getattr(_obj, _attr), rest)


def initialize(num_features: int, config: dict) -> None:
    global model, preprocessor, params
    if config is None:
        raise AtfError("Config file not provided")
    architecture = config['architecture']
    modules = []
    connections = []
    for layer in architecture:
        _from = layer[0]
        _module = layer[1]
        _args = layer[2]
        connections.append(_from)
        if has_nested_attr(commons_modules, _module):
            source = commons_modules
        elif has_nested_attr(nn, _module):
            source = nn
        elif has_nested_attr(sys.modules[__name__], _module):
            source = sys.modules[__name__]
        else:
            raise AtfError(f"Module not found '{_module}'")
        if isinstance(_args, list):
            modules.append(get_nested_attr(source, _module)(
                *list(map(lambda x: x if x is not None else num_features, _args))))
        elif isinstance(_args, dict):
            modules.append(get_nested_attr(source, _module)(
                **dict(map(lambda kv: (kv[0], kv[1]) if kv[1] is not None else (kv[0], num_features), _args))))
        else:
            raise AtfError(f"Invalid module arguments type for '{_module}'")
    model = commons_modules.GraphNN(connections, modules)
    params = config['hyperparams']
    ppargs = config['preprocessor']
    if isinstance(ppargs, list):
        preprocessor = Preprocessor(*ppargs, num_features=num_features)
    elif isinstance(ppargs, dict):
        preprocessor = Preprocessor(**ppargs, num_features=num_features)
    else:
        raise AtfError(f"Invalid preprocessor arguments type")


def predict(x: pd.DataFrame) -> np.ndarray:
    model.eval()
    return model.forward(
        torch.tensor(
            preprocessor.apply(x).to_numpy().astype(
                np.float32))).detach().numpy()


def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    sample_weights = np.flipud(np.power(params['sample_weight_ratio'], np.arange(x.shape[0]))).astype(np.float32)
    preprocessor.fit(x)
    pytorch.train(
        model,
        preprocessor.apply(x).to_numpy().astype(np.float32),
        y.to_numpy().astype(np.float32),
        nn.BCELoss(),
        optim.Adam(model.parameters(), weight_decay=params['weight_decay']),
        n_epochs=params['n_epochs'],
        batch_size=params['batch_size'],
        metrics=dict(
            accuracy=accuracy,
            precision=precision,
            recall=recall
        ),
        sample_weights=sample_weights.copy()
    )


def save_weights(path: str) -> None:
    torch.save(model.state_dict(), os.path.join(path, 'model'))
    preprocessor.save(os.path.join(path, 'preprocessor'))


def load_weights(path: str) -> None:
    global model, preprocessor
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
    model.load_state_dict(torch.load(os.path.join(path, 'model')))
