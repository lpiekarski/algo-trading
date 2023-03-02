import core.testing.mocks as mocks
from model.steps.evaluate_predictions import evaluate_predictions


def test_evaluate_predictions():
    dataset = mocks.labeled_dataset()
    label = 'label1'
    y_pred = dataset.get_y(label)
    res = evaluate_predictions(dataset, y_pred, label, None)
    assert res['eval']['binary_cross_entropy'] == 0
    assert res['eval']['accuracy'] == 1
