import pytest

from commons.configparams import Config


@pytest.fixture()
def workspace():
    return Config.require_param('test_workspace')
