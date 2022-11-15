import pickle
import re


class Preprocessor:
    def __init__(self, num_features=None, standardization_regexes=None, normalization_regexes=None):
        self.std = None
        self.mean = None
        self.range_min = None
        self.range_max = None
        self.standardized_columns = None
        self.normalized_columns = None
        self.num_features = num_features
        if standardization_regexes is not None:
            self.standardization_regexes = standardization_regexes
        else:
            self.standardization_regexes = [
                ".*log_change.*"
            ]
        if normalization_regexes is not None:
            self.normalization_regexes = normalization_regexes
        else:
            self.normalization_regexes = [
                ".*"
            ]

    def fit(self, x):
        x_ = x.copy()
        self.num_features = x_.shape[1]
        self.normalized_columns = []
        self.standardized_columns = []
        for col in x_:
            if any([bool(re.match(r, col)) for r in self.standardization_regexes]):
                self.standardized_columns.append(col)
            elif any([bool(re.match(r, col)) for r in self.normalization_regexes]):
                self.normalized_columns.append(col)
        xstd = x_[self.standardized_columns]
        self.mean = xstd.mean()
        self.std = xstd.std()
        xnorm = x_[self.normalized_columns]
        self.range_min = xnorm.min()
        self.range_max = xnorm.max()

    def apply(self, x):
        x_ = x.copy()
        xstd = x_[self.standardized_columns]
        xnorm = x_[self.normalized_columns]
        x_.update((xstd - self.mean) / self.std)
        x_.update((xnorm - self.range_min) /
                  (self.range_max - self.range_min + 1e-8))
        x_ = x_.fillna(0)
        return x_

    def save(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filepath):
        with open(filepath, 'rb') as file:
            return pickle.load(file)
