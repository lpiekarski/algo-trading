import copy
import math
from typing import List, Tuple

import torch.nn as nn
import torch
import numpy as np


class Linear(nn.Module):
    """
    Linear block consisting of linear transformation, dropout, sigmoid and batch normalisation.
    """

    def __init__(self, in_features: int, out_features: int, dropout: float = 0.5):
        """
        Net initialization.
        :param in_features: Size of the input dimension.
        :param out_features: Size of the output dimension.
        :param dropout: Dropout rate.
        """
        super(Linear, self).__init__()
        self.fc = nn.Linear(in_features, out_features)
        self.drop = nn.Dropout(dropout)
        self.sigmoid = nn.ReLU()
        self.bn = nn.BatchNorm1d(out_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward method of the net.
        :param x: Input of shape (B, in_features)
        :return: Output of shape (B, out_features)
        """
        x = self.fc(x)
        x = self.drop(x)
        x = self.sigmoid(x)
        x = self.bn(x)
        return x


class LinearResidual(nn.Module):
    """
    Linear block with residual connection.
    """

    def __init__(self, in_out_features: int, dropout: float = 0.5):
        """
        Net initialization.
        :param in_out_features: Size of the input and output dimension.
        :param dropout: Dropout rate.
        """
        super(LinearResidual, self).__init__()
        self.lin = Linear(in_out_features, in_out_features, dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward method of the net.
        :param x: Input of shape (B, in_out_features)
        :return: Output of shape (B, in_out_features)
        """
        return self.lin(x) + x


class GraphNN(nn.Module):
    def __init__(self, connections, modules: [nn.Module]):
        super(GraphNN, self).__init__()
        self.connections = []
        self.last_occurrence = dict()
        for idx, _from in enumerate(connections):
            if isinstance(_from, list):
                self.connections.append(list(map(lambda k: k if k >= 0 else idx + k, _from)))
            else:
                self.connections.append(_from if _from >= 0 else idx + _from)
        for i in reversed(range(len(self.connections))):
            _from = self.connections[i]
            if isinstance(_from, list):
                for k in _from:
                    if k not in self.last_occurrence:
                        self.last_occurrence[k] = i
            elif _from not in self.last_occurrence:
                self.last_occurrence[_from] = i
        self.nodes = nn.ModuleList(modules)

    def forward(self, *inputs):
        results = {-(idx + 1): x for idx, x in enumerate(inputs)}
        for idx, (_from, _module) in enumerate(list(zip(self.connections, self.nodes))):
            if isinstance(_from, list):
                results[idx] = _module.forward(*list(map(lambda k: results[k], _from)))
                for _f in _from:
                    if self.last_occurrence[_f] == idx:
                        del results[_f]
            else:
                results[idx] = _module.forward(results[_from])
                if self.last_occurrence[_from] == idx:
                    del results[_from]
        return results[len(self.nodes) - 1]
