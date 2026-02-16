import os
import json
import asyncio
import logging
import random
from typing import Optional
from google import genai
from google.genai import types

from ...core.domain import HostPersona, TopicGraph
from ...core.interfaces import StateStore
from ...agents.base import BaseAgent
from ...infrastructure.redis_store import RedisStateStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversalHostAgent(BaseAgent):
    persona_id: str
    model_name: str
    persona: Optional[HostPersona] = None

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

        # Initialize GenAI Client
        # Expects GOOGLE_API_KEY in env
        self._client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

        # Load Persona
        self._load_persona()

    def _load_persona(self):
        """Loads the persona JSON file."""
        try:
            # Assuming personas are stored in src/personas/
            # We need to find the absolute path or relative path
            # For now, let's assume the CWD is the project root
            persona_path = f"src/personas/{self.persona_id}.json"
            if not os.path.exists(persona_path):
                 # Fallback for Docker structure if needed, or raise error
                 logger.error(f"Persona file not found: {persona_path}")
                 return

            with open(persona_path, "r") as f:
                data = json.load(f)
                self.persona = HostPersona(**data)

            logger.info(f"Loaded persona: {self.persona.name} ({self.persona.id})")
        except Exception as e:
            logger.error(f"Failed to load persona {self.persona_id}: {e}")
            raise

    async def _generate_dialogue(self, node_content: str, context: str) -> str:
        """Generates dialogue using Gemini."""
        if not self.persona:
            return "..."

        system_instruction = f"""
You are {self.persona.name}, a podcast host.
Your personality: {self.persona.system_prompt}
Voice Settings: {self.persona.voice_settings}
Interaction Rules: {self.persona.interaction_rules}

Current Topic: {context}
Key Facts: {node_content}

Task: Generate 2-3 sentences of natural, improvised dialogue for a podcast.
Do not include stage directions. Just the spoken text.
"""
        try:
            # Use the synchronous client in an async wrapper or just assume it's fast enough?
            # google-genai v1.0+ has an async client usually, but let's check standard usage.
            # The 'google.genai' library has an async client?
            # For now, we'll wrap the sync call if needed, or use client.aio if available.
            # Checking documentation implies client.models.generate_content is sync.
            # Let's use asyncio.to_thread to avoid blocking the loop.

            response = await asyncio.to_thread(
                self._client.models.generate_content,
                model=self.model_name,
                contents=system_instruction,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=150,
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return "..."

    async def run_loop(self):
        """
        The main execution loop.
        State A: Idle (Wait for EPISODE_READY)
        State B: Active (Talking Stick Cycle)
        """
        logger.info(f"Agent {self.name} starting run_loop...")

        pubsub = await self.state_store.subscribe_to_channel("EPISODE_READY")

        while True:
            # STATE A: IDLE
            logger.info("State A: Idle. Waiting for EPISODE_READY...")
            async for message in pubsub.listen():
                if message["type"] == "message":
                    logger.info("Received EPISODE_READY. Switching to State B: Active.")
                    break # Exit listener, enter active loop

            # STATE B: ACTIVE
            active = True
            while active:
                # Check for session end (this logic depends on how 'is_outro' or 'session_end' is signaled)
                # For now, we'll check the TopicGraph
                graph = await self.state_store.get_topic_graph()
                if not graph:
                    logger.warning("No TopicGraph found. Returning to Idle.")
                    active = False
                    break

                # Check if we are done (e.g., last node and processed)
                # For this implementation, we assume the graph has a state or we get a signal.
                # The user said: "After the TopicGraph is exhausted (the agent sees the is_outro flag or a session_end signal)"
                # Let's assume TopicNode has 'is_outro' in metadata or similar, or we check current_node_id.

                current_node = next((n for n in graph.nodes if n.id == graph.current_node_id), None)
                if not current_node:
                    # If no current node is set, maybe we start at the first one?
                    # Or we wait.
                    await asyncio.sleep(1)
                    continue

                if current_node.metadata.get("is_outro", False):
                    # We might want to say one last thing, then stop.
                    # For now, let's just break if we've "finished".
                    # Real logic: The Producer moves the graph. We just talk about the current node.
                    # If the session is explicitly ended, we break.
                    pass

                # Attempt to acquire talking stick
                acquired = await self.state_store.acquire_talking_stick(self.name, timeout=5)

                if acquired:
                    logger.info(f"{self.name} acquired talking stick.")
                    try:
                        # Fetch context
                        dialogue = await self._generate_dialogue(
                            node_content=current_node.content,
                            context=current_node.label
                        )

                        # Publish to Stream
                        payload = {
                            "agent_id": self.name,
                            "text": dialogue,
                            "timestamp": str(asyncio.get_event_loop().time()), # Use proper timestamp in real app
                            "node_id": current_node.id
                        }

                        # Add to Redis Stream
                        msg_id = await self.state_store.add_to_stream("conversation_stream", payload)

                        # Log to stdout
                        logger.info(f"Generated: {dialogue}")
                        print(f"[{self.name}]: {dialogue}") # Explicit stdout for Docker logs

                        # Simulate speaking time (or just hold lock for a moment?)
                        # User: "prevent... interrupting each other... natural passing"
                        # We release immediately after "speaking" (publishing).

                    except Exception as e:
                        logger.error(f"Error during turn: {e}")
                    finally:
                        await self.state_store.release_talking_stick(self.name)
                        # Backoff to let others speak
                        await asyncio.sleep(random.uniform(1.0, 2.0))
                else:
                    # Stick not acquired, wait and retry
                    await asyncio.sleep(0.5)

                # Check for session end signal via Redis?
                # For simplicity, we loop until the graph is cleared or a specific event.
                # We'll just loop forever in Active state for now until "EPISODE_END" (not yet defined) or just keep going.
                # The user said: "After the TopicGraph is exhausted... transition back to State A".
                # We'll implement a check: if current_node is None or is_outro.
                if current_node and current_node.metadata.get("is_outro") and False: # Disable auto-exit for now to keep it simple
                     active = False
