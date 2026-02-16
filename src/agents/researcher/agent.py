from ..base import BaseAgent
from ...core.domain import ResearchSummary
from .tools import google_search
from typing import Optional, Dict, Any
import json

class ResearchAgent(BaseAgent):
    """
    Agent responsible for researching a topic using MCP-style tools.
    """
    def __init__(self, model: str = "gemini-3.0-pro", **kwargs):
        system_prompt = """
        You are an expert Research Analyst.
        Your goal is to thoroughly research a given topic and provide a structured summary.
        You have access to a 'google_search' tool. Use it to find latest information.
        Focus on finding:
        1. Key facts and consensus.
        2. Conflicting viewpoints or controversies (crucial for a good debate).
        3. Reliable primary sources.

        Your final output MUST be a valid JSON object matching the ResearchSummary schema:
        {
            "key_facts": ["fact1", "fact2"],
            "conflicting_views": ["view1", "view2"],
            "primary_sources": ["url1", "url2"]
        }
        """

        super().__init__(
            name="researcher",
            model=model,
            tools=[google_search],
            instruction=system_prompt,
            **kwargs
        )

    # We might need a method to specifically return the Pydantic object
    # But for now, we rely on the agent loop returning the final text/json.
