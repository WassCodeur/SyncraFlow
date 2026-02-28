from fastapi import APIRouter, status, HTTPException
from app.models.workflows import WorkFlow, Step, WorkflowCreated, WorkFlowModel, StepModel
from app.api.utils import generat_slug
from uuid import uuid4
from app.stockage import save_data, load_data, STEPS_DATA, WORFLOWS_DATA


router = APIRouter(prefix="/api/v1", tags=['Workflows'])


@router.post('/workflows', response_model=WorkflowCreated)
def add_workflow(workflow: WorkFlowModel):
    workflows = load_data(WORFLOWS_DATA)
    data = {
        'id': str(uuid4()),
        'name': workflow.name,
        'user_id': "qtqrRTZQgPO3",  # TODO: to be update
        'slug': generat_slug(workflow.name),
        'is_active': True
    }
    print(workflows)
    for workflow in workflows:
        if workflow['name'] == data['name'] and workflow['user_id'] == data['user_id']:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"You alreary have this workflow with the same name slug: {workflow['slug']}"
            )

    workflow = WorkFlow(**data)
    workflows.append(data)
    save_data(workflows, WORFLOWS_DATA)

    return {"workflow_id": workflow.id, "slug": workflow.slug}


@router.post("/workflows/{workflow_id}/steps")
def add_step(step: Step, workflow_id):
    workflows = load_data(WORFLOWS_DATA)
    steps = load_data(STEPS_DATA)
    print(steps)
    for workflow in workflows:
        if workflow['id'] == workflow_id:
            step = {
                "id": str(uuid4()),
                "workflow_id": workflow_id,
                "type": step.type,
                "config": step.config,
                "order": len(steps) + 1

            }
            steps.append(step)
            save_data(steps, STEPS_DATA)
            step = StepModel(**step)

            return {"step_id": step.id, "workflow_id": step.workflow_id, "step_type": step.type, "order": step.order}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to add the new step"
    )
