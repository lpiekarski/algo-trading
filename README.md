# Algorithmic Trading Framework
The Algorithmic Trading Framework is a project that provides a set of tools for training and testing machine learning models for algorithmic trading. The Project includes a command-line interface that allows users to manage datasets, train models, and test them on historical data. In order to use the Framework, users must have Python 3.10 or later and Git installed on their system. The project uses environment variables to specify the location of data repositories and other settings, making it easy to customize the behavior of the framework. Overall, the Algorithmic Trading Framework offers a convenient and powerful set of tools for exploring and experimenting with algorithmic trading strategies.

## Installation
### Prerequisites
To use the framework, users must have Python 3.10 and git installed on their system.
#### Steps On Ubuntu
1. Clone the repository
   ```bash
   git clone https://github.com/lpiekarski/algo-trading.git
   cd algo-trading
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
There are a few environmental variables that are expected to be set by some parts of the framework:

`GIT_DRIVE_REPO_URL` - URL of the git repository that is being used as a data source for git drive

`DRIVE` - Default drive type. Can be `local` or `git` (Each file in `core/drive` not starting with `__` corresponds to a drive type) 

## Examples
Here are some examples of how to use the ATF CLI to perform common tasks.

File `atf.py` is the cli through which every subcommand can be referenced. ATF stands for Algorithmic Trading Framework. You can always run `python -m atf --help` to get some information on available subcommands and `python -m atf <subcommand> --help` to show information about a specific subcommand. Path to every file can be prefixed with `<drive>:`, where <drive> is `local` or `git`. If there is no drive prefix default value from environmental variable `DRIVE` is assumed. In case of `local` the file is located as usual, but in case of `git` program looks for the file in the repository specified by `GIT_DRIVE_REPO_URL` environmental variable. In this repository each file must be in separate branch, name of the branch should be the same as the path of the file, and the file should be zipped and divided into 100MB parts suffixed with 3 digits starting from 000. You can see an example of a repository set up like this here: https://github.com/S-P-2137/Data

Each argument can be assigned value through a environmental variable with the same name. Environmental variables can also be assigned directly in the command for example below command assigns values for environmental variables `GIT_DRIVE_REPO_URL=https://github.com/S-P-2137` and `LOG_LEVEL=DEBUG`, then proceeds with the copy subcommand:
```
python -m atf -DGIT_DRIVE_REPO_URL=https://github.com/S-P-2137/Data -DLOG_LEVEL=DEBUG copy git:datasets/train/M30_H1 M30_H1.zip
```


### Downloading Datasets from Drive
1. Download a file from drive using command below (you can also run `atf.py copy --help` to see additional options)
    ```bash
    python -m atf copy git:datasets/train/M30_H1 M30_H1.zip
    ```

### Converting Dataset Format to CSV
Typically, a dataset file from the drive will have its own format that contains all the data but also description on which columns are used as labels etc. To extract raw csv from the dataset file format run: 
```bash
python -m atf dataset2csv git:datasets/train/M30_H1 M30_H1.csv
```

### Converting CSV to Dataset Format
Notice that if you don't provide a config file or specify label columns through an argument (TODO: implement), this information will not be saved in the resulting dataset
```bash
python -m atf csv2dataset M30_H1.csv local:datasets/M30_H1
```

### Adding Features And Labels To Dataset Containing Only OHLC Or OHLCV
If you have only `.csv` file first you need to convert it to dataset format.
1. This will add H1 resampled indicators
   ```bash
   python -m atf extract --dataset=local:raw/M1 --time-tag=1h --name=local:resampled_M1_H1.zip
   ```
2. This will add regular M1 indicators
   ```bash
   python -m atf extract --dataset=local:raw/M1 --name=local:M1.zip
   ```

### Uploading to Drive
1. Upload a file to drive using command below (you can also run `python -m atf copy --help` or `python -m atf upload --help` to see additional options)
   ```bash
   python -m atf copy M30_H1.zip git:datasets/train/M30_H1
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
- Evaluate model `fully_connected` with configuration under a path `examples/model_configs/fully_connected.json`, use the dataset under a path `datasets/test/M30_H1` located in git repository, test using label `Best decision_0.01` that is present within this dataset. Evaluation result will be saved in `evaluation/results.csv`. If this file is already present new evaluation result will be appended.
    ```bash
    python -m atf evaluate --model=local:models/fully_connected --model-config=local:examples/model_configs/fully_connected.json --dataset=git:datasets/test/M30_H1 --label=Best_decision_0.01
    ```

### Backtesting Strategy
- Backtest strategy `percentage_tp_sl`
    ```bash
    python -m atf backtest --dataset=git:datasets/test/M30_H1 --model=local:models/fully_connected --strategy=local:strategies/percentage_tp_sl --model-config=local:examples/model_configs/fully_connected.json --strategy-config=local:examples/strategy_configs/percentage_tp_sl.json 
    ```

### Getting Predictions
1. Generate predictions file for a model using command below (you can also run `atf.py predict --help` to see additional options)
    ```bash
    python -m atf predict --model=local:models/naive_bayes --dataset=git:datasets/test/M30_H1
    ```

### Deleting Data from Drive
1. Delete a file from drive using command below (you can also run `atf.py delete --help` to see additional options)
    ```bash
    python -m atf delete git:datasets/raw/dataset_to_delete.zip
    ```

### Collecting OHLC Data
1. You can collect the ohcl S&P 500 data from yfinance using command below (you can also run `atf.py collect --help` to see additional options)
   ```bash
   python -m atf collect --name=local:raw/latest
   ```

### Live Trading (TODO: implement)
   ```bash
   python -m atf trade
   ```

### Running Tests
Every pull request should contain appropriate tests for the changes and all the previous tests present in the repository should be passing.
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

## Implementing New Model
1. Create a new `[model_name].py` file inside `/model/predictors` directory.
2. This module has to implement 5 functions:
   - `initialize(num_features: int, config: dict) -> None` model initialization based on the number of input features and configuration from model's yaml config file.
   - `train(x: pd.DataFrame, y: pd.DataFrame) -> None` training using x as inputs and y as targets.
   - `predict(x: pd.DataFrame) -> np.ndarray` generating prediction from the input x
   - `save_weights(path: str) -> None` saving model's state as file in `path` location
   - `load_weights(path: str) -> None` loading model's state from file location `path`

## Implementing New Strategy
TODO
