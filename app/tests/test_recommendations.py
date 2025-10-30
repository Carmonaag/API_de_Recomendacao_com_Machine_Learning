from fastapi.testclient import TestClient
from ..main import app
from unittest.mock import patch

client = TestClient(app)

@patch("app.api.v1.endpoints.recommendations.get_from_cache")
@patch("app.api.v1.endpoints.recommendations.set_to_cache")
@patch("app.api.v1.endpoints.recommendations.model.predict")
def test_get_recommendations(mock_predict, mock_set_to_cache, mock_get_from_cache):
    mock_get_from_cache.return_value = None
    mock_predict.return_value = [
        {"item_id": "A", "score": 0.9},
        {"item_id": "B", "score": 0.8},
    ]

    response = client.post("/api/v1/recommendations/user/123", json={"n_items": 2})

    assert response.status_code == 200
    assert "recommendations" in response.json()
    assert len(response.json()["recommendations"]) == 2
    assert response.json()["recommendations"][0]["item_id"] == "A"
