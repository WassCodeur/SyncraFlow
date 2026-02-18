from contextlib import asynccontextmanager
from psycopg.sql import SQL, Identifier
from psycopg.types.json import Jsonb
from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
from psycopg_pool import ConnectionPool
from app.auth.routes import router as auth_router
from app.auth.user import router as users_router
from app.core.config import get_config, setup_logging
from app.database import queries
from app.database.connection import get_conn, get_connection_pool
from typing import Annotated
from psycopg import connection


config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = setup_logging()
    logger.info("Starting Up")
    pool = get_connection_pool()

    app.state.conn_pool = pool

    pool.open()
    yield

    pool.close()

    logger.info("shutinnnng down")


app = FastAPI(
    openapi_url=None if config.envirement == "production" else "/openapi.json",
    docs_url=None if config.envirement == "production" else "/docs",
    redoc_url=None if config.envirement == "production" else "/redoc",
    lifespan=lifespan

)


app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
async def welcome(db: Annotated[connection, Depends(get_conn)]):

    thing = {
        "number": 12,
        "name": "hello"
    }
    filter = {
        "number": 4
    }
    # print(queries.insert(db, 'test', thing))

    print(queries.get_all(db, 'test', ['id', 'phone']))

    # queries.update('test', filter=thing, new_data={'name': 'Wasscodeur'})
    # print(queries.get_one(db, 'test', [
    #      'id', 'number', 'name'], filter=filter))

    # print(queries.delete('test', filter=filter))

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


if __name__ == "__main__":
    pass
