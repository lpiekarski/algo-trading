import torch
from tqdm import tqdm
import numpy as np
import logging

LOGGER = logging.getLogger(__name__)


def weighted_loss(loss_fn, outputs, labels, weights):
    return (loss_fn(outputs, labels) * weights).mean()


def train(
        model,
        x,
        y,
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
    model = model.to(device)
    if metrics is None:
        metrics = {}
    if sample_weights is not None:
        sample_weights = torch.tensor(sample_weights)
        x = torch.tensor(x)
        if len(x.shape) == 2:
            x = torch.cat((sample_weights.unsqueeze(1), x), dim=1)
        elif len(x.shape) == 3:
            sample_weights = sample_weights.unsqueeze(1)
            sample_weights = sample_weights.unsqueeze(1)
            sample_weights = sample_weights.repeat(1, 1, x.shape[2])
            x = torch.cat([sample_weights, x], dim=1)

    loader = torch.utils.data.DataLoader(
        list(zip(x, y)), batch_size=batch_size, **cuda_kwargs)
    for epoch in range(n_epochs):
        model.train()
        losses = []
        metric_series = {}
        n_batches = int(np.ceil(len(x) / batch_size))
        with tqdm(total=n_batches) as progress_bar:
            for batch_idx, (inputs, labels) in enumerate(loader):
                inputs, labels = inputs.to(device), labels.to(device)
                if len(inputs.shape) == 3:
                    inputs = inputs.swapdims(1, 2)
                    inputs = inputs.swapdims(0, 1)
                    labels = labels.swapdims(0, 1)
                optimizer.zero_grad()
                if sample_weights is not None:
                    outputs = model.forward(inputs[..., 1:])
                else:
                    outputs = model.forward(inputs)
                if sample_weights is not None:
                    loss = weighted_loss(loss_function, np.squeeze(outputs), labels, inputs[..., 0])
                else:
                    loss = loss_function(np.squeeze(outputs), labels)
                loss.backward()
                optimizer.step()
                losses.append(loss.item())
                for name, metric in metrics.items():
                    if name not in metric_series:
                        metric_series[name] = []
                    metric_series[name].append(
                        metric(
                            np.squeeze(outputs).detach().cpu().numpy(),
                            labels.detach().cpu().numpy()))
                progress_bar.set_description(
                    f"Epoch: {epoch}, loss: {np.mean(losses):.5f}, {', '.join([f'{name}: {np.mean(vals):.5f}' for name, vals in metric_series.items()])}")
                progress_bar.update()
                del inputs
                del labels
        LOGGER.info(
            f"Epoch: {epoch}, loss: {np.sum(losses) / len(losses)}, {', '.join([f'{name}: {np.sum(vals) / len(vals)}' for name, vals in metric_series.items()])}")
