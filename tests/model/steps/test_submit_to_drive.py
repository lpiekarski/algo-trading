import os

import pandas as pd
import model.predictors.zero as zero
from model.steps.submit_to_drive import submit_to_drive


def test_submit_to_drive(workspace):
    kwargs = dict(
        eval=dict(
            binary_cross_entropy=0,
            accuracy=0
        ),
        model=zero,
        dataset_name='test_dataset',
        label='label1'
    )
    submit_to_drive(**kwargs)
    path = os.path.join(workspace, "evaluation/results.csv")
    results = pd.read_csv(path, parse_dates=True, index_col="date")
    assert results["parameters/dataset"][0] == kwargs['dataset_name']
    assert results["eval/accuracy"][0] == kwargs['eval']['accuracy']
