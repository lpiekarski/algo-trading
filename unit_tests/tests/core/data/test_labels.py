import numpy as np
import core.data.labels as labels
import core.testing.mocks as mocks


def test_add_best_decision_on_random_sequences():
    n_tries = 100
    for i in range(n_tries):
        pct_change = np.random.uniform(0, 0.5)
        sequence_test(pct_change)


def sequence_test(pct_change):
    dataset = mocks.dataset(size=20)
    labels.best_decision(dataset, pct_change, smooth=True)
    real = list(dataset.df[f'Best_decision_{pct_change}_smooth_60'])
    brute = brute_force_best_decision(dataset, pct_change)
    assert real == brute


def brute_force_best_decision(dataset, pct_change):
    return [
        find_best_decision_for_id(
            dataset.df,
            index,
            pct_change) for index in range(
            dataset.df.shape[0])]


def find_best_decision_for_id(df, index, pct_change):
    for i in range(index + 1, df.shape[0]):
        if df.iloc[i]['Low'] <= df.iloc[index]['Close'] * (1 - pct_change):
            seconds_to_next_short = (df.index[i].asm8.astype("float64") -
                                     df.index[index].asm8.astype("float64")) / (10 ** 9 * 60)
            decision = -seconds_to_next_short
            decision = 60 / decision
            decision = 1 / (1 + np.exp(-decision))
            return decision
        elif df.iloc[i]['High'] >= df.iloc[index]['Close'] * (1 + pct_change):
            seconds_to_next_long = (df.index[i].asm8.astype("float64") -
                                    df.index[index].asm8.astype("float64")) / (10 ** 9 * 60)
            decision = seconds_to_next_long
            decision = 60 / decision
            decision = 1 / (1 + np.exp(-decision))
            return decision
    return 0.5
