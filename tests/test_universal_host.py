import pytest
import json
import asyncio
import os
from unittest.mock import MagicMock, AsyncMock, patch
from src.core.domain import HostPersona, TopicGraph, TopicNode
from src.infrastructure.redis_store import RedisStateStore
from src.agents.universal_host.engine import UniversalHostAgent

# Mock Redis
@pytest.fixture
def mock_redis():
    mock = AsyncMock()
    mock.xadd.return_value = "12345-0"
    mock.set.return_value = True
    return mock

@pytest.fixture
def store(mock_redis):
    store = RedisStateStore()
    store.client = mock_redis
    return store

def test_host_persona_validation():
    data = {
        "id": "test_host",
        "name": "Test Host",
        "voice_id": "voice_123",
        "system_prompt": "You are a test.",
        "interruption_sensitivity": 0.5,
        "voice_settings": {"stability": 0.5},
        "interaction_rules": ["Be nice"],
        "a2a_id": "agent_test"
    }
    persona = HostPersona(**data)
    assert persona.voice_settings["stability"] == 0.5
    assert "Be nice" in persona.interaction_rules
    assert persona.a2a_id == "agent_test"

@pytest.mark.asyncio
async def test_add_to_stream(store, mock_redis):
    msg_id = await store.add_to_stream("test_stream", {"foo": "bar"})
    mock_redis.xadd.assert_called_with("test_stream", {"foo": "bar"})
    assert msg_id == "12345-0"

@pytest.mark.asyncio
async def test_agent_initialization(store):
    # Mock persona loading and genai client
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.read.return_value = json.dumps({
            "id": "host_sascha",
            "name": "Sascha",
            "voice_id": "v1",
            "system_prompt": "prompt",
            "a2a_id": "sascha",
            "voice_settings": {},
            "interaction_rules": []
        })

        with patch("json.load", return_value={
            "id": "host_sascha",
            "name": "Sascha",
            "voice_id": "v1",
            "system_prompt": "prompt",
            "a2a_id": "sascha",
            "voice_settings": {},
            "interaction_rules": []
        }):
            with patch("os.path.exists", return_value=True):
                with patch("google.genai.Client") as MockGenClient:
                    # Set a dummy API key in env just in case, or rely on Mock
                    with patch.dict(os.environ, {"GOOGLE_API_KEY": "dummy"}):
                         agent = UniversalHostAgent("test_agent", "host_sascha", store)
                         assert agent.persona.name == "Sascha"
                         MockGenClient.assert_called()

@pytest.mark.asyncio
async def test_acquire_talking_stick(store, mock_redis):
    acquired = await store.acquire_talking_stick("agent_1", timeout=5)
    mock_redis.set.assert_called_with("talking_stick", "agent_1", nx=True, ex=5)
    assert acquired is True
