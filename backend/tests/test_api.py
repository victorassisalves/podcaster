from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Podcaster API is running"}

def test_get_agents():
    response = client.get("/api/agents")
    assert response.status_code == 200
    assert len(response.json()) > 0
