from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.model import TrainRequest, EvaluationResponse
from app.ml.training.train import train_model
from app.ml.training.evaluate import evaluate_model
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/models/train", status_code=202, tags=["Models"])
async def trigger_model_training(request: TrainRequest, background_tasks: BackgroundTasks):
    """
    Inicia o treinamento de um novo modelo em background.
    """
    logger.info(f"Requisição de treinamento para modelo: {request.model_type}")
    
    background_tasks.add_task(
        train_model, 
        model_type=request.model_type, 
        hyperparameters=request.hyperparameters
    )
    
    return {"message": "Treinamento do modelo iniciado em background."}

@router.get("/models/{model_id}/evaluate", response_model=EvaluationResponse, tags=["Models"])
async def get_model_evaluation(model_id: str):
    """
    Retorna as métricas de avaliação para um modelo específico.
    """
    logger.info(f"Requisição de avaliação para o modelo_id: {model_id}")
    
    try:
        metrics = evaluate_model(model_path=f"models/{model_id}.pkl", test_data="data/test.csv")
        
        if not metrics:
            raise HTTPException(status_code=404, detail=f"Modelo ou avaliação para '{model_id}' não encontrado.")

        return EvaluationResponse(
            model_id=model_id,
            metrics=metrics
        )
    except FileNotFoundError:
        logger.warning(f"Arquivo de modelo para '{model_id}' não encontrado.")
        raise HTTPException(status_code=404, detail=f"Modelo '{model_id}' não encontrado.")
    except Exception as e:
        logger.error(f"Erro ao avaliar modelo '{model_id}': {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao avaliar o modelo.")
