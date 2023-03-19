def save_data(savepath, config, dataset, *args, **kwargs):
    if savepath: config['save']['savepath'] = savepath
    print(f'saving_data at { config["save"]["savepath"] }')
    dataset.save(config['save']['savepath'])
    
    return dict() 