import pytest
from app.ml.models.collaborative_filtering import CollaborativeFilteringModel
from app.ml.models.content_based import ContentBasedModel
from app.ml.models.hybrid import HybridModel

def test_collaborative_model():
    """
    Testa o placeholder do modelo de filtro colaborativo.
    """
    model = CollaborativeFilteringModel()
    n_items = 5
    recs = model.predict(user_id="test", n_items=n_items)
    
    assert isinstance(recs, list)
    assert len(recs) == n_items
    if n_items > 0:
        assert "item_id" in recs[0]
        assert "score" in recs[0]

def test_content_based_model():
    """
    Testa o placeholder do modelo baseado em conteúdo.
    """
    model = ContentBasedModel()
    n_items = 7
    recs = model.predict(user_id="test", n_items=n_items)
    
    assert isinstance(recs, list)
    assert len(recs) == n_items
    if n_items > 0:
        assert "item_id" in recs[0]
        assert "score" in recs[0]

def test_hybrid_model():
    """
    Testa o placeholder do modelo híbrido.
    """
    model = HybridModel()
    n_items = 10
    # O modelo híbrido precisa de mais argumentos
    recs = model.predict(user_id="test", n_items=n_items, strategy="hybrid", filters={})
    
    assert isinstance(recs, list)
    # O modelo híbrido pode retornar menos itens se houver sobreposição
    assert len(recs) <= n_items
    if len(recs) > 0:
        assert "item_id" in recs[0]
        assert "score" in recs[0]
