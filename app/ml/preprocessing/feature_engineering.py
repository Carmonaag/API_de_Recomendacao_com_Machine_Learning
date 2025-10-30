import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logger = logging.getLogger(__name__)

def create_interaction_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria uma matriz de interação usuário-item.

    Args:
        df (pd.DataFrame): DataFrame com colunas 'user_id', 'item_id', 'rating'.

    Returns:
        pd.DataFrame: Matriz com usuários como linhas, itens como colunas e ratings como valores.
    """
    logger.info("Criando matriz de interação usuário-item...")
    interaction_matrix = df.pivot_table(index='user_id', columns='item_id', values='rating')
    logger.info(f"Matriz de interação criada com shape: {interaction_matrix.shape}")
    return interaction_matrix

def create_tfidf_matrix(items_df: pd.DataFrame) -> tuple:
    """
    Cria uma matriz TF-IDF para as características textuais dos itens.

    Args:
        items_df (pd.DataFrame): DataFrame com 'item_id' e 'description'.

    Returns:
        tuple: Matriz TF-IDF e o objeto vectorizer.
    """
    logger.info("Criando matriz TF-IDF para características dos itens...")
    items_df['description'] = items_df['description'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(items_df['description'])
    logger.info(f"Matriz TF-IDF criada com shape: {tfidf_matrix.shape}")
    return tfidf_matrix, tfidf

def preprocess_data_for_hybrid(df: pd.DataFrame, items_df: pd.DataFrame) -> dict:
    """
    Prepara todos os dados necessários para o modelo híbrido.

    Args:
        df (pd.DataFrame): DataFrame de interações.
        items_df (pdDataFrame): DataFrame de itens.

    Returns:
        dict: Dicionário contendo 'interaction_matrix' e 'tfidf_matrix'.
    """
    logger.info("Pré-processando dados para o modelo híbrido...")
    interaction_matrix = create_interaction_matrix(df)
    tfidf_matrix, _ = create_tfidf_matrix(items_df)
    
    processed_data = {
        "interaction_matrix": interaction_matrix,
        "tfidf_matrix": tfidf_matrix
    }
    logger.info("Dados pré-processados com sucesso.")
    return processed_data
