from collector.steps.add_resample_indicators import add_resample_indicators
import commons.testing.mocks as mocks
import commons.testing.asserts as asrt


def test_add_resample_indicators():
    dataset = mocks.dataset(1010)
    time_tag = "5min"
    pre_shape = dataset.df.shape[1]
    add_resample_indicators(dataset, time_tag)
    post_shape = dataset.df.shape[1]
    assert post_shape > pre_shape
    asrt.dataframe_no_empty_cols(dataset.df)
