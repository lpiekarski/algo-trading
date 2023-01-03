import datetime
import logging
import os
import pandas as pd
import commons.git as git
from commons.drivepath import clear_cache, copy, delete
from commons.exceptions import SubmissionError, NotFoundError
from commons.tempdir import TempDir

LOGGER = logging.getLogger(__name__)


def submit_to_drive(
        eval,
        model,
        dataset_name,
        label,
        task=None,
        result_file_path=None,
        **kwargs):
    LOGGER.info("Storing the results")

    with TempDir() as tempdir:
        if result_file_path is None:
            cloud_path = "evaluation/results.csv"
        else:
            cloud_path = result_file_path
        local_path = os.path.join(tempdir, cloud_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        drive_type = os.getenv("drive")
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
                "parameters/label": []
            } | {f"eval/{metric}": [] for metric, _ in eval.items()}, index=pd.DatetimeIndex([], name='date'))
        try:
            version = git.file_version(f"model/predictors/{model}.py")
            if os.getenv('drive') == 'git':
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
            } | {f"eval/{metric}": [value] for metric, value in eval.items()}
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
