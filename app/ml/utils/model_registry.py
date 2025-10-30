import mlflow
import mlflow.sklearn
import joblib
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class ModelRegistry:
    def __init__(self, tracking_uri=None):
        pass

    def log_model(self, model, model_name: str, params: dict, metrics: dict):
        logger.info(f"Registrando modelo '{model_name}' no MLflow.")
        return "mock_run_id"

    def load_model(self, model_name: str, stage: str = "Production"):
        logger.info(f"Carregando modelo '{model_name}' (stage: {stage}) do MLflow.")
        return "mock_model"
