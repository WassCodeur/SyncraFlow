from contextlib import asynccontextmanager
from psycopg.sql import SQL, Identifier
from psycopg.types.json import Jsonb
from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
from psycopg_pool import ConnectionPool
from app.auth.routes import router as auth_router
from app.auth.user import router as users_router
from app.core.config import settings, logger
from app.database import queries
from app.database.connection import get_conn, get_connection_pool
from typing import Annotated
from psycopg import connection
from app.workers.tasks import initial_task
from celery.result import AsyncResult
from app.api.routes import router as api_routes
from app.api.workflows import router as workflows_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Up")
    pool = get_connection_pool()

    app.state.conn_pool = pool

    pool.open()
    yield

    pool.close()

    logger.info("shutinnnng down")


app = FastAPI(
    title="Syncraflow",
    openapi_url=None if settings.envirement == "production" else "/openapi.json",
    docs_url=None if settings.envirement == "production" else "/docs",
    redoc_url=None if settings.envirement == "production" else "/redoc",
    lifespan=lifespan


)


@app.get("/")
async def welcome(db: Annotated[connection, Depends(get_conn)]):
    data = queries.get_all(db, 'test', ['id', 'phone'])

    initial_task.delay(data)

    return JSONResponse(
        content={
            "status": "Online",
            "message": "Welcome to SyncraFlow Engine API",
            "description": "High-performance event-driven automation backend.",
            "documentation": "/docs",
            "repository": "https://github.com/WassCodeur/syncraflow",
            "version": "1.0.0",
            "author": "Wachiou BOURAIMA (WassCodeur)",
            "email": "b.wachiou@pytogo.org",
            "version": "1.0.0"
        }
    )


app.include_router(users_router)
app.include_router(api_routes)
app.include_router(auth_router)
app.include_router(workflows_router)


@app.post("/tasts/status/{task_id}")
async def task_status(task_id: str):
    """Endpoint to check the status of a Celery task.

    Parameters
    ----------
    task_id : str
        The ID of the Celery task to check.

    Returns
    -------
    dict
        A dictionary containing the status message of the task.
    """
    task_result = AsyncResult(task_id)

    if task_result.ready():
        return {'message': f'task {task_id} is done'}
    elif task_result.failed():
        return {'message': f'task {task_id} is failed'}
    else:
        return {'message': f'task {task_id} is in progress'}

if __name__ == "__main__":
    pass
