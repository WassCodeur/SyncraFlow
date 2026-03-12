from app.stockage import STEPS_DATA, WORFLOWS_DATA, load_data
from app.workers.celery_app import celery_app
from app.workers.utils import run_step
from app.core.config import logger

import time


@celery_app.task
def initial_task(data):
    time.sleep(20)
    logger.info(f"Initial task received data: {data}")
    logger.info("Initial task completed")

    return {"message": "ok"}


@celery_app.task
def run_workflow(workflow_id, steps,  payload):
    """This function will run the workflow steps sequentially. In a real implementation,
    you would handle step dependencies, error handling, and more complex logic.

    Parameters:
    -----------
    workflow_id: str
        The ID of the workflow being executed.
    steps: list
        A list of steps to execute, where each step is a dictionary containing the step type and configuration.
    payload: dict
        The input data that will be passed to each step for processing.

    Returns:
    --------
    dict
        A dictionary containing the result of the workflow execution, such as a success message or any relevant output from the steps.
    """

    logger.info(
        f"Running workflow {workflow_id} with steps {steps} and payload {payload}")

    for step in steps:
        logger.info(f"Executing step: {step['type']}")
        result = run_step(step["type"], step["config"])
        logger.info(f"Result of step {step['type']}: {result}")


    return {"message": "ok"}
