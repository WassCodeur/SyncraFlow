from app.stockage import STEPS_DATA, WORFLOWS_DATA, load_data
from app.works.celery_app import celery_app

import time


@celery_app.task
def initial_task(data):
    time.sleep(20)
    print("I'm wass a.k.a wasscoder the wizard")
    print("I've received this: ", data)

    return {"message": "ok"}


@celery_app.task
def run_workfow(workflow_id, steps,  playload):
    workflows = load_data(WORFLOWS_DATA)
    steps = load_data(STEPS_DATA)
