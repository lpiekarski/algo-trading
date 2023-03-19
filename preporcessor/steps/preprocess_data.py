import importlib
import logging
from core.data.dataset import Dataset

def preprocess_data(datapath, config, **kwargs):
    LOGGER = logging.getLogger(__name__)
    if datapath: config['data']=datapath
    
    LOGGER.debug(f'preprocessing {config["data"]}')
    dataset = Dataset.load(config['data'])

    for func in config["flow"]:
        module = importlib.import_module(f"preprocessor.functions.{config['function'][func]['file']}")
        f = getattr(module, config['function'][func]['name'])
        dataset.df = f(dataset.df, config['function'][func]['params'])

    # DataFrame under dataset.df
    return dict(dataset=dataset)