import pandas as pd
import numpy as np
from hmmlearn import hmm
import warnings


def hmm_predict(df: pd.DataFrame):
    warnings.filterwarnings("ignore")
    df['Time'] = df.index
    time = df['Time']
    time.reset_index()
    hmm_data = np.stack((df['Close'],
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
                model_hmm.fit(hmm_data)
                score = model_hmm.score(HMM)
                if best_score is None or score > best_score:
                    best_model = model_hmm
                    best_score = score

    print(f'Generated score: \nBest score:      {best_score}')
    # use the Viterbi algorithm to predict the most likely sequence of states
    # probabilities of each state and merge with df
    predict_proba = best_model.predict_proba(hmm_data)
    pred = pd.DataFrame(predict_proba)

    time = time.reset_index(drop=True)
    time = pd.DataFrame(time)
    pred = pd.concat([time, pred], axis=1)
    pred = pred.set_index('Time')
    return pred
    
