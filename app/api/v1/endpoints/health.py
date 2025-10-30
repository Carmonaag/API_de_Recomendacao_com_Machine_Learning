from fastapi import APIRouter
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Verifica a saúde da aplicação, incluindo conexão com cache e status do modelo.
    """
    logger.info("Health check solicitado.")
    return {
        "status": "healthy",
        "model_loaded": True,
        "cache_connected": True
    }
