import pandas as pd
from ...core.config import settings
import logging

logger = logging.getLogger(__name__)

def load_interaction_data(file_path: str) -> pd.DataFrame:
    """
    Carrega dados de interação de um arquivo CSV.
    """
    logger.info(f"Carregando dados de interação de {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"{len(df)} interações carregadas.")
    return df

def load_item_data(file_path: str) -> pd.DataFrame:
    """
    Carrega metadados de itens de um arquivo CSV.
    """
    logger.info(f"Carregando metadados de itens de {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"{len(df)} itens carregados.")
    return df
