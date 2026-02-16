import os
import json
import asyncio
import logging
from typing import Optional
from google import genai
from google.genai import types
from google.adk import agents, runners, events
from google.adk.agents.run_config import RunConfig

from ...core.domain import HostPersona, TopicGraph
from ...core.interfaces import StateStore
from ...agents.base import BaseAgent
from ...infrastructure.livekit_adapter import LiveKitAdapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversalHostAgent(BaseAgent):
    persona_id: str
    model_name: str
    persona: Optional[HostPersona] = None
    _adapter: Optional[LiveKitAdapter] = None

    def __init__(
        self,
        name: str,
        persona_id: str,
        state_store: StateStore,
        model_name: str = "gemini-3.0-flash-preview"
    ):
        super().__init__(
            name=name,
            state_store=state_store,
            persona_id=persona_id,
            model_name=model_name,
            persona=None
        )
        self._load_persona()
        self._adapter = LiveKitAdapter()

    def _load_persona(self):
        """Loads the persona JSON file."""
        try:
            persona_path = f"src/personas/{self.persona_id}.json"
            if not os.path.exists(persona_path):
                 logger.error(f"Persona file not found: {persona_path}")
                 return

            with open(persona_path, "r") as f:
                data = json.load(f)
                self.persona = HostPersona(**data)

            logger.info(f"Loaded persona: {self.persona.name} ({self.persona.id})")
        except Exception as e:
            logger.error(f"Failed to load persona {self.persona_id}: {e}")
            raise

    async def run_loop(self):
        """
        The main execution loop for Phase 4 (Bidi-Streaming).
        """
        logger.info(f"Agent {self.name} starting run_loop (Phase 4)...")

        # 1. Wait for EPISODE_READY (State A)
        pubsub = await self.state_store.subscribe_to_channel("EPISODE_READY")
        logger.info("State A: Idle. Waiting for EPISODE_READY...")
        async for message in pubsub.listen():
            if message["type"] == "message":
                logger.info("Received EPISODE_READY. Switching to State B: Active.")
                break

        # 2. Initialize & Connect Adapter
        room_id = os.getenv("LIVEKIT_ROOM", "daily_room")
        logger.info(f"Connecting to LiveKit room: {room_id}")
        await self._adapter.start_session(room_id)

        # 3. Setup ADK Agent
        graph = await self.state_store.get_topic_graph()
        current_node_context = ""
        if graph and graph.current_node_id:
            node = next((n for n in graph.nodes if n.id == graph.current_node_id), None)
            if node:
                current_node_context = f"Current Topic: {node.label}\nKey Facts: {node.content}"

        system_instruction = f"""
You are {self.persona.name}, a podcast host.
Your personality: {self.persona.system_prompt}
Voice Settings: {self.persona.voice_settings}
Interaction Rules: {self.persona.interaction_rules}

{current_node_context}

Task: Engage in a natural conversation. You are live on air.
"""

        adk_agent = agents.Agent(
            name=self.name,
            model=self.model_name,
            system_prompt=system_instruction
        )

        # 4. Run Live Loop
        runner = runners.Runner(agent=adk_agent)
        queue = self._adapter.live_request_queue
        config = RunConfig(response_modalities=["AUDIO"])

        logger.info("Starting run_live loop...")

        try:
            async for event in runner.run_live(live_request_queue=queue, run_config=config):
                # Handle interruptions
                if getattr(event, "interrupted", False):
                    logger.info("Interruption detected (Cognitive Rewind).")
                    await self.state_store.add_to_stream(
                        "conversation_stream",
                        {
                            "type": "SYSTEM_SIGNAL",
                            "event": "INTERRUPTION",
                            "agent_id": self.name,
                            "timestamp": str(asyncio.get_event_loop().time()),
                            "metadata": { "last_token_index": 0 }
                        }
                    )
                    continue

                # Handle Audio Output
                # Checking for audio parts in the event
                # Event structure varies, but usually follows google.genai.types.GenerateContentResponse
                # or similar ADK wrappers.
                # We check for `parts` or `audio`.

                parts = getattr(event, "parts", []) or []
                # Also check direct attributes if event is a chunk
                if hasattr(event, "audio") and event.audio:
                     # It might be a ModelResponse with audio
                     # Treat event as part-like if it has audio directly
                     parts = [event]

                for part in parts:
                    data = None
                    if hasattr(part, "inline_data") and part.inline_data:
                         data = part.inline_data.data
                    elif hasattr(part, "audio") and part.audio:
                         # Check if part.audio is bytes or Blob
                         if hasattr(part.audio, "data"):
                             data = part.audio.data
                         elif isinstance(part.audio, (bytes, bytearray)):
                             data = part.audio

                    if data:
                        await self._adapter.send_audio_chunk(data)

        except Exception as e:
            logger.error(f"Error in run_live loop: {e}")
            raise
