from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class TrainRequest(BaseModel):
    model_type: str = Field(..., description="Tipo de modelo a ser treinado: 'collaborative', 'content_based'")
    hyperparameters: Optional[Dict[str, Any]] = None

class EvaluationMetrics(BaseModel):
    rmse: float
    mae: float
    precision_at_5: float
    recall_at_5: float
    f1_score: float

class EvaluationResponse(BaseModel):
    model_id: str
    metrics: EvaluationMetrics
    evaluation_date: datetime = Field(default_factory=datetime.utcnow)
