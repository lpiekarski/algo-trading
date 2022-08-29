from commons.dataset import put_dataset
from commons.timing import step

@step
def save_dataset(name=None, df=None, start_date=None, *args, **kwargs):
    if name is None:
        name = start_date.strftime("%Y-%m-%d-%H-%M")
    put_dataset(name, df)
