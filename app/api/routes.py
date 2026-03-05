from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from app.database.connection import get_conn
from app.database import queries
from psycopg import connection
from app.models.workflows import Steps


router = APIRouter(prefix="/api/v1", tags=['API'])


@router.get("/hooks/{slug}")
async def slgus(db: Annotated[connection, Depends(get_conn)], slug):
    workflow = queries.get_one(db_conn=db, table="workflows", filter={
                               "trigger_slug": slug})

    if workflow:
        steps = queries.get_all_by_filter(db_conn=db, table="steps", filter={
            "workflow_id": workflow['id']})

        if steps:
            return steps

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Workflow not found or no steps found for this workflow"
    )
