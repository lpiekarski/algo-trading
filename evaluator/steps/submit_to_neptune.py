import logging

from commons.timing import run_step

LOGGER = logging.getLogger(__name__)

@run_step
def submit_to_neptune(*args, **kwargs):
    LOGGER.info("Storing results in Neptune")
    # run = neptune.init(
    #    name=model_name,
    #    project="lpiekarski/S-P-2137",
    #    api_token
    #
    #    ="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIzMTQ4NTdmMy00OWRkLTQ2MmUtYWIwNC03MWVhZmM2MDQxNDMifQ==", #os.getenv("NEPTUNE_API_TOKEN")

    # )

    # params = {"learning_rate": 0.001, "optimizer": "Adam"}
    # run["parameters"] = params

    # for epoch in range(10):
    #    run["train/loss"].log(0.9 ** epoch)

    # run["eval/f1_score"] = 0.66

    # run.stop()