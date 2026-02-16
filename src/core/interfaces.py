from abc import ABC, abstractmethod
from typing import Optional, List, Any, AsyncIterator
from .domain import TopicGraph, TopicNode

class StateStore(ABC):
    """Interface for managing shared state (Redis)."""

    @abstractmethod
    async def set_topic_graph(self, graph: TopicGraph) -> None:
        pass

    @abstractmethod
    async def get_topic_graph(self) -> Optional[TopicGraph]:
        pass

    @abstractmethod
    async def update_current_node(self, node_id: str) -> None:
        pass

    @abstractmethod
    async def acquire_talking_stick(self, agent_id: str, timeout: int = 5) -> bool:
        """Try to acquire the lock to speak. Returns True if acquired."""
        pass

    @abstractmethod
    async def release_talking_stick(self, agent_id: str) -> None:
        pass

    @abstractmethod
    async def publish_event(self, channel: str, message: dict) -> None:
        """Publish a message to a channel."""
        pass

    @abstractmethod
    @abstractmethod
    async def add_to_stream(self, stream_key: str, fields: dict) -> str:
        """Add a message to a Redis Stream. Returns the message ID."""
        pass

    async def subscribe_to_channel(self, channel: str) -> Any:
        """Subscribe to a channel and return a listener."""
        pass

class LlmProvider(ABC):
    """Interface for LLM generation."""
    @abstractmethod
    async def generate_response(self, prompt: str, history: List[dict]) -> str:
        pass

class AudioProvider(ABC):
    """Interface for Audio/WebRTC (LiveKit)."""
    @abstractmethod
    async def stream_audio(self, text: str, voice_id: str) -> None:
        pass
