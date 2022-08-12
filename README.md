# Stock market bot

## Contents
- Commons (in `/commons`)
  - A technical module containing code that is reused across multiple modules
- Data Collector (in `/collector`)
  - Collects all the necessary data for models
  - Exposes `/collector/collect.py` script that can be used to save data onto target cloud location
  - Saved data contains at least `Date`, `Open`, `High`, `Low`, `Close` features, but also many more technical indicators
  - Features in saved data need not be normalized or standardized
  - Data should be divided by a year. Some years should be marked as a part of train set, and some as test set possibly in a way to form an 80-20 split of the whole dataset
- Model (in `/model`)
  - Uses the data generated by Data Collector to create and store a prediction model
  - Exposes `/model/train.py` script that can be used to train the model on specified dataset and store the resulting model parameters
  - Exposes `/model/predict.py` script that generates model predictions for the specified dataset
- Evaluator (in `/evaluator`)
  - Evaluates the Model based on the predictions generated for test dataset in a way that the results can be compared with different models/runs of the same adjusted model
  - Exposes `/evaluator/evaluate.py` script that evaluates the Model and uploads results to Neptune
- Bot (in `/bot.py`)
  - CLI that bridges scripts exposed by modules into one command line tool