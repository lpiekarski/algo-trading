from commons.timing import step
import commons.drivepath as dp

@step
def delete(path, **kwargs):
    dp.delete(path)
