import redis.asyncio as redis
import json
from typing import Optional, Any
from ..core.domain import TopicGraph
from ..core.interfaces import StateStore

class RedisStateStore(StateStore):
    def __init__(self, redis_url: str = "redis://redis:6379"):
        self.client = redis.from_url(redis_url, decode_responses=True)
        self.topic_key = "topic_graph"
        self.stick_key = "talking_stick"

    async def set_topic_graph(self, graph: TopicGraph) -> None:
        # Pydantic v2: model_dump_json
        await self.client.set(self.topic_key, graph.model_dump_json())

    async def get_topic_graph(self) -> Optional[TopicGraph]:
        data = await self.client.get(self.topic_key)
        if data:
            # Pydantic v2: model_validate_json
            return TopicGraph.model_validate_json(data)
        return None

    async def update_current_node(self, node_id: str) -> None:
        graph = await self.get_topic_graph()
        if graph:
            graph.current_node_id = node_id
            await self.set_topic_graph(graph)

    async def acquire_talking_stick(self, agent_id: str, timeout: int = 5) -> bool:
        """
        Uses Redis SET NX to acquire a lock.
        timeout: Lock expiry in seconds to prevent deadlocks.
        """
        acquired = await self.client.set(self.stick_key, agent_id, nx=True, ex=timeout)
        return bool(acquired)

    async def release_talking_stick(self, agent_id: str) -> None:
        """Release only if the caller owns the lock."""
        # Lua script to ensure atomicity
        script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        await self.client.eval(script, 1, self.stick_key, agent_id)

    async def publish_event(self, channel: str, message: dict) -> None:
        """Publish a message to a channel."""
        await self.client.publish(channel, json.dumps(message))

    async def subscribe_to_channel(self, channel: str) -> Any:
        """Subscribe to a channel and return a listener."""
        pubsub = self.client.pubsub()
        await pubsub.subscribe(channel)
        return pubsub
