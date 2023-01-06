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


class ClassificationGenerator(nn.Module):
    """
    Standard output generator for classification problems:
    linear layer + softmax
    """

    def __init__(self, d_model: int, num_classes):
        super(ClassificationGenerator, self).__init__()
        self.proj = nn.Linear(d_model, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.nn.functional.log_softmax(self.proj(x), dim=-1)


class BinaryClassificationGenerator(nn.Module):
    """
    Standard output generator for binary classification problems:
    linear layer + sigmoid activation
    """

    def __init__(self, d_model: int):
        super(BinaryClassificationGenerator, self).__init__()
        self.proj = nn.Linear(d_model, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(self.proj(x))


class PositionalEncoding(nn.Module):
    """
    Implement the PE function.
    """

    def __init__(self, d_model: int, dropout: float, max_len: int = 5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        # Compute the positional encodings once in log space.
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        pe = pe.swapdims(0, 1)
        self.register_buffer("pe", pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0)].requires_grad_(False)
        return self.dropout(x)


class TorchBinaryTransformer(nn.Module):
    def __init__(self, encoder_layers: int = 6, decoder_layers: int = 6, d_model: int = 512,
                 d_ff: int = 2048, num_heads: int = 8, dropout: float = 0.1):
        """
        Helper: Construct a model from hyperparameters.
        :param encoder_layers: Number of encoder layers.
        :param decoder_layers: Number of decoder layers.
        :param d_model: Size of the model dimension.
        :param d_ff: Size of the feed-forward hidden dimension.
        :param num_heads: Number of attention heads.
        :param dropout: dropout rate.
        :return: Encoder-Decoder model.
        """
        super().__init__()
        self.transformer = nn.Transformer(
            d_model=d_model,
            dim_feedforward=d_ff,
            dropout=dropout,
            num_decoder_layers=decoder_layers,
            num_encoder_layers=encoder_layers,
            norm_first=True,
            nhead=num_heads,
            batch_first=False
        )
        self.generator = BinaryClassificationGenerator(d_model)
        self.src_embed = PositionalEncoding(d_model, dropout)
        self.tgt_embed = PositionalEncoding(d_model, dropout)

    def forward(self, src: torch.Tensor, tgt: torch.Tensor):
        src_mask = torch.ones(src.shape[0], src.shape[0]).to(src.device)
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt.size(0), src.device)
        src = self.src_embed(src)
        tgt = self.tgt_embed(tgt)
        output = self.transformer.forward(src, tgt, src_mask, tgt_mask)
        return self.generator(output)
