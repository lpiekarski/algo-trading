import logging
import os
import datetime
from subprocess import CalledProcessError

import pandas as pd
import commons.git as git
from commons.drive import get_drive_module
from commons.env import getenv
from commons.exceptions import BotError, CloudFileNotFoundError
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def submit_to_drive(binary_cross_entropy, accuracy, model, test_dataset, train_dataset, test_label, train_label, **kwargs):
    LOGGER.info("Storing the results")

    cache_dir = getenv("CACHE_DIR")
    cloud_path = "evaluation/results.csv"
    local_path = os.path.join(cache_dir, cloud_path)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    drive = get_drive_module()
    try:
        drive.download(cloud_path, local_path)
        results = pd.read_csv(local_path, parse_dates=True, index_col="date")
    except CloudFileNotFoundError:
        LOGGER.warning(f"Evaluation results file doesn't exist on drive '{drive}', creating one")
        results = pd.DataFrame({
            "parameters/model": [],
            "parameters/version": [],
            "parameters/train_dataset": [],
            "parameters/test_dataset": [],
            "parameters/train_label": [],
            "parameters/test_label": [],
            "eval/binary_cross_entropy": [],
            "eval/accuracy": []
        }, index=pd.DatetimeIndex([], name='date'))
    version = git.file_version(f"model/predictors/{model}.py")
    if getenv('drive') == 'git':
        if git.get_branch() != 'master':
            raise BotError('Submitting results from non-master branch is prohibited.')
        if version.endswith("-dirty"):
            raise BotError('Submitting results from a dirty predictor file is prohibited. Commit or revert the changes.')
    run = pd.DataFrame({
        "parameters/model": [str(model)],
        "parameters/version": [version],
        "parameters/train_dataset": [str(train_dataset)],
        "parameters/test_dataset": [str(test_dataset)],
        "parameters/train_label": [str(train_label)],
        "parameters/test_label": [str(test_label)],
        "eval/binary_cross_entropy": [binary_cross_entropy],
        "eval/accuracy": [accuracy]
    }, index=pd.DatetimeIndex([datetime.datetime.now()], name='date'))
    LOGGER.info(f"Submitting evaluation:\n{run.to_string()}")
    pd.concat([results, run]).to_csv(local_path)
    drive.upload(local_path, cloud_path)
