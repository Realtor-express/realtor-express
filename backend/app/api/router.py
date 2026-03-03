from fastapi import APIRouter

from app.api.routes import auth, agent, broadcasts, admin, directory

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])
api_router.include_router(broadcasts.router, prefix="/broadcasts", tags=["Broadcast"])
api_router.include_router(directory.router, prefix="/directory", tags=["Directory"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
