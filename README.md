# Algorithmic Trading Framework

## Installation
### Prerequisites
1. You have to have git and python 3.10 installed
#### Steps On Ubuntu
1. Clone the repository
   ```bash
   git clone https://github.com/lpiekarski/SP2137.git
   cd SP2137
   ```
2. Create python virtual environment
   ```bash
   python3 -m venv venv --upgrade-deps
   ```
3. Activate the environment
   ```bash
   . ./venv/bin/activate
   ```
4. Install required python dependencies
   ```bash
   python -m pip install -r requirements.txt
   ```
#### Setting Up Environment After Installation
There are a few environmental variables that are expected for some parts of the framework:

`GIT_DRIVE_REPO_URL` - URL of the git repository that is being used as a data source for git drive

`DRIVE` - Default drive type. Can be `local` or `git` 

## Examples
File `atf.py` is the cli through which every subcommand can be referenced. ATF stands for Algorithmic Trading Framework. You can always run `python -m atf --help` to get some information on available subcommands and `python -m atf <subcommand> --help` to show information about a specific subcommand. Path to every file can be prefixed with `<drive>:`, where <drive> is `local` or `git`. If there is no drive prefix default value from environmental variable `DRIVE` is assumed. In case of `local` the file is located as usual, but in case of `git` program looks for the file in the repository specified by `GIT_DRIVE_REPO_URL` environmental variable. In this repository each file must be in separate branch, name of the branch should be the same as the path of the file, and the file should be zipped and divided into 100MB parts suffixed with 3 digits starting from 000. You can see an example of a repository set up like this here: https://github.com/S-P-2137/Data

### Running Tests
- Run tests regularly
   ```bash
   python -m atf test
   ```
- Run tests but skip unit tests
   ```bash
   python -m atf test --skip-unit-tests
   ```
- Run tests but skip shape tests
   ```bash
   python -m atf test --skip-shape-tests
   ```
- Run tests but skip checking the formatting
   ```bash
   python -m atf test --skip-format-tests
   ```
   
### Training Model
- Run training of model `naive_bayes`, use the dataset under a path `datasets/train/M30_H1` located in git repository, train using label `Best decision_0.01` that is present within this dataset and save the weights of the model after training to a local file `./models/naive_bayes`
    ```bash
    python -m atf train --model=local:models/naive_bayes --dataset=git:datasets/train/M30_H1 --label=Best_decision_0.01
    ```
- Run training of model `fully_connected` with configuration under a path `examples/model_configs/fully_connected.json`, use the dataset under a path `datasets/train/M30_H1` located in git repository, train using label `Best decision_0.01` that is present within this dataset and save the weights of the model after training to a local file `./models/fully_connected`
    ```bash
    python -m atf train --model=local:models/fully_connected --model-config=local:examples/model_configs/fully_connected.json --dataset=git:datasets/train/M30_H1 --label=Best_decision_0.01
    ```
   
### Evaluating Model
1. Evaluate model `fully_connected` with configuration under a path `examples/model_configs/fully_connected.json`, use the dataset under a path `datasets/test/M30_H1` located in git repository, test using label `Best decision_0.01` that is present within this dataset. Evaluation result will be saved in `evaluation/results.csv`. If this file is already present new evaluation result will be appended.
   ```bash
   python -m atf evaluate --model=local:models/fully_connected --model-config=local:examples/model_configs/fully_connected.json --dataset=git:datasets/test/M30_H1 --label=Best_decision_0.01
   ```

### Backtesting Strategy
   ```bash
   python -m atf backtest --dataset=git:datasets/test/M30_H1 --model=local:models/fully_connected --strategy=local:strategies/percentage_tp_sl --model-config=local:examples/model_configs/fully_connected.json --strategy-config=local:examples/strategy_configs/percentage_tp_sl.json 
   ```


### Getting Predictions
1. Generate predictions file for a model using command below (you can also run `bot.py predict --help` to see additional options)
    ```bash
    python -m atf predict --model=local:models/naive_bayes --dataset=git:datasets/test/M30_H1
    ```

### Downloading from Drive
1. Download a file from drive using command below (you can also run `bot.py download --help` to see additional options)
    ```bash
    python -m atf copy git:datasets/train/M30_H1 M30_H1.zip
    ```

### Converting Dataset Format to CSV
```bash
python -m atf dataset2csv git:datasets/train/M30_H1 M30_H1.csv
```

### Converting CSV to Dataset Format
```bash
python -m atf csv2dataset M30_H1.csv local:datasets/M30_H1
```

### Uploading to Drive
1. Upload a file to drive using command below (you can also run `bot.py upload --help` to see additional options)
   ```bash
   python -m atf copy M30_H1.zip git:datasets/train/M30_H1
   ```

### Deleting Data from Drive
1. Delete a file from drive using command below (you can also run `bot.py delete --help` to see additional options)
    ```bash
    python -m atf delete git:datasets/raw/dataset_to_delete.zip
    ```

### Collecting OHLC Data
1. You can collect the ohcl S&P 500 data from yfinance using command below (you can also run `bot.py collect --help` to see additional options)
   ```bash
   python -m atf collect --name=local:raw/latest
   ```

### Adding Features And Labels To Dataset Containing Only OHLC Or OHLCV
1. This will add H1 resampled indicators
   ```bash
   python -m atf extract --dataset=local:raw/M1 --time-tag=1h --name=local:resampled_M1_H1.zip
   ```
2. This will add regular M1 indicators
   ```bash
   python -m atf extract --dataset=local:raw/M1 --name=local:M1.zip
   ```

### Live Trading (WIP)
   ```bash
   python -m atf trade
   ```

## Implementing New Model
1. Create a new `[model_name].py` file inside `/model/predictors` directory.
2. This module has to implement 4 methods: `train(x, y)`, `predict(x)`, `save(path)`, `load(path)`.
3. Methods `save(path)` and `load(path)` should implement storing and restoring the model's state from a directory given by `path`.
4. Method `train(x, y)` should fit the model to the given dataset (`x` - features, `y` - label)
5. Method `predict(x)` should return the model's prediction for a given input `x`.

## Implementing New Strategy