from collector.steps.add_labels import add_labels
import core.testing.mocks as mocks
import core.testing.asserts as asrt


def test_label_in_dataframe():
    dataset = mocks.dataset()
    add_labels(dataset)
    assert f'Best_decision_0.01' in dataset.df


def test_label_in_dataset_labels():
    dataset = mocks.dataset()
    add_labels(dataset)
    assert f'Best_decision_0.01' in dataset.labels


def test_labels_not_empty():
    dataset = mocks.dataset()
    add_labels(dataset)
    asrt.dataframe_no_empty_cols(dataset.df)
