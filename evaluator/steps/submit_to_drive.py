import logging
import os
import datetime
import pandas as pd
from commons.drive import get_drive_module
from commons.env import getenv
from commons.exceptions import CloudFileNotFoundError
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def submit_to_drive(binary_cross_entropy=None, model=None, dataset=None, *args, **kwargs):
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
            "parameters/dataset": [],
            "eval/binary_cross_entropy": []
        }, index=pd.DatetimeIndex([], name='date'))
    run = pd.DataFrame({
        "parameters/model": [str(model)],
        "parameters/dataset": [str(dataset)],
        "eval/binary_cross_entropy": [binary_cross_entropy]
    }, index=pd.DatetimeIndex([datetime.datetime.now()], name='date'))

    pd.concat([results, run]).to_csv(local_path)
    drive.upload(local_path, cloud_path)
