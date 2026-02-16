from ..base import BaseAgent
from ..researcher.agent import ResearchAgent
from ...core.domain import TopicGraph
import json
import asyncio
from typing import Dict, Any

class ProducerAgent(BaseAgent):
    """
    The Executive Director agent.
    Orchestrates research and planning.
    """
    def __init__(self, state_store, model: str = "gemini-3.0-pro", **kwargs):
        super().__init__(
            name="producer",
            state_store=state_store,
            model=model,
            instruction="""
            You are the Executive Producer of a podcast.
            Your goal is to plan a new episode based on a user-provided topic.

            WORKFLOW:
            1.  **Analyze the Request**: Understand the user's topic.
            2.  **Conduct Research**: Call the 'perform_research' tool to get a summary of key facts and controversies.
            3.  **Synthesize Plan**: Create a 'TopicGraph' JSON structure.
                - It must have at least 5 nodes.
                - Use 'TopicEdge' to connect them.
                - Include Conditional Edges (e.g., condition="sentiment == skeptical") to allow for non-linear flow.
                - The 'content' of each node should be detailed script guidance for the hosts.
            4.  **Publish**: Call the 'finalize_episode' tool with the complete JSON.

            The TopicGraph schema is:
            {
              "nodes": [{"id": "...", "label": "...", "content": "..."}],
              "edges": [{"source_id": "...", "target_id": "...", "condition": "..."}],
              "current_node_id": "..."
            }
            """,
            tools=[self.perform_research, self.finalize_episode],
            **kwargs
        )

    def perform_research(self, topic: str) -> str:
        """
        Conducts research on a topic using the Research Agent.
        Returns a summary string.
        """
        # In a real async environment, we'd await this.
        # But if this tool is called synchronously by the runner, we might need a workaround.
        # For now, let's assume we can run the researcher synchronously or the runner handles coroutines.
        # We'll try to run the researcher in a new loop if needed, or just call its logic.

        print(f"[Producer] Delegating research for: {topic}")
        researcher = ResearchAgent()

        # Mocking the interaction for now since we don't have the full async runner context setup
        # In production, this would be: summary = await researcher.run(topic)
        # Here we manually invoke the tool and format the result to simulate the agent's work.
        from ..researcher.tools import google_search
        results = google_search(topic)

        # Simple synthesis (mocking the Researcher's LLM step to avoid nesting complexity in this phase)
        summary = {
            "key_facts": [r['snippet'] for r in results],
            "conflicting_views": ["Some sources disagree on the timeline."],
            "primary_sources": [r['url'] for r in results]
        }
        return json.dumps(summary)

    def finalize_episode(self, graph_json: Dict[str, Any]) -> str:
        """
        Validates the TopicGraph and publishes the episode.
        Args:
            graph_json: The dictionary representing the TopicGraph.
        """
        print(f"[Producer] Finalizing episode...")
        try:
            # Validate
            graph = TopicGraph.model_validate(graph_json)

            # Save to State Store
            # We need to run async methods. If this tool is sync, we use a helper.
            # Assuming we can use asyncio.run or similar if not in a loop, but we likely are.
            # A safe way in a tool is to return a special signal or try to schedule.
            # But let's try to use the event loop.

            async def _save():
                await self.state_store.set_topic_graph(graph)
                await self.state_store.publish_event("EPISODE_READY", {"initial_node": graph.nodes[0].id})
                print(f"[Producer] Episode published: {graph.nodes[0].label}")

            # If there's a running loop, create a task.
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(_save())
            except RuntimeError:
                asyncio.run(_save())

            return "Episode successfully planned and published."

        except Exception as e:
            return f"Error validating graph: {str(e)}"
