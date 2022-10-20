import pickle
import re

class Preprocessor:
    def __init__(self):
        self.std = None
        self.mean = None
        self.range_min = None
        self.range_max = None
        self.standardized_columns = None
        self.normalized_columns = None

    def fit(self, X, standardization=None):
        X_ = X.copy()
        if standardization is None:
            standardization = [
                ".*log_change.*"
            ]
        self.normalized_columns = []
        self.standardized_columns = []
        for col in X_:
            if all([not bool(re.match(r, col)) for r in standardization]):
                self.normalized_columns.append(col)
            else:
                self.standardized_columns.append(col)
        Xstd = X_[self.standardized_columns]
        self.mean = Xstd.mean()
        self.std = Xstd.std()
        Xnorm = X_[self.normalized_columns]
        self.range_min = Xnorm.min()
        self.range_max = Xnorm.max()

    def apply(self, X):
        X_ = X.copy()
        Xstd = X_[self.standardized_columns]
        Xnorm = X_[self.normalized_columns]
        X_.update((Xstd - self.mean) / self.std)
        X_.update((Xnorm - self.range_min) / (self.range_max - self.range_min + 1e-8))
        X_ = X_.fillna(0)
        return X_

    def save(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filepath):
        with open(filepath, 'r') as file:
            return pickle.load(file)