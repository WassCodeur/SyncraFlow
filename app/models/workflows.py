from pydantic import BaseModel
from uuid import UUID
from typing import List, Dict, Any


class WorkFlowModel(BaseModel):
    name: str


class WorkFlow(WorkFlowModel):
    id: str
    user_id: str
    slug: str
    is_active: bool


class Step(BaseModel):
    type: str
    config: Dict[str, Any]
    # order: int


class StepModel(Step):
    id: str
    workflow_id: str
    order: int


class Steps(BaseModel):
    steps: List[Step]


class WorkflowCreated(BaseModel):
    workflow_id: str
    slug: str
