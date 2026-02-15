from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_agent():
    agent_data = {
        "name": "Test Agent",
        "role": "Guest",
        "personality": "Test Personality",
        "voice_id": "Puck"
    }
    response = client.post("/api/agents", json=agent_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Agent"
    assert data["role"] == "Guest"
    assert data["id"] is not None

def test_get_agents_includes_new_agent():
    # First create one
    client.post("/api/agents", json={
        "name": "Newbie",
        "role": "Host",
        "personality": "New",
        "voice_id": "Charley"
    })

    response = client.get("/api/agents")
    assert response.status_code == 200
    agents = response.json()
    # Check for default agents
    assert any(a["name"] == "Alex" for a in agents)
    # Check for new agent
    assert any(a["name"] == "Newbie" for a in agents)
