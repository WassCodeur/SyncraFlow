from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from app.models.users import UserData
from app.routers.auths import router as auth_router
from app.routers.user import router as users_router
from app.utils.auth_utils import authentication, current_active_user


app = FastAPI()


app.include_router(auth_router)
app.include_router(users_router)


@app.get("/", dependencies=[Depends(current_active_user)])
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


if __name__ == "__main__":
    print(authentication("andrewbean", "Pass1234"))
    pass
