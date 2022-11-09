import commons.drivepath as dp
from commons.timing import step

@step
def copy(source, target, **kwargs):
    dp.copy(source, target)
