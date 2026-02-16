from pydantic import BaseModel, Field
from typing import List, Optional, Any

class TopicNode(BaseModel):
    id: str = Field(..., description="Unique identifier for the node")
    label: str = Field(..., description="Short label for the topic")
    content: str = Field(..., description="Detailed content or key facts for this topic")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional metadata")

class TopicGraph(BaseModel):
    nodes: List[TopicNode] = Field(..., description="List of topic nodes")
    edges: List[Any] = Field(default_factory=list, description="Connections between nodes (optional for now)")
    current_node_id: Optional[str] = Field(None, description="The ID of the currently active topic")

class HostPersona(BaseModel):
    id: str = Field(..., description="Unique identifier for the host")
    name: str = Field(..., description="Name of the host")
    voice_id: str = Field(..., description="Voice ID for TTS")
    system_prompt: str = Field(..., description="System prompt defining personality")
    interruption_sensitivity: float = Field(0.5, ge=0.0, le=1.0, description="Sensitivity to interruptions (0-1)")
