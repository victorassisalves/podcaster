# Producer Agent

The Producer Agent is the "Brain" of the operation. It is responsible for researching topics, structuring the episode, and providing the "script" (in graph form) for the Host Agents to follow.

## Role & Responsibilities

*   **Deep Research:** Uses Gemini 2.0 (Deep Research) to gather facts, news, and context about a given subject.
*   **Graph Synthesis:** Converts unstructured research into a structured `TopicGraph`.
*   **Orchestration:** Publishes the `EPISODE_READY` signal to start the show.

## Workflow

1.  **Input:** User provides a topic (e.g., "The Future of AI Agents").
2.  **Research Phase:**
    *   The agent uses MCP tools (e.g., Google Search) to find relevant articles.
    *   It synthesizes key points, counter-arguments, and quotes.
3.  **Graph Generation:**
    *   It structures the findings into a DAG (Directed Acyclic Graph).
    *   **Nodes:** Represent sub-topics or specific talking points.
    *   **Edges:** Represent logical transitions.
4.  **Publication:**
    *   The `TopicGraph` is serialized to JSON and saved to Redis.
    *   A message is published to the `EPISODE_READY` channel.

## Configuration

*   **Model:** `gemini-2.0-pro-exp` (High reasoning capacity).
*   **Tools:**
    *   `google_search_tool`: For real-time information.
    *   `knowledge_base_tool`: For accessing internal docs.

## Implementation Details

The Producer Agent logic resides in `src/agents/producer/`. It leverages LangChain or LangGraph to manage the multi-step research process.
