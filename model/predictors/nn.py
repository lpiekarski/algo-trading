from typing import Dict

import torch.optim as optim
import torch
import sys
from torch import nn
import pandas as pd
import numpy as np
import logging
import os

from torch.utils.data import TensorDataset, DataLoader
from tqdm import tqdm

import core.torch as pytorch
from core.data.preprocessor import Preprocessor
import core.data.utils as metric_source
import core.torch.modules as commons_modules
from core.exceptions import AtfError

LOGGER = logging.getLogger(__name__)


model: commons_modules.GraphNN | None = None
preprocessor: Preprocessor | None = None
params: dict = dict()
optimizer: str | None = None
optimizer_params: dict | None = None
loss_fn: nn.Module | None = None
metrics: Dict[str, str] | None = None


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
    global model, preprocessor, params, optimizer, optimizer_params, loss_fn, metrics
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
    optimizer = config["optimizer"]
    optimizer_params = config["optimizer_params"]
    if hasattr(commons_modules, config["loss"]):
        loss_fn = getattr(commons_modules, config["loss"])
    elif hasattr(nn, config["loss"]):
        loss_fn = getattr(nn, config["loss"])
    else:
        raise AtfError(f"Invalid loss {config['loss']}")
    metrics = config["metrics"]


def get_result(src, tgt, device):
    src = src.to(device).swapdims(0, 1)
    tgt = tgt.to(device).swapdims(0, 1)
    src[src.isnan()] = 0
    output = model.forward(src, tgt)[0]
    output = output[-1]
    return output.detach().cpu().numpy()


def predict(x: pd.DataFrame, y: pd.DataFrame) -> np.ndarray:
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    model.to(device)
    model.eval()
    with torch.no_grad():
        if preprocessor.rolling_window is not None:
            x, y = preprocessor.apply(x, y, apply_rolling_window=False)
            x = torch.tensor(x.astype(np.float32))
            y = torch.tensor(y.astype(np.float32))
            inputs = []
            result = []
            srcs = []
            tgts = []
            for i in tqdm(range(x.shape[0])):
                inputs.append(x[i])
                if len(inputs) > preprocessor.rolling_window:
                    inputs.pop(0)
                init_tensor = torch.ones(1, y.shape[1])
                init_tensor = init_tensor / init_tensor.sum() if y.shape[1] > 1 else init_tensor / 2
                outputs = torch.cat([init_tensor, y[:i]])
                if outputs.shape[0] > preprocessor.rolling_window:
                    outputs = outputs[-preprocessor.rolling_window:]
                src = torch.stack(inputs)
                src = src.view(1, src.shape[0], src.shape[1])
                tgt = outputs
                tgt = tgt.view(1, tgt.shape[0], tgt.shape[1])
                if len(srcs) > 0 and (src.shape != srcs[0].shape or tgt.shape !=
                                      tgts[0].shape or len(srcs) >= params["batch_size"]):
                    result.append(get_result(torch.cat(srcs), torch.cat(tgts), device))
                    srcs = []
                    tgts = []
                srcs.append(src)
                tgts.append(tgt)
            if len(srcs) > 0:
                result.append(get_result(torch.cat(srcs), torch.cat(tgts), device))

            return np.concatenate(result, axis=0)
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
    metrics_dict = {
        k: getattr(metric_source, v)
        for k, v in metrics.items()
    }
    preprocessor.fit(x)
    x, y = preprocessor.apply(x, y)
    pytorch.train(
        model,
        x,
        y,
        loss_fn(reduction="none"),
        getattr(optim, optimizer)(model.parameters(), **optimizer_params),
        n_epochs=params['n_epochs'],
        batch_size=params['batch_size'],
        metrics=metrics_dict,
        train_test_split=params["train_test_split"]
    )


def save_weights(path: str) -> None:
    torch.save(model.state_dict(), os.path.join(path, 'model'))
    preprocessor.save(os.path.join(path, 'preprocessor'))


def load_weights(path: str) -> None:
    global model, preprocessor
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))
    model.load_state_dict(torch.load(os.path.join(path, 'model'), map_location=device))
