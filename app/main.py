from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from app.auth.routes import router as auth_router
from app.auth.user import router as users_router
from app.core.config import get_config
from app.database.connection import db_connection

config = get_config()


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


print(conn)

if __name__ == "__main__":
    pass
