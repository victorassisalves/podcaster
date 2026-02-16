from pydantic import BaseModel, Field
from typing import List, Optional, Any

class TopicNode(BaseModel):
    id: str = Field(..., description="Unique identifier for the node")
    label: str = Field(..., description="Short label for the topic")
    content: str = Field(..., description="Detailed content or key facts for this topic")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional metadata")

class TopicEdge(BaseModel):
    source_id: str = Field(..., description="ID of the source node")
    target_id: str = Field(..., description="ID of the target node")
    condition: Optional[str] = Field(None, description="Condition for traversing this edge (e.g., 'sentiment == skeptical')")

class TopicGraph(BaseModel):
    nodes: List[TopicNode] = Field(..., description="List of topic nodes")
    edges: List[TopicEdge] = Field(default_factory=list, description="Connections between nodes")
    current_node_id: Optional[str] = Field(None, description="The ID of the currently active topic")

class ResearchSummary(BaseModel):
    key_facts: List[str] = Field(..., description="List of key facts extracted from research")
    conflicting_views: List[str] = Field(..., description="Points of disagreement or conflict")
    primary_sources: List[str] = Field(..., description="URLs or names of primary sources")

class HostPersona(BaseModel):
    id: str = Field(..., description="Unique identifier for the host")
    name: str = Field(..., description="Name of the host")
    voice_id: str = Field(..., description="Voice ID for TTS")
    system_prompt: str = Field(..., description="System prompt defining personality")
    interruption_sensitivity: float = Field(0.5, ge=0.0, le=1.0, description="Sensitivity to interruptions (0-1)")
