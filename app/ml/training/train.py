import logging
from app.ml.models.collaborative_filtering import CollaborativeFilteringModel
from app.ml.models.content_based import ContentBasedModel
from app.data.sample_data import get_sample_interactions, get_sample_items
from app.core.config import settings

logger = logging.getLogger(__name__)

def train_model(model_type: str, hyperparameters: dict = None):
    """
    Trains and saves a machine learning model.
    """
    logger.info(f"Starting training for model: {model_type}...")
    logger.info(f"Hyperparameters: {hyperparameters}")

    if model_type == "collaborative":
        interactions = get_sample_interactions()
        model = CollaborativeFilteringModel()
        model.train(interactions)
        output_path = settings.CF_MODEL_PATH
        model.save_model(output_path)
    elif model_type == "content_based":
        items = get_sample_items()
        model = ContentBasedModel()
        model.train(items)
        output_path = settings.CB_MODEL_PATH
        model.save_model(output_path)
    else:
        logger.error(f"Unknown model type: {model_type}")
        return

    logger.info(f"Training complete! Model saved to: {output_path}")
