from collector.steps.add_indicators import add_indicators
import core.testing.mocks as mocks


def test_add_indicators_00():
    dataset = mocks.dataset()
    add_indicators(dataset)
    assert f'VWAP_{dataset.interval.total_seconds():.0f}s' in dataset.df


def test_add_indicators_01():
    dataset = mocks.dataset()
    add_indicators(dataset, indicator_config=dict(rsi=[14]))
    assert dataset.df.shape[1] == 6
    assert f'rsi_14_{dataset.interval.total_seconds():.0f}s' in dataset.df
