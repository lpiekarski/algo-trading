import logging
import neptune.new as neptune
from commons.timing import step

LOGGER = logging.getLogger(__name__)

@step
def submit_to_neptune(NEPTUNE_API_KEY=None, binary_cross_entropy=None, model=None, dataset=None, *args, **kwargs):
    if NEPTUNE_API_KEY is None:
        LOGGER.warning(f"Skipping submitting to neptune (NEPTUNE_API_KEY is not set).")
        return
    LOGGER.info("Storing results in Neptune")
    run = neptune.init(
        name=model,
        project="lpiekarski/S-P-2137",
        api_token=NEPTUNE_API_KEY,
    )

    params = {"model": model, "dataset": dataset}
    run["parameters"] = params

    # for epoch in range(10):
    #    run["train/loss"].log(0.9 ** epoch)

    run["eval/binary_cross_entropy"] = binary_cross_entropy

    run.stop()