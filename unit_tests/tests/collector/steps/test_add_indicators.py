from collector.steps.add_indicators import add_indicators
import core.testing.mocks as mocks


def test_add_indicators():
    dataset = mocks.dataset()
    add_indicators(dataset)
    assert f'VWAP_{dataset.interval.total_seconds():.0f}s' in dataset.df
