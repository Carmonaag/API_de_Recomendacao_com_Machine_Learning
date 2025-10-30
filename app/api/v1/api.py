from fastapi import APIRouter
from .endpoints import recommendations, models, health, users, items

api_router = APIRouter()

api_router.include_router(recommendations.router, tags=["Recommendations"])
api_router.include_router(models.router, tags=["Models"])
api_router.include_router(health.router, tags=["Monitoring"])
api_router.include_router(users.router, tags=["Users"])
api_router.include_router(items.router, tags=["Items"])
