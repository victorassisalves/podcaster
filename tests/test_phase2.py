import pytest
import asyncio
import json
from src.core.interfaces import StateStore
from src.core.domain import TopicGraph, TopicNode, TopicEdge
from src.agents.producer.agent import ProducerAgent

# Mocking StateStore
class MockStateStore(StateStore):
    def __init__(self):
        self.graph = None
        self.events = []

    async def set_topic_graph(self, graph: TopicGraph) -> None:
        self.graph = graph

    async def get_topic_graph(self):
        return self.graph

    async def update_current_node(self, node_id: str) -> None:
        pass

    async def acquire_talking_stick(self, agent_id: str, timeout: int = 5) -> bool:
        return True

    async def release_talking_stick(self, agent_id: str) -> None:
        pass

    async def publish_event(self, channel: str, message: dict) -> None:
        self.events.append((channel, message))

    async def subscribe_to_channel(self, channel: str):
        pass

# Dummy Agent to bypass strict initialization
class DummyAgent:
    def __init__(self, state_store):
        self.state_store = state_store
        self.model = "test-model"

@pytest.mark.asyncio
async def test_producer_tools():
    store = MockStateStore()

    # We create a dummy instance and bind the ProducerAgent methods to it manually
    agent = DummyAgent(store)

    # Test perform_research logic
    # perform_research is defined on ProducerAgent. Since we didn't inherit, we call it unbound passing 'agent' as self.
    summary_json = ProducerAgent.perform_research(agent, "WebRTC")

    print(f"Summary: {summary_json}")
    # The summary is a JSON string containing key_facts
    summary = json.loads(summary_json)
    assert "key_facts" in summary
    assert isinstance(summary["key_facts"], list)

    # Test finalize_episode logic
    graph_data = {
        "nodes": [
            {"id": "1", "label": "Intro", "content": "Welcome"},
            {"id": "2", "label": "Body", "content": "Content"},
            {"id": "3", "label": "Conclusion", "content": "Bye"},
            {"id": "4", "label": "Extra", "content": "More"},
            {"id": "5", "label": "Credits", "content": "Team"}
        ],
        "edges": [],
        "current_node_id": "1"
    }

    # We call finalize_episode, which is synchronous but spawns an async task using get_running_loop()
    # Since pytest-asyncio runs the test in a loop, get_running_loop() should work.
    result = ProducerAgent.finalize_episode(agent, graph_data)
    print(f"Result: {result}")
    assert "published" in result

    # Allow the background task spawned by create_task to run
    await asyncio.sleep(0.1)

    assert store.graph is not None
    assert len(store.graph.nodes) == 5
    assert len(store.events) > 0
    assert store.events[0][0] == "EPISODE_READY"
    assert store.events[0][1]["initial_node"] == "1"
