import pandas as pd
import numpy as np
from core.data.preprocessor import Preprocessor


def test_preprocessor_01():
    preprocessor = Preprocessor(normalization_regexes=['a'])
    preprocessor.fit(pd.DataFrame({'a': [0, 1, 2, 3, 4]}))
    assert np.allclose(
        np.array([[0., 1., 0.5]]),
        preprocessor.apply(pd.DataFrame({'a': [0, 4, 2]}))
    )


def test_preprocessor_02():
    preprocessor = Preprocessor(standardization_regexes=['a'])
    preprocessor.fit(pd.DataFrame(
        {'a': [0, 1, 2, 3, 4]}))
    assert np.allclose(
        np.array([[-1.264911, 1.264911, 0]]),
        preprocessor.apply(pd.DataFrame({'a': [0, 4, 2]}))
    )


def test_preprocessor_03():
    preprocessor = Preprocessor(standardization_regexes=['a'])
    preprocessor.fit(pd.DataFrame({'a': [0, 1, 2, 3, 4], 'b': [
                     0, 1, 2, 3, 4]}))
    assert np.allclose(
        np.array([[-1.264911, 1.264911, 0], [0., 1., 0.5]]),
        preprocessor.apply(pd.DataFrame({'a': [0, 4, 2], 'b': [0, 4, 2]}))
    )
