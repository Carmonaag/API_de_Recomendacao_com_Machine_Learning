from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_health_check():
    """
    Testa o endpoint /health.
    """
    response = client.get("/health")
    assert response.status_code == 200
    # O status do banco de dados pode variar, então testamos apenas as chaves
    assert "status" in response.json()
    assert "db_status" in response.json()

def test_root():
    """
    Testa o endpoint raiz (/).
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "Recommendation ML API"


@patch('app.api.v1.endpoints.recommendations.get_from_cache')
@patch('app.api.v1.endpoints.recommendations.set_to_cache')
def test_get_recommendations_default(mock_set_to_cache, mock_get_from_cache):
    """
    Testa o endpoint de recomendações com valores padrão.
    """
    mock_get_from_cache.return_value = None
    user_id = "user1"
    response = client.post(f"/api/v1/recommendations/user/{user_id}", json={})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["user_id"] == user_id
    assert data["strategy_used"] == "hybrid"
    assert len(data["recommendations"]) <= 5


@patch('app.api.v1.endpoints.recommendations.get_from_cache')
@patch('app.api.v1.endpoints.recommendations.set_to_cache')
def test_get_recommendations_with_filter(mock_set_to_cache, mock_get_from_cache):
    """
    Testa o endpoint de recomendações com filtro de categoria.
    """
    mock_get_from_cache.return_value = None
    user_id = "user1"
    request_body = {
        "n_items": 5,
        "strategy": "content_based",
        "filters": {"category": "cat1"}
    }
    
    response = client.post(f"/api/v1/recommendations/user/{user_id}", json=request_body)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["strategy_used"] == "content_based"
    # Verifica se todos os itens recomendados são da categoria correta
    # Esta parte do teste depende dos dados de exemplo e da lógica do modelo
    # Pode ser necessário ajustar dependendo da implementação real


@patch('app.api.v1.endpoints.recommendations.get_from_cache')
@patch('app.api.v1.endpoints.recommendations.set_to_cache')
def test_recommendation_for_new_user(mock_set_to_cache, mock_get_from_cache):
    """
    Testa o endpoint de recomendações para um novo usuário.
    """
    mock_get_from_cache.return_value = None
    user_id = "new_user_test"
    response = client.post(f"/api/v1/recommendations/user/{user_id}", json={})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["user_id"] == user_id
    assert len(data["recommendations"]) > 0


@patch('app.api.v1.endpoints.recommendations.get_from_cache', return_value={"user_id": "user1", "recommendations": [], "strategy_used": "hybrid", "model_version": "test"})
def test_recommendation_cache_hit(mock_get_from_cache):
    """
    Testa se o cache de recomendações está funcionando.
    """
    user_id = "user1"
    response = client.post(f"/api/v1/recommendations/user/{user_id}", json={})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["cache_hit"] == True
    mock_get_from_cache.assert_called_once()