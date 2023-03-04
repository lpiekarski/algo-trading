from sklearn.svm import SVC
import pandas as pd
import numpy as np
import os
import pickle
from core.data.preprocessor import Preprocessor
from core.exceptions import AtfError
from hmmlearn import hmm
import warnings

model: SVC = None
preprocessor: Preprocessor = None


def initialize(num_features: int, config: dict) -> None:
    global preprocessor, model
    warnings.filterwarnings("ignore")
    model = SVC(C=0.5, kernel='rbf', degree=1, probability=True)


def predict(x: pd.DataFrame, y) -> np.ndarray:
    pred = hmm_pred(x)
    x = pd.concat([x, pred], axis=1)
    return model.predict_proba(preprocessor.apply(x))[:, 1]


def train(x: pd.DataFrame, y: pd.DataFrame) -> None:
    global model
    pred = hmm_pred(x)
    x = pd.concat([x, pred], axis=1)

    # weight = []
    # weight = pred.iloc[:, ]
    # weight = pd.DataFrame(weight)
    # weight = pd.concat([pred.iloc['Time'], weight], axis=1)
    # weight = weight.set_index('Time')
    # weight = weight.dropna()
    # weight = weight.to_numpy().squeeze()

    preprocessor.fit(x)
    model.fit(preprocessor.apply(x), y)  # sample_weight=weight


def save_weights(path: str) -> None:
    with open(os.path.join(path, 'model'), 'wb') as file:
        pickle.dump(model, file)
    preprocessor.save(os.path.join(path, 'preprocessor'))


def load_weights(path: str) -> None:
    global model, preprocessor
    with open(os.path.join(path, 'model'), 'rb') as file:
        model = pickle.load(file)
    preprocessor = Preprocessor.load(os.path.join(path, "preprocessor"))


def hmm_pred(df: pd.DataFrame):
    warnings.filterwarnings("ignore")
    df['Time'] = df.index
    time = df['Time']
    time.reset_index()
    HMM = np.stack((df['Close'],
                    df['Volume']),
                   axis=1)

    # HMM MODEL
    # Estimating models and choosing best one
    best_score = best_model = None
    n_fits = 50  # 50
    np.random.seed(2137)
    for n in range(15, 121, 15):  # (15, 121, 15)
        for n_components in range(3, 10):  # (2,10)
            for idx in range(n_fits):
                model_hmm = hmm.GaussianHMM(
                    n_components=n_components, random_state=idx,
                    init_params='se', n_iter=n)  # some upgrades here needed
                model_hmm.fit(HMM)
                score = model_hmm.score(HMM)
                if best_score is None or score > best_score:
                    best_model = model_hmm
                    best_score = score

    print(f'Generated score: \nBest score:      {best_score}')
    # use the Viterbi algorithm to predict the most likely sequence of states
    # probabilities of each state and merge with df
    predict_proba = best_model.predict_proba(HMM)
    pred = pd.DataFrame(predict_proba)

    time = time.reset_index(drop=True)
    time = pd.DataFrame(time)
    pred = pd.concat([time, pred], axis=1)
    pred = pred.set_index('Time')
    return pred
