from fastapi.testclient import TestClient
from ..main import app
from unittest.mock import patch
from ..schemas.model import EvaluationMetrics

client = TestClient(app)

@patch("app.api.v1.endpoints.models.train_model")
def test_trigger_model_training(mock_train_model):
    response = client.post("/api/v1/models/train", json={"model_type": "collaborative"})

    assert response.status_code == 202
    assert response.json() == {"message": "Treinamento do modelo iniciado em background."}
    mock_train_model.assert_called_once_with(model_type="collaborative", hyperparameters=None)

@patch("app.api.v1.endpoints.models.evaluate_model")
def test_get_model_evaluation(mock_evaluate_model):
    mock_metrics = EvaluationMetrics(
        rmse=0.85,
        mae=0.65,
        precision_at_5=0.8,
        recall_at_5=0.75,
        f1_score=0.77
    )
    mock_evaluate_model.return_value = mock_metrics

    response = client.get("/api/v1/models/some_model/evaluate")

    assert response.status_code == 200
    assert "model_id" in response.json()
    assert "metrics" in response.json()
    assert response.json()["metrics"]["rmse"] == 0.85
