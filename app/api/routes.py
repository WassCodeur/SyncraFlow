from fastapi import APIRouter, HTTPException, status
from app.stockage import save_data, load_data, STEPS_DATA, WORFLOWS_DATA


router = APIRouter(prefix="/api/v1", tags=['API'])


@router.get("/hooks/{slug}")
async def slgus(slug):
    workflows = load_data(WORFLOWS_DATA)
    steps = load_data(STEPS_DATA)
    for workflow in workflows:
        _steps = []
        if workflow['slug'] == slug:
            for step in steps:
                if step['workflow_id'] == workflow['id']:
                    _steps.append(step)
            return {"name": workflow['name'], "workflow_id": step['workflow_id'], "steps": _steps}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )
