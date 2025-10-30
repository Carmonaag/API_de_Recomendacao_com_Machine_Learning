import logging
from app.data.sample_data import get_sample_interactions, get_sample_items
from app.ml.models.collaborative_filtering import CollaborativeFilteringModel
from app.ml.models.content_based import ContentBasedModel
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_all_models():
    """Treina e salva todos os modelos de recomendação."""
    logger.info("Iniciando o treinamento de todos os modelos...")

    # Carregar dados
    interactions = get_sample_interactions()
    items = get_sample_items()

    # Treinar e salvar modelo de filtro colaborativo
    logger.info("Treinando o modelo de Filtro Colaborativo...")
    cf_model = CollaborativeFilteringModel(n_components=2)
    cf_model.train(interactions)
    cf_model.save_model(settings.CF_MODEL_PATH)
    logger.info(f"Modelo de Filtro Colaborativo salvo em: {settings.CF_MODEL_PATH}")

    # Treinar e salvar modelo baseado em conteúdo
    logger.info("Treinando o modelo Baseado em Conteúdo...")
    cb_model = ContentBasedModel()
    cb_model.train(items)
    cb_model.save_model(settings.CB_MODEL_PATH)
    logger.info(f"Modelo Baseado em Conteúdo salvo em: {settings.CB_MODEL_PATH}")

    logger.info("Treinamento de todos os modelos concluído com sucesso!")

if __name__ == "__main__":
    train_all_models()
