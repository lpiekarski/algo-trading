import collector.technical_indicators.technical_indicators as ti
import commons.testing.mocks as mocks


def test_technical_indicators_added():
    dataset = mocks.dataset()
    time_tag = 'test'
    pre_add_columns = dataset.df.shape[1]
    dataset.df = ti.add_technical_indicators(dataset, time_tag)
    post_add_columns = dataset.df.shape[1]
    assert post_add_columns > pre_add_columns


def test_technical_indicators_have_values():
    dataset = mocks.dataset()
    time_tag = 'test'
    dataset.df = ti.add_technical_indicators(dataset, time_tag)
    df = dataset.df.dropna(axis=1, how='all')
    assert dataset.df.shape[1] == df.shape[1]
