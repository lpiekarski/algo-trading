import torch
from tqdm import tqdm
import numpy as np
import logging

LOGGER = logging.getLogger(__name__)


def train(
        model,
        x,
        y,
        loss_function,
        optimizer,
        n_epochs=100,
        batch_size=256,
        metrics=None):
    use_cuda = torch.cuda.is_available()
    LOGGER.info(f"Use cuda: {use_cuda}")
    device = torch.device("cuda" if use_cuda else "cpu")
    cuda_kwargs = {'num_workers': 1,
                   'pin_memory': True,
                   'shuffle': True}
    model = model.to(device)
    if metrics is None:
        metrics = {}
    loader = torch.utils.data.DataLoader(
        list(zip(x, y)), batch_size=batch_size, **cuda_kwargs)
    for epoch in tqdm(range(n_epochs)):
        model.train()
        losses = []
        metric_series = {}
        for batch_idx, (inputs, labels) in enumerate(loader):
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_function(np.squeeze(outputs), labels)
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
            for name, metric in metrics.items():
                if name not in metric_series:
                    metric_series[name] = []
                metric_series[name].append(
                    metric(
                        np.squeeze(outputs).detach().numpy(),
                        labels.detach().numpy()))
        LOGGER.info(
            f"Epoch: {epoch}, loss: {np.sum(losses) / len(losses)}, {', '.join([f'{name}: {np.sum(vals) / len(vals)}' for name, vals in metric_series.items()])}")
