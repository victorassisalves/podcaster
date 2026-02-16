from google.adk.agents import LlmAgent
from typing import Optional, Any
from pydantic import Field, ConfigDict
from ..core.interfaces import StateStore

class BaseAgent(LlmAgent):
    """
    Base class for all agents in the Podcaster swarm.
    Inherits from Google ADK's LlmAgent for intelligent loop management.
    Injects shared infrastructure (StateStore).
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    state_store: Optional[StateStore] = Field(default=None, description="Shared state store")

    def __init__(
        self,
        name: str,
        state_store: Optional[StateStore] = None,
        **kwargs
    ):
        # Pass state_store to the Pydantic model initialization
        super().__init__(name=name, state_store=state_store, **kwargs)

    def set_state_store(self, state_store: StateStore):
        self.state_store = state_store
