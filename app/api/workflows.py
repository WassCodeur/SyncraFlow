from fastapi import APIRouter, status, HTTPException, Depends
from psycopg import connection
from app.database.connection import get_conn
from app.models.workflows import WorkFlow, Step, WorkflowCreated, WorkFlowModel, StepModel
from app.api.utils import generat_slug
from uuid import uuid4
from app.database import queries
from app.models.users import UserData
from app.auth.utils import current_active_user
from typing import Annotated
from psycopg.types.json import Jsonb

from app.stockage import STEPS_DATA, WORFLOWS_DATA, load_data, save_data


router = APIRouter(prefix="/api/v1", tags=['Workflows'])


@router.post('/workflows', response_model=WorkflowCreated)
def add_workflow(db: Annotated[connection, Depends(get_conn)], user: Annotated[UserData, Depends(current_active_user)], workflow: WorkFlowModel):
    """Create a new workflow for the authenticated user.

    Parameters
    ----------
    db : connection
        The database connection.
    user : UserData
        The currently authenticated user.
    workflow : WorkFlowModel
        The workflow data to be created, including the name and any relevant configuration.

    Returns
    -------
    dict
        A dictionary containing the ID of the newly created workflow and its trigger slug.
    """
    table = "workflows"
    data = {
        'id': str(uuid4()),
        'name': workflow.name,
        'user_id': str(user.id),
        'trigger_slug': generat_slug(workflow.name),
    }
    workflow_exist = queries.get_one(db_conn=db, table=table, columns=[
                                     "id", "trigger_slug"], filter={'name': data['name'], 'user_id': data['user_id']})
    if workflow_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You alreary have this workflow with the same name slug: {workflow_exist['trigger_slug']}"
        )

    workflow = queries.insert(db, table, data)

    return {"workflow_id": str(workflow['id']), "trigger_slug": workflow['trigger_slug']}


@router.post("/workflows/{workflow_id}/steps", response_model=StepModel)
def add_step(db: Annotated[connection, Depends(get_conn)], user: Annotated[UserData, Depends(current_active_user)], step: Step, workflow_id):
    """Add a new step to an existing workflow.

    Parameters
    ----------
    db : connection
        The database connection.
    user : UserData
        The currently authenticated user.
    step : Step
        The step data to be added, including type and configuration.
    workflow_id : str
        The ID of the workflow to which the step will be added.

    Returns
    -------
    dict
        A dictionary containing the details of the newly added step, such as step ID, workflow ID, type, order, and configuration.
    """

    workflow_exist = queries.get_one(db_conn=db, table="workflows", columns=[
                                     "id", "trigger_slug"], filter={'id': workflow_id, 'user_id': user.id})

    if workflow_exist:
        name = step.name.strip().lower()
        step_exist = queries.get_one(
            db_conn=db, table="steps", filter={"type": step.type, "name": name, 'workflow_id': workflow_id})
        if step_exist:
    
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"You already have this step with the same type: {step_exist['type']}"
            )

        steps = queries.get_all_by_filter(db_conn=db, table='steps', filter={
                                          'workflow_id': workflow_id})
        next_order = len(steps) + 1

        step = {
            "id": str(uuid4()),
            "workflow_id": workflow_id,
            "name": name,
            "type": step.type,
            "config": step.config.model_dump(),
            "order":  next_order

        }

        queries.insert(db, 'steps', step)

        return {"step_id": step['id'], "workflow_id": step['workflow_id'], "type": step['type'], "order": step['order'], 'config': step['config']}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to add the new step, workflow not found or you don't have access to it"
    )
