from fastapi import APIRouter
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.upload import router as upload_router
from app.api.routes.equipment import router as equipment_router
from app.api.routes.stats import router as stats_router
api_router = APIRouter()

api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"]
)
api_router.include_router(
    upload_router,
    prefix="/upload",
    tags=["Upload"]
)
api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"],
)
api_router.include_router(
    equipment_router,
    prefix="/equipment",
    tags=["Equipment"],
)
api_router.include_router(
    stats_router,
    prefix="/stats",
    tags=["Stats"],
)