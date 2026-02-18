from contextlib import asynccontextmanager
from psycopg.sql import SQL, Identifier
from psycopg.types.json import Jsonb
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from psycopg_pool import ConnectionPool
from app.auth.routes import router as auth_router
from app.auth.user import router as users_router
from app.core.config import get_config
from app.database import queries, connection


config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    pass


app = FastAPI(
    openapi_url=None if config.envirement == "production" else "/openapi.json",
    docs_url=None if config.envirement == "production" else "/docs",
    redoc_url=None if config.envirement == "production" else "/redoc",

)


app.include_router(auth_router)
app.include_router(users_router)


@app.get("/", dependencies=[])
async def welcome():
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


thing = {
    "number": 4,
    "name": "Test"
}
filter = {
    "number": 4
}

try:
    queries.insert('test', thing)
except Exception as e:
    print(e)

# print(queries.get_all('test', ['id', 'phone']))

queries.update('test', filter=thing, new_data={'name': 'Wasscodeur'})

# print(queries.delete('test', filter=filter))

print(queries.get_one('test', ['id', 'number', 'name'], filter=filter))
if __name__ == "__main__":
    pass
