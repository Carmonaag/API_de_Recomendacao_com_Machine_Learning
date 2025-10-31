import pytest
from unittest.mock import patch
from app.ml.models.collaborative_filtering import CollaborativeFilteringModel
from app.ml.models.content_based import ContentBasedModel
from app.ml.models.hybrid import HybridModel


@patch('app.ml.models.collaborative_filtering.get_sample_interactions')
def test_collaborative_model(mock_get_sample_interactions, sample_data):
    """
    Testa o modelo de filtro colaborativo com dados mockados.
    """
    mock_get_sample_interactions.return_value = sample_data["interactions"]
    
    model = CollaborativeFilteringModel()
    model.train()

    # Testa predição para um usuário existente
    recs = model.predict(user_id="user1", n_items=2)
    assert isinstance(recs, list)
    assert len(recs) == 2
    assert "item_id" in recs[0]
    assert "score" in recs[0]

    # Testa predição para um novo usuário (deve retornar as recomendações mais populares)
    recs_new_user = model.predict(user_id="new_user", n_items=3)
    assert isinstance(recs_new_user, list)
    assert len(recs_new_user) == 3
    # O item mais popular é 'item1' e 'item2'
    assert recs_new_user[0]['item_id'] in ['item1', 'item2']


@patch('app.ml.models.content_based.get_sample_interactions')
@patch('app.ml.models.content_based.ContentBasedModel.item_data')
def test_content_based_model(mock_item_data, mock_get_sample_interactions, sample_data):
    """
    Testa o modelo baseado em conteúdo com dados mockados.
    """
    mock_get_sample_interactions.return_value = sample_data["interactions"]
    mock_item_data.return_value = sample_data["items"]

    model = ContentBasedModel()
    model.train()

    # Testa predição para um usuário existente
    recs = model.predict(user_id="user1", n_items=2)
    assert isinstance(recs, list)
    assert len(recs) == 2
    assert "item_id" in recs[0]
    assert "score" in recs[0]

    # Testa se as recomendações são da mesma categoria que o usuário interagiu
    user1_interacted_items = sample_data["interactions"][sample_data["interactions"]['user_id'] == 'user1']['item_id']
    user1_interacted_categories = sample_data["items"][sample_data["items"]['item_id'].isin(user1_interacted_items)]['category'].unique()
    recommended_categories = sample_data["items"][sample_data["items"]['item_id'].isin([r['item_id'] for r in recs])]['category'].unique()
    assert any(cat in recommended_categories for cat in user1_interacted_categories)


@patch('app.ml.models.hybrid.get_sample_interactions')
@patch('app.ml.models.hybrid.CollaborativeFilteringModel.load_model')
@patch('app.ml.models.hybrid.ContentBasedModel.load_model')
def test_hybrid_model(mock_cb_load, mock_cf_load, mock_get_sample_interactions, sample_data):
    """
    Testa o modelo híbrido com dados mockados.
    """
    mock_get_sample_interactions.return_value = sample_data
    mock_cf_load.return_value = None
    mock_cb_load.return_value = None

    model = HybridModel()
    model.cf_model.train_data = sample_data["interactions"]
    model.cb_model.item_data = sample_data["items"]
    model.cb_model.train_tfidf_matrix()

    # Testa a estratégia híbrida
    recs = model.predict(user_id="user1", n_items=3, strategy="hybrid", filters={})
    assert isinstance(recs, list)
    assert len(recs) <= 3

    # Testa a estratégia colaborativa
    recs_cf = model.predict(user_id="user1", n_items=2, strategy="collaborative", filters={})
    assert isinstance(recs_cf, list)
    assert len(recs_cf) == 2

    # Testa a estratégia baseada em conteúdo
    recs_cb = model.predict(user_id="user1", n_items=2, strategy="content_based", filters={})
    assert isinstance(recs_cb, list)
    assert len(recs_cb) == 2