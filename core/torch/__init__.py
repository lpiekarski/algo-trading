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
        train_test_split=0.8,
        early_stopping=True):
    use_cuda = torch.cuda.is_available()
    LOGGER.info(f"Use cuda: {use_cuda}")
    device = torch.device("cuda" if use_cuda else "cpu")
    cuda_kwargs = {'num_workers': 1,
                   'pin_memory': True,
                   'shuffle': True}
    x = torch.tensor(x, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32)
    n_obs = x.shape[0]
    if train_test_split < 1:
        split_idx = int(n_obs * train_test_split)
        x_test = x[split_idx:]
        y_test = y[split_idx:]
        x = x[:split_idx]
        y = y[:split_idx]
        torch_dataset_test = TensorDataset(x_test, y_test)
        test_loader = DataLoader(torch_dataset_test, batch_size=batch_size, **cuda_kwargs)
    model = model.to(device)
    if metrics is None:
        metrics = {}
    torch_dataset = TensorDataset(x, y)
    loader = DataLoader(torch_dataset, batch_size=batch_size, **cuda_kwargs)
    condition_repeat = 0
    prev_loss = 10
    prev_test_loss = 10
    for epoch in range(n_epochs):
        model.train()
        losses = []
        metric_series = {}
        n_batches = int(np.ceil(len(x) / batch_size))
        with tqdm(total=n_batches) as progress_bar:
            for batch_idx, (inputs, labels) in enumerate(loader):
                inputs, labels = prepare_inputs_and_labels(inputs, labels, device)
                optimizer.zero_grad()
                if len(inputs.shape) == 3:
                    outputs, labels = model.forward(inputs, labels)
                else:
                    outputs = model.forward(inputs)
                outputs, labels = post_process_outputs_and_labels(outputs, labels)
                loss = loss_function(outputs, labels).mean()
                loss.backward()
                optimizer.step()
                losses.append(loss.cpu().item())
                update_metrics(metrics, metric_series, labels, outputs)
                progress_bar.set_description(
                    f"Epoch: {epoch}, loss: {np.mean(losses):.5f}, {', '.join([f'{name}: {np.mean(vals):.5f}' for name, vals in metric_series.items()])}")
                progress_bar.update()
                del inputs
                del labels
        model.eval()
        if train_test_split < 1:
            test_metric_series = {}
            test_losses = []
            with torch.no_grad():
                for batch_idx, (inputs, labels) in enumerate(test_loader):
                    inputs, labels = prepare_inputs_and_labels(inputs, labels, device)
                    if len(inputs.shape) == 3:
                        outputs, labels = model.forward(inputs, labels)
                    else:
                        outputs = model.forward(inputs)
                    outputs, labels = post_process_outputs_and_labels(outputs, labels)
                    loss = loss_function(outputs, labels).mean()
                    test_losses.append(loss.cpu().item())
                    update_metrics(metrics, test_metric_series, labels, outputs)
                LOGGER.info(
                    f"Epoch {epoch} test: loss: {np.mean(test_losses):.5f}, {', '.join([f'{name}: {np.mean(vals):.5f}' for name, vals in test_metric_series.items()])}")
            if early_stopping:
                if np.mean(test_losses) > prev_test_loss:
                    condition_repeat += 1
                    if condition_repeat >= 4:
                        break
                else:
                    condition_repeat = 0
                prev_test_loss = np.mean(test_losses)
                prev_loss = np.mean(losses)


def prepare_inputs_and_labels(inputs, labels, device):
    inputs, labels = inputs.to(device), labels.to(device)
    label_nan_mask = labels.view(labels.shape[0], -1).isnan().min(dim=1).values
    inputs_nan_mask = inputs.view(inputs.shape[0], -1).isnan().min(dim=1).values
    all_nan_mask = label_nan_mask | inputs_nan_mask
    inputs = inputs[~all_nan_mask]
    labels = labels[~all_nan_mask]
    inputs[inputs.isnan()] = 0
    labels[labels.isnan()] = 1e9
    if len(inputs.shape) == 3:
        inputs = inputs.swapdims(1, 2)
        inputs = inputs.swapdims(0, 1)
        if len(labels.shape) == 3 and labels.shape[1] == 1:
            labels = labels.swapdims(1, 2)
        labels = labels.swapdims(0, 1)
        if len(labels.shape) == 2:
            labels = labels.unsqueeze(-1)
    return inputs, labels


def post_process_outputs_and_labels(outputs, labels):
    labels = labels.reshape(-1, labels.shape[-1])
    outputs = outputs.reshape(-1, outputs.shape[-1])
    mask = (labels == 1e9).max(dim=1).values
    labels = labels[~mask]
    outputs = outputs[~mask]
    return outputs, labels


def update_metrics(metrics, metric_series, labels, outputs):
    for name, metric in metrics.items():
        if name not in metric_series:
            metric_series[name] = []
        metric_series[name].append(
            metric(
                labels.detach().cpu().numpy(),
                outputs.detach().cpu().numpy()))
