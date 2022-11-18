import datetime
import logging
import os

import pandas as pd

import commons.git as git
from commons.drivepath import clear_cache, copy, delete
from commons.env import getenv
from commons.exceptions import SubmissionError, NotFoundError
from commons.tempdir import TempDir
from commons.timing import step

LOGGER = logging.getLogger(__name__)


@step
def submit_to_drive(
        binary_cross_entropy,
        accuracy,
        model,
        dataset_name,
        label,
        task=None,
        **kwargs):
    LOGGER.info("Storing the results")

    with TempDir() as tempdir:
        cloud_path = "evaluation/results.csv"
        local_path = os.path.join(tempdir, cloud_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        drive_type = getenv('drive')
        drivepath = f"{drive_type}:{cloud_path}"
        try:
            copy(drivepath, f"local:{local_path}")
            results = pd.read_csv(
                local_path, parse_dates=True, index_col="date")
            delete(drivepath)
        except NotFoundError:
            LOGGER.warning(
                f"Evaluation results file doesn't exist on drive '{drive_type}', creating one")
            results = pd.DataFrame({
                "parameters/model": [],
                "parameters/version": [],
                "parameters/dataset": [],
                "parameters/label": [],
                "eval/binary_cross_entropy": [],
                "eval/accuracy": []
            }, index=pd.DatetimeIndex([], name='date'))
        try:
            version = git.file_version(f"model/predictors/{model}.py")
            if getenv('drive') == 'git':
                if git.get_branch() != 'master':
                    raise SubmissionError(
                        'Submitting results from non-master branch is prohibited.')
                if version.endswith("-dirty"):
                    raise SubmissionError(
                        'Submitting results from a dirty predictor file is prohibited. Commit or revert the changes.')
            params = {
                "parameters/model": [str(model)],
                "parameters/version": [version],
                "parameters/dataset": [str(dataset_name)],
                "parameters/label": [str(label)],
                "eval/binary_cross_entropy": [binary_cross_entropy],
                "eval/accuracy": [accuracy]
            }
            run = pd.DataFrame(params, index=pd.DatetimeIndex(
                [datetime.datetime.now()], name='date'))
            LOGGER.info(f"Submitting evaluation:\n{run.to_string()}")
            if task is not None:
                task.connect(run.iloc[0].to_dict())
            pd.concat([results, run]).to_csv(local_path)
        finally:
            if task is not None:
                task.close()
            copy(f"local:{local_path}", drivepath)
        clear_cache(f"local:{local_path}")
