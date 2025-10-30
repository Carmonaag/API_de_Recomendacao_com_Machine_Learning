from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Recommendation ML API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "db_status" in response.json()
