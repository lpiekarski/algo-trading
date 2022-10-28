import torch
from tqdm import tqdm
import numpy as np
import logging

LOGGER = logging.getLogger(__name__)


def train(model, x, y, loss_function, optimizer, n_epochs=100, batch_size=256, metrics=None, lambda_1=0):
    if metrics is None:
        metrics = {}
    loader = torch.utils.data.DataLoader(list(zip(x, y)), batch_size=batch_size)
    for epoch in tqdm(range(n_epochs)):
        model.train()
        losses = []
        metric_series = {}
        for inputs, labels in loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            l1_penalty = lambda_1 * sum([p.abs().sum() for p in model.parameters()])
            loss = loss_function(np.squeeze(outputs), labels) + l1_penalty
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
            for name, metric in metrics.items():
                if name not in metric_series:
                    metric_series[name] = []
                metric_series[name].append(metric(np.squeeze(outputs).detach().numpy(), labels.detach().numpy()))
        LOGGER.info(f"Epoch: {epoch}, loss: {np.sum(losses) / len(losses)}, {', '.join([f'{name}: {np.sum(vals) / len(vals)}' for name, vals in metric_series.items()])}")