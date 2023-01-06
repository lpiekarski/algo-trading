import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm
import numpy as np
import logging
import pandas as pd

LOGGER = logging.getLogger(__name__)


def weighted_loss(loss_fn, outputs, labels, weights):
    return (loss_fn(outputs, labels) * weights).mean()


def train(
        model: nn.Module,
        x: pd.DataFrame,
        y: pd.DataFrame,
        loss_function,
        optimizer,
        n_epochs=100,
        batch_size=256,
        metrics=None,
        sample_weights=None):
    use_cuda = torch.cuda.is_available()
    LOGGER.info(f"Use cuda: {use_cuda}")
    device = torch.device("cuda" if use_cuda else "cpu")
    cuda_kwargs = {'num_workers': 1,
                   'pin_memory': True,
                   'shuffle': True}

    x = torch.tensor(x, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32)
    model = model.to(device)
    if metrics is None:
        metrics = {}
    if sample_weights is not None:
        sample_weights = torch.tensor(sample_weights)
        if len(x.shape) == 2:
            x = torch.cat((sample_weights.unsqueeze(1), x), dim=1)
        elif len(x.shape) == 3:
            sample_weights = sample_weights.unsqueeze(1)
            sample_weights = sample_weights.unsqueeze(1)
            sample_weights = sample_weights.repeat(1, 1, x.shape[2])
            x = torch.cat([sample_weights, x], dim=1)
    torch_dataset = TensorDataset(x, y)
    loader = DataLoader(torch_dataset, batch_size=batch_size, **cuda_kwargs)
    for epoch in range(n_epochs):
        model.train()
        losses = []
        metric_series = {}
        n_batches = int(np.ceil(len(x) / batch_size))
        with tqdm(total=n_batches) as progress_bar:
            for batch_idx, (inputs, labels) in enumerate(loader):
                inputs, labels = inputs.to(device), labels.to(device)
                if sample_weights is not None:
                    inputs, batch_sample_weights = inputs[:, 1:, :], inputs[:, 0, :]
                if len(inputs.shape) == 3:
                    inputs = inputs.swapdims(1, 2)
                    inputs = inputs.swapdims(0, 1)
                    labels = labels.swapdims(0, 1)
                    if sample_weights is not None:
                        batch_sample_weights = batch_sample_weights.swapdims(0, 1)
                optimizer.zero_grad()
                outputs = model.forward(inputs)
                if sample_weights is not None:
                    loss = weighted_loss(
                        loss_function,
                        outputs.squeeze(),
                        labels.squeeze(),
                        batch_sample_weights.squeeze())
                else:
                    loss = loss_function(outputs.squeeze(), labels.squeeze()).mean()
                loss.backward()
                optimizer.step()
                losses.append(loss.cpu().item())
                for name, metric in metrics.items():
                    if name not in metric_series:
                        metric_series[name] = []
                    metric_series[name].append(
                        metric(
                            labels.detach().cpu().numpy(),
                            outputs.squeeze().detach().cpu().numpy()))
                progress_bar.set_description(
                    f"Epoch: {epoch}, loss: {np.mean(losses):.5f}, {', '.join([f'{name}: {np.mean(vals):.5f}' for name, vals in metric_series.items()])}")
                progress_bar.update()
                del inputs
                del batch_sample_weights
                del labels
        LOGGER.info(
            f"Epoch: {epoch}, loss: {np.sum(losses) / len(losses)}, {', '.join([f'{name}: {np.sum(vals) / len(vals)}' for name, vals in metric_series.items()])}")
