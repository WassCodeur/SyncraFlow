from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from app.database.connection import get_conn
from app.database import queries
from psycopg import connection
from app.models.workflows import Steps
from app.workers.tasks import run_workflow
from app.models.workflows import Step


router = APIRouter(prefix="/api/v1", tags=['API'])


@router.post("/hooks/{slug}")
async def hook_handler(db: Annotated[connection, Depends(get_conn)], payload: dict, slug):
    """Handle incoming webhook requests and trigger the corresponding workflow.

    Parameters
    ----------
    db : connection
        The database connection.
    payload : dict
        The JSON payload received from the webhook.
    slug : str
        The unique slug identifier for the workflow to trigger.

    Returns
    -------
    dict
        A message indicating the result of the webhook handling.
    """
    workflow = queries.get_one(db_conn=db, table="workflows", filter={
                               "trigger_slug": slug})

    if workflow:
        workflow_id = str(workflow['id'])
        steps = queries.get_all_by_filter(db_conn=db, table="steps", filter={
            "workflow_id": workflow_id}, order_by="order")

        if steps:
            run_workflow.delay(workflow['id'], steps, payload)
            return {"message": "Workflow triggered successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Workflow not found or no steps found for this workflow"
    )
