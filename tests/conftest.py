import pytest
from commons.env import require_env


@pytest.fixture()
def workspace():
    return require_env('test_workspace')
