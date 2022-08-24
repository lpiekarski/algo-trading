from commons.dataset import put_dataset
from commons.timing import run_step

@run_step
def save_dataset(name=None, previous_step_result=None, *args, **kwargs):
    df, start_date = previous_step_result
    if name is None:
        name = start_date.strftime("%Y-%m-%d-%H-%M")
    put_dataset(name, df)
