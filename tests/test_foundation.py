import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from src.core.domain import TopicGraph, TopicNode
from src.infrastructure.redis_store import RedisStateStore
import json

@pytest.mark.asyncio
async def test_domain_models():
    """Test that Pydantic models are defined correctly."""
    node = TopicNode(id="1", label="Test", content="Content")
    graph = TopicGraph(nodes=[node], current_node_id="1")

    json_data = graph.model_dump_json()
    loaded_graph = TopicGraph.model_validate_json(json_data)

    assert loaded_graph.nodes[0].id == "1"
    assert loaded_graph.current_node_id == "1"

@pytest.mark.asyncio
async def test_redis_store_set_get():
    """Test RedisStateStore logic using mocks."""
    # Mock redis connection
    mock_client = AsyncMock()

    with patch("redis.asyncio.from_url", return_value=mock_client):
        store = RedisStateStore()

        node = TopicNode(id="1", label="Test", content="Content")
        graph = TopicGraph(nodes=[node], current_node_id="1")

        # Test Set
        await store.set_topic_graph(graph)
        mock_client.set.assert_called_once()
        args, _ = mock_client.set.call_args
        assert args[0] == "topic_graph"
        assert json.loads(args[1]) == graph.model_dump(mode='json')

        # Test Get
        mock_client.get.return_value = graph.model_dump_json()
        retrieved = await store.get_topic_graph()
        assert retrieved.nodes[0].id == "1"

@pytest.mark.asyncio
async def test_acquire_talking_stick():
    """Test distributed lock logic."""
    mock_client = AsyncMock()

    with patch("redis.asyncio.from_url", return_value=mock_client):
        store = RedisStateStore()

        # Scenario 1: Success
        mock_client.set.return_value = True
        result = await store.acquire_talking_stick("agent1")
        assert result is True
        mock_client.set.assert_called_with("talking_stick", "agent1", nx=True, ex=5)

        # Scenario 2: Failure (Lock held by someone else)
        mock_client.set.return_value = None # redis-py returns None if NX fails
        result = await store.acquire_talking_stick("agent2")
        assert result is False

@pytest.mark.asyncio
async def test_release_talking_stick():
    """Test release logic with Lua script."""
    mock_client = AsyncMock()

    with patch("redis.asyncio.from_url", return_value=mock_client):
        store = RedisStateStore()

        await store.release_talking_stick("agent1")
        mock_client.eval.assert_called_once()
