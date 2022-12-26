import commons.testing.mocks as mocks
import commons.testing.asserts as asrt
from collector.technical_indicators.resample_technical_indicators import resample_technical_indicators


def test_resample_technical_indicators():
    dataset = mocks.dataset(1010)
    pre_cols = dataset.df.shape[1]
    dataset.concat(resample_technical_indicators(
        dataset, time_tag="5min"), axis=1, join='inner')
    post_cols = dataset.df.shape[1]
    assert pre_cols < post_cols
    asrt.dataframe_no_empty_cols(dataset.df)
