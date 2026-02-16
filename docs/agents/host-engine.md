# Host Engine (Universal Host)

The Host Engine is the "Body" and "Mouth" of the system. It is a generic execution environment that, when combined with a "Soul" (Persona), becomes a specific podcast host.

## Core Components

### 1. The Engine (`src/agents/universal_host/engine.py`)
*   **Loop:** The main event loop that drives the agent.
*   **State Machine:** Manages transitions between `Listening`, `Thinking`, and `Speaking`.
*   **Persona Loading:** Reads `src/personas/*.json` to configure the LLM's system prompt and voice.

### 2. LiveKit Adapter (`src/infrastructure/livekit_adapter.py`)
*   **WebRTC Interface:** Handles real-time audio I/O.
*   **VAD (Voice Activity Detection):** Uses `silero` to detect when a user (or another agent) starts speaking.
*   **Gating:** Instantly drops outgoing audio packets when speech is detected to prevent "talking over".

### 3. Google ADK Integration
*   The Host Agent inherits from `google.adk.agents.LlmAgent`.
*   It uses `runner.run_live()` to manage the bi-directional stream with Gemini.
*   **Interruption Handling:** Responds to `interrupted` events from the ADK by performing a "Cognitive Rewind".

## The Run Loop

1.  **Wait for Signal:** The agent idles until it receives `EPISODE_READY` or acquires the "Talking Stick".
2.  **Context Assembly:**
    *   Retrieves the current `TopicNode` from Redis.
    *   Retrieves the last few turns of conversation history.
    *   Injects the Persona's system prompt.
3.  **Generation:**
    *   Sends the context to Gemini 3.0 via the ADK.
    *   Receives audio chunks in real-time.
4.  **Streaming:**
    *   Passes audio chunks to the `LiveKitAdapter`.
    *   Adapter plays them into the room.
5.  **Yielding:**
    *   Once the turn is complete, the agent releases the "Talking Stick" in Redis.

## Interruption Logic

See `docs/architecture/interruption-handling.md` for the detailed state transition diagram.
