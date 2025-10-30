from fastapi import APIRouter, HTTPException
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse, RecommendedItem
from app.ml.models.hybrid import HybridModel
from app.core.cache import get_from_cache, set_to_cache
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

model = HybridModel()

@router.post("/recommendations/user/{user_id}", response_model=RecommendationResponse)
async def get_recommendations(
    user_id: str,
    request: RecommendationRequest
):
    """
    Gera e retorna uma lista de itens recomendados para um usuário específico.
    """
    logger.info(f"Requisição de recomendação para user_id: {user_id} com estratégia: {request.strategy}")

    cache_key = f"user_recs:{user_id}:{request.strategy}:{request.n_items}"
    cached_result = await get_from_cache(cache_key)
    if cached_result:
        logger.info(f"Cache hit para user_id: {user_id}")
        response = RecommendationResponse(**cached_result)
        response.cache_hit = True
        return response

    logger.info(f"Cache miss para user_id: {user_id}. Gerando novas recomendações.")
    
    try:
        recommended_items_data = model.predict(
            user_id=user_id, 
            n_items=request.n_items, 
            strategy=request.strategy,
            filters=request.filters.model_dump() if request.filters else {}
        )

        recommendations = [RecommendedItem(**item) for item in recommended_items_data]

    except Exception as e:
        logger.error(f"Erro ao gerar recomendações para user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao gerar recomendações.")

    response = RecommendationResponse(
        user_id=user_id,
        recommendations=recommendations,
        strategy_used=request.strategy,
        model_version=model.version
    )

    await set_to_cache(cache_key, response.model_dump())

    return response