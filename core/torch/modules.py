import copy
import math
from typing import List

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

    def forward(self, x):
        results = {-1: x}
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


class EncoderDecoder(nn.Module):
    def __init__(self, encoder: nn.Module, decoder: nn.Module, src_embed: nn.Module, tgt_embed: nn.Module, generator: nn.Module):
        """
        :param encoder: Encoder module
        :param decoder: Decoder module
        :param src_embed: Source embeddings
        :param tgt_embed: Target embeddings
        :param generator: Output generator
        """
        super(EncoderDecoder, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.src_embed = src_embed
        self.tgt_embed = tgt_embed
        self.generator = generator

    def forward(self, src: torch.Tensor) -> torch.Tensor:
        """
        Take in and process masked src and target sequences.
        :param src: shape (seq, batch, d_model)
        :return:
        """
        src_mask = torch.ones(1, src.shape[0], src.shape[0]).to(src.device)
        tgt = torch.zeros_like(src).to(src.device)
        tgt_mask = subsequent_mask(tgt.size(0)).to(src.device)
        memory = self.encode(src, src_mask)
        output = self.decode(memory, src_mask, tgt, tgt_mask)
        return self.generator(output)

    def encode(self, src: torch.Tensor, src_mask: torch.Tensor) -> torch.Tensor:
        return self.encoder(self.src_embed(src), src_mask)

    def decode(self, memory: torch.Tensor, src_mask: torch.Tensor, tgt: torch.Tensor, tgt_mask: torch.Tensor) -> torch.Tensor:
        return self.decoder(self.tgt_embed(tgt), memory, src_mask, tgt_mask)


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


def clones(module: nn.Module, n: int) -> nn.ModuleList:
    """
    Produce n identical layers.
    """
    return nn.ModuleList([copy.deepcopy(module) for _ in range(n)])


class Encoder(nn.Module):
    """
    Core encoder is a stack of n layers
    """

    def __init__(self, layer: nn.Module, n: int):
        super(Encoder, self).__init__()
        self.layers = clones(layer, n)
        self.norm = LayerNorm(layer.size)

    def forward(self, x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        """
        Pass the input (and mask) through each layer in turn.
        :param x: shape (seq, batch, d_model)
        :param mask: shape (1, seq, seq)
        :return:
        """
        for layer in self.layers:
            x = layer(x, mask)
        return self.norm(x)


class LayerNorm(nn.Module):
    """
    Construct a layer-norm module.
    """

    def __init__(self, features: int, eps: float = 1e-6):
        super(LayerNorm, self).__init__()
        self.a_2 = nn.Parameter(torch.ones(features))
        self.b_2 = nn.Parameter(torch.zeros(features))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True)
        return self.a_2 * (x - mean) / (std + self.eps) + self.b_2


class SublayerConnection(nn.Module):
    """
    A residual connection followed by a layer norm.
    Note for code simplicity the norm is first as opposed to last.
    """

    def __init__(self, size: int, dropout: float):
        super(SublayerConnection, self).__init__()
        self.norm = LayerNorm(size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor, sublayer: nn.Module) -> torch.Tensor:
        """
        Apply residual connection to any sublayer with the same size.
        """
        return x + self.dropout(sublayer(self.norm(x)))


class EncoderLayer(nn.Module):
    """
    Encoder is made up of self-attn and feed forward (defined below)
    """

    def __init__(self, size: int, self_attn: nn.Module, feed_forward: nn.Module, dropout: float):
        super(EncoderLayer, self).__init__()
        self.self_attn = self_attn
        self.feed_forward = feed_forward
        self.sublayer = clones(SublayerConnection(size, dropout), 2)
        self.size = size

    def forward(self, x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))
        return self.sublayer[1](x, self.feed_forward)


class Decoder(nn.Module):
    """
    Generic N layer decoder with masking.
    """

    def __init__(self, layer: nn.Module, n: int):
        super(Decoder, self).__init__()
        self.layers = clones(layer, n)
        self.norm = LayerNorm(layer.size)

    def forward(self, x: torch.Tensor, memory: torch.Tensor, src_mask: torch.Tensor, tgt_mask: torch.Tensor):
        for layer in self.layers:
            x = layer(x, memory, src_mask, tgt_mask)
        return self.norm(x)


class DecoderLayer(nn.Module):
    """
    Decoder is made of self-attn, src-attn, and feed forward (defined below)
    """

    def __init__(self, size: int, self_attn: nn.Module, src_attn: nn.Module, feed_forward: nn.Module, dropout: float):
        super(DecoderLayer, self).__init__()
        self.size = size
        self.self_attn = self_attn
        self.src_attn = src_attn
        self.feed_forward = feed_forward
        self.sublayer = clones(SublayerConnection(size, dropout), 3)

    def forward(self, x: torch.Tensor, memory: torch.Tensor, src_mask: torch.Tensor, tgt_mask: torch.Tensor) -> torch.Tensor:
        m = memory
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, tgt_mask))
        x = self.sublayer[1](x, lambda x: self.src_attn(x, m, m, src_mask))
        return self.sublayer[2](x, self.feed_forward)


def subsequent_mask(size: int) -> torch.Tensor:
    """Mask out subsequent positions."""
    attn_shape = (1, size, size)
    return torch.triu(torch.ones(attn_shape), diagonal=1).type(torch.uint8) == 0


def attention(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, mask: torch.Tensor = None, dropout: nn.Module = None):
    """
    Compute 'Scaled Dot Product Attention'
    :param query: shape (seq, h, batch, d_k)
    :param key: shape (seq, h, batch, d_k)
    :param value: shape (seq, h, batch, d_k)
    :param mask: shape (1, 1, seq, seq)
    :param dropout:
    :return: shape (batch, h, seq, d_k)
    """
    d_k = query.size(-1)
    query = query.swapdims(0, 2)  # shape (batch, h, seq, d_k)
    key = key.swapdims(0, 2)  # shape (batch, h, seq, d_k)
    value = value.swapdims(0, 2)  # shape (batch, h, seq, d_k)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)  # shape (batch, h, seq, seq)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    p_attn = scores.softmax(dim=-1)  # shape (batch, h, seq, seq)
    if dropout is not None:
        p_attn = dropout(p_attn)
    return torch.matmul(p_attn, value), p_attn


class MultiHeadedAttention(nn.Module):
    def __init__(self, h: int, d_model: int, dropout: float = 0.1):
        """
        Take in model size and number of heads.
        """
        super(MultiHeadedAttention, self).__init__()
        assert d_model % h == 0
        # We assume d_v always equals d_k
        self.d_k = d_model // h
        self.h = h
        self.linears = clones(nn.Linear(d_model, d_model), 4)
        self.attn = None
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, mask: torch.Tensor = None):
        """
        :param query: shape (seq, batch, d_model)
        :param key: shape (seq, batch, d_model)
        :param value: shape (seq, batch, d_model)
        :param mask: shape (1, seq, seq)
        :return: shape (seq, batch, d_model)
        """
        if mask is not None:
            # Same mask applied to all h heads.
            mask = mask.unsqueeze(1)

        # 1) Do all the linear projections in batch from d_model => h x d_k
        query, key, value = [
            lin(x).view(query.size(0), -1, self.h, self.d_k).transpose(1, 2)
            for lin, x in zip(self.linears, (query, key, value))
        ]  # shape: (seq, h, batch, d_k)

        # 2) Apply attention on all the projected vectors in batch.
        x, self.attn = attention(
            query, key, value, mask=mask, dropout=self.dropout
        )  # shape (batch, h, seq, d_k)

        # 3) "Concat" using a view and apply a final linear.
        x = (
            x.transpose(1, 2)  # (batch, seq, h, d_k)
            .contiguous()
            .view(query.size(0), -1, self.h * self.d_k)
        )  # shape (seq, batch, d_model)
        del query
        del key
        del value
        return self.linears[-1](x)


class PositionWiseFeedForward(nn.Module):
    """
    Implements FFN equation.
    """

    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super(PositionWiseFeedForward, self).__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.w_2(self.dropout(self.w_1(x).relu()))


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
        self.register_buffer("pe", pe)

    def forward(self, x):
        x = x + self.pe[:, : x.size(1)].requires_grad_(False)
        return self.dropout(x)


class Transformer(EncoderDecoder):
    def __init__(self,
                 num_classes: int,
                 encoder_layers: int = 6,
                 decoder_layers: int = 6,
                 d_model: int = 512,
                 d_ff: int = 2048,
                 num_heads: int = 8,
                 dropout: float = 0.1
                 ):
        """
        Helper: Construct a model from hyperparameters.
        :param num_classes: Number of output classes.
        :param encoder_layers: Number of encoder layers.
        :param decoder_layers: Number of decoder layers.
        :param d_model: Size of the model dimension.
        :param d_ff: Size of the feed-forward hidden dimension.
        :param num_heads: Number of attention heads.
        :param dropout: dropout rate.
        :return: Encoder-Decoder model.
        """
        c = copy.deepcopy
        attn = MultiHeadedAttention(num_heads, d_model)
        ff = PositionWiseFeedForward(d_model, d_ff, dropout)
        position = PositionalEncoding(d_model, dropout)
        super().__init__(
            Encoder(EncoderLayer(d_model, c(attn), c(ff), dropout), encoder_layers),
            Decoder(DecoderLayer(d_model, c(attn), c(attn), c(ff), dropout), decoder_layers),
            c(position),
            c(position),
            BinaryClassificationGenerator(d_model)
        )
