from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Testa o endpoint /health.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "model_loaded": True,
        "cache_connected": True
    }

def test_root():
    """
    Testa o endpoint raiz (/).
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "Recommendation ML API"

def test_get_recommendations_default():
    """
    Testa o endpoint de recomendações com valores padrão (corpo vazio).
    """
    user_id = "test-user-123"
    # Enviamos um corpo JSON vazio para usar os valores padrão do modelo Pydantic
    response = client.post(f"/api/v1/recommendations/user/{user_id}", json={})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["user_id"] == user_id
    assert data["strategy_used"] == "hybrid"  # Estratégia padrão
    assert "recommendations" in data
    
    recommendations = data["recommendations"]
    assert isinstance(recommendations, list)
    assert len(recommendations) == 5  # n_items padrão
    
    if len(recommendations) > 0:
        first_item = recommendations[0]
        assert "item_id" in first_item
        assert "score" in first_item

def test_get_recommendations_with_params():
    """
    Testa o endpoint de recomendações com parâmetros customizados.
    """
    user_id = "test-user-456"
    request_body = {"n_items": 10, "strategy": "collaborative"}
    
    response = client.post(
        f"/api/v1/recommendations/user/{user_id}",
        json=request_body
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["user_id"] == user_id
    assert data["strategy_used"] == "collaborative"
    assert len(data["recommendations"]) == 10
