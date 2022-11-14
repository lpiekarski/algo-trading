# Stock market bot

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

## Example Usages
File `atf.py` is the cli through which every subcommand can be referenced. ATF stands for Algorithmic Trading Framework. 

### Testing
1. Run tests
   ```bash
   python -m atf test
   ```

### Implementing a New Model
1. Create a new `[model_name].py` file inside `/model/predictors` directory.
2. This module has to implement 4 methods: `train(x, y)`, `predict(x)`, `save(path)`, `load(path)`.
3. Methods `save(path)` and `load(path)` should implement storing and restoring the model's state from a directory given by `path`.
4. Method `train(x, y)` should fit the model to the given dataset (`x` - features, `y` - label)
5. Method `predict(x)` should return the model's prediction for a given input `x`.

### Evaluating
1. Evaluate using command below (you can also run `atf.py evaluate --help` to see additional options)
   ```bash
   python -m atf evaluate --dataset=git:datasets/test/M30_H1 --label=Best_decision_0.01 --model=local:models/fully_connected --model-config=local:cfgs/fc1.json
   ```

### Backtesting
   ```bash
   python -m atf backtest --dataset=git:datasets/test/M30_H1 --model=local:models/fully_connected --strategy=local:strategies/percentage_tp_sl --model-config=local:cfgs/fc1.json --strategy-config=local:cfgs/pct_tpsl.json 
   ```
   
### Training
1. Train model using command below (you can also run `bot.py train --help` to see additional options)
    ```bash
    python -m atf train --model=local:models/naive_bayes --dataset=git:datasets/train/M30_H1 --label=Best_decision_0.01
    ```

### Obtaining Model Predictions for a Given Dataset
1. Generate predictions file for a model using command below (you can also run `bot.py predict --help` to see additional options)
    ```bash
    python -m atf predict --model=local:models/naive_bayes --dataset=git:datasets/test/M30_H1
    ```

### Downloading Data from Drive
1. Download a file from drive using command below (you can also run `bot.py download --help` to see additional options)
    ```bash
    python -m atf copy git:datasets/train/M30_H1 M30_H1.zip
    ```

### Converting Dataset to CSV
```bash
python -m atf dataset2csv git:datasets/train/M30_H1 M30_H1.csv
```

### Converting CSV to dataset
```bash
python -m atf csv2dataset M30_H1.csv local:datasets/M30_H1
```

### Uploading Data to Drive
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

### Creating Dataset from OHLC Data
1. Extract features from a raw OHLC data using command below (you can also run `bot.py extract --help` to see additional options)
   ```bash
   python -m atf extract --dataset=local:raw/M1 --time-tag=1h --name=local:resampled_M1_H1.zip
   ```

### Trading Using Model's Predictions
   ```bash
   python -m atf trade
   ```

## Repository Contents
- Github configuration (in `/.github`)
  - Contains directory `/.github/workflows` with github actions definition
- Data Collector (in `/collector`)
  - Collects all the necessary data for models
  - Exposes `/collector/collect.py` script that can be used to save data for the last or target hour onto target cloud location
  - Saved data contains at least `Date`, `Open`, `High`, `Low`, `Close` features, but also many more technical indicators
  - Features in saved data need not be normalized or standardized
- Commons (in `/commons`)
  - A technical module containing code that is reused across multiple modules
- Data (in `/data`)
  - Precomputed datasets stored using git-lfs
- Docker (in `/docker`)
  - Files needed for running bot using docker
- Evaluator (in `/evaluator`)
  - Evaluates the Model based on the predictions generated for test dataset in a way that the results can be compared with different models/runs of the same adjusted model
  - Exposes `/evaluator/evaluate.py` script that evaluates the Model and uploads results to Neptune
- Model (in `/model`)
  - Uses the data generated by Data Collector to create and store a prediction model
  - Exposes `/model/train.py` script that can be used to train the model on specified dataset and store the resulting model parameters
  - Exposes `/model/predict.py` script that generates model predictions for the specified dataset
- Testing (in `/testing`)
  - Test runner module containing script `/testing/test.py` that runs tests
- Trader (in `/trader`)
  - Trade using `/trader/trade.py` connecting through chosen broker API, perform decision based on command options or the result from Model
- Bot (in `/bot.py`)
  - CLI that bridges scripts exposed by modules into one command line tool
