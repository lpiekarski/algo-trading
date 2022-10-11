import logging

import pandas as pd

from collector.technical_indicators.resample_technical_indicators import resample_technical_indicators
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def add_resample_indicators(X, time_tag, *args, **kwargs):
    LOGGER.info(f"reshape to time unit '{time_tag}'")
    resample_df = resample_technical_indicators(X, time_tag=time_tag)
    resampled_X = pd.concat([X, resample_df], axis=1, join='inner')
    return dict(resampled_X=resampled_X)
