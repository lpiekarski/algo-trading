from core.data.dataset import Dataset

def preprocess_data(datapath, config, **kwargs):
    if datapath: config['data']=datapath

    dataset = Dataset.load(config['data'])
    # DataFrame under dataset.df
    print(f'preprocessing {config["data"]}')