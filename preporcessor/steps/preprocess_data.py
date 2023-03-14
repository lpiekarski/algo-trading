import logging
from core.data.dataset import Dataset

def preprocess_data(datapath, config, **kwargs):
    LOGGER = logging.getLogger(__name__)
    if datapath: config['data']=datapath
    
    LOGGER.debug(f'preprocessing {config["data"]}')
    dataset = Dataset.load(config['data'])

    # DataFrame under dataset.df
    # do some preprocessng
    return dict(dataset=dataset)