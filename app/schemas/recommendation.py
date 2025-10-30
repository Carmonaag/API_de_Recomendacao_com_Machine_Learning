from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, UTC

class RecommendationFilters(BaseModel):
    category: Optional[str] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)

class RecommendationRequest(BaseModel):
    n_items: int = Field(default=5, ge=1, le=50, description="Número de itens a serem recomendados")
    strategy: str = Field(default="hybrid", description="Estratégia de recomendação: 'collaborative', 'content_based', 'hybrid'")
    filters: Optional[RecommendationFilters] = None

class RecommendedItem(BaseModel):
    item_id: Any
    score: float = Field(..., description="Pontuação de relevância da recomendação")
    title: Optional[str] = None
    category: Optional[str] = None
    predicted_rating: Optional[float] = None

class RecommendationResponse(BaseModel):
    user_id: Any
    recommendations: List[RecommendedItem]
    strategy_used: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    cache_hit: bool = False
    model_version: Optional[str] = None
