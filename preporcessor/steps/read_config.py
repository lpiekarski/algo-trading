import yaml
import pprint


def read_config(config_path, **kwargs):
    print(f'reading config from {config_path}')
    with open(config_path, 'r') as stream:
        config = yaml.load(stream, yaml.SafeLoader)
        pprint.pprint(config)
    return dict(config=config)
