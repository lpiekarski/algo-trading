import numpy as np
import collector.technical_indicators.labels as labels
from commons.dataset import Dataset
import pandas as pd

def test_add_best_decision():
    sequence_test([117, 141, 108, 149, 116, 171, 188, 193, 148, 134], 0.1)

def test_add_best_decision_on_random_sequences():
    n_tries = 100
    for _ in range(n_tries):
        sequence = np.random.randint(100, 201, 10)
        pct_change = np.random.uniform(0, 0.5)
        sequence_test(sequence, pct_change)

def sequence_test(sequence, pct_change):
        dataset = Dataset(pd.DataFrame({
            'Open': sequence,
            'High': sequence,
            "Low": sequence,
            'Close': sequence
        }, index=pd.DatetimeIndex([pd.Timestamp('2010-01-01 00:00') + pd.Timedelta(minutes=i) for i in range(len(sequence))])))
        labels.add_best_decision(dataset, pct_change)
        real = list(dataset.df[f'Best_decision_{pct_change}'])
        brute = brute_force_best_decision(dataset, pct_change)
        print('Sequence:')
        print(sequence)
        print(f'Percent change: {pct_change}')
        print('Real:')
        print(real)
        print('Brute:')
        print(brute)
        assert real == brute

def brute_force_best_decision(dataset, pct_change):
    return [find_best_decision_for_id(dataset.df, index, pct_change) for index in range(dataset.df.shape[0])]

def find_best_decision_for_id(df, index, pct_change):
    for i in range(index + 1, df.shape[0]):
        if df.iloc[i]['Low'] <= df.iloc[index]['Close'] * (1 - pct_change):
            return 0
        elif df.iloc[i]['High'] >= df.iloc[index]['Close'] * (1 + pct_change):
            return 1
    return 0