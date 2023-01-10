import torch.optim as optim
import torch
import sys
from torch import nn
import pandas as pd
import numpy as np
import logging
import os
from tqdm import tqdm

from torch.utils.data import TensorDataset, DataLoader

import core.torch as pytorch
from core.data.preprocessor import Preprocessor
from core.data.utils import accuracy, precision, recall, balanced_accuracy
import core.torch.modules as commons_modules
from core.exceptions import AtfError

LOGGER = logging.getLogger(__name__)


model: commons_modules.GraphNN = None
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
    LOGGER.info(model)
    num_parameters = sum(p.numel() for p in model.parameters() if p.requires_grad)
    LOGGER.info(f"Number of trainable parameters: {num_parameters}")
    params = config['hyperparams']
    ppargs = config['preprocessor']
    if isinstance(ppargs, list):
        preprocessor = Preprocessor(*ppargs, num_features=num_features)
    elif isinstance(ppargs, dict):
        preprocessor = Preprocessor(**ppargs, num_features=num_features)
    else:
        raise AtfError(f"Invalid preprocessor arguments type")


def predict(x: pd.DataFrame) -> np.ndarray:
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    model.to(device)
    model.eval()
    if preprocessor.rolling_window is not None:
        x = torch.tensor(preprocessor.apply(x, apply_rolling_window=False).astype(np.float32))
        inputs = []
        outputs = [0.5]
        result = []
        for i in tqdm(range(x.shape[0])):
            inputs.append(x[i])
            if len(inputs) > preprocessor.rolling_window:
                inputs.pop(0)
            src = torch.stack(inputs).to(device)
            src = src.view(src.shape[0], 1, src.shape[1])
            tgt = torch.tensor(outputs, dtype=torch.float32, device=device)
            tgt = tgt.view(tgt.shape[0], 1, 1)
            output = model.forward(src, tgt)
            output = output.flatten()
            result.append(output[-1].detach().cpu().item())
            outputs.append(output[-1].detach().cpu().item())
            if len(outputs) > preprocessor.rolling_window:
                outputs.pop(0)
        return np.array(result)
    else:
        cuda_kwargs = {'num_workers': 1,
                       'pin_memory': True}
        x = torch.tensor(preprocessor.apply(x).astype(np.float32))
        torch_dataset = TensorDataset(x)
        loader = DataLoader(torch_dataset, shuffle=False, batch_size=params['batch_size'], **cuda_kwargs)
        outputs = []
        for idx, (inputs,) in enumerate(loader):
            inputs = inputs.to(device)
            output = model.forward(inputs).detach().cpu().numpy()
            outputs.append(output.squeeze())
        return np.concatenate(outputs, axis=0)


def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    preprocessor.fit(x)
    x, y = preprocessor.apply(x, y)
    sample_weights = np.flipud(np.power(params['sample_weight_ratio'], np.arange(x.shape[0]))).astype(np.float32)
    pytorch.train(
        model,
        x,
        y,
        nn.BCELoss(reduction="none"),
        optim.Adam(model.parameters(), weight_decay=params['weight_decay']),
        n_epochs=params['n_epochs'],
        batch_size=params['batch_size'],
        metrics=dict(
            acc=accuracy,
            b_acc=balanced_accuracy,
            p=precision,
            r=recall
        ),
        sample_weights=sample_weights
    )


def save_weights(path: str) -> None:
    torch.save(model.state_dict(), os.path.join(path, 'model'))
    preprocessor.save(os.path.join(path, 'preprocessor'))


def load_weights(path: str) -> None:
    global model, preprocessor
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
    model.load_state_dict(torch.load(os.path.join(path, 'model')))
