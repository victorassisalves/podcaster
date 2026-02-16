# Shell & Soul Pattern

The **Shell & Soul** pattern is a core architectural design in Podcaster 360 that enables dynamic agent instantiation and scalability.

## Concept

Instead of creating a unique codebase or class for every character (e.g., "The Skeptic", "The Optimist"), we use a single, generic **Universal Host Agent** ("The Shell") that loads a specific personality configuration ("The Soul") at runtime.

## The Shell: `UniversalHostAgent`

The Shell is the execution environment. It is agnostic to *who* is speaking and focuses on *how* to speak and interact.

*   **Location:** `src/agents/universal_host/`
*   **Responsibilities:**
    *   **LiveKit Connection:** Managing WebRTC audio streams.
    *   **State Management:** Listening to Redis for the "Talking Stick".
    *   **Interruption Handling:** Processing VAD events and rewinding context.
    *   **LLM Interaction:** Sending prompts to the LLM and streaming responses.

## The Soul: `HostPersona`

The Soul is the data that gives the agent its identity. It is defined as a Pydantic model and serialized as JSON.

*   **Definition:** `src/core/domain.py` -> `HostPersona`
*   **Storage:** `src/personas/*.json` or Environment Variables.

### Schema
```json
{
  "id": "host_sascha",
  "name": "Sascha",
  "voice_id": "elevenlabs_id_123",
  "system_prompt": "You are a skeptical tech journalist...",
  "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.75
  },
  "interruption_sensitivity": 0.8
}
```

## Runtime Injection

1.  **Deployment:** The Docker container for `UniversalHostAgent` is started.
2.  **Configuration:** The container receives an environment variable `PERSONA_ID` (e.g., `host_sascha`).
3.  **Initialization:**
    *   The agent reads `src/personas/host_sascha.json`.
    *   It hydrates the `HostPersona` object.
    *   It configures the LLM system prompt and TTS voice accordingly.

## Advantages

*   **Scalability:** Deploy 100 agents by simply orchestrating 100 containers with different env vars.
*   **Maintainability:** Fix a bug in `UniversalHostAgent`, and it applies to all characters.
*   **Flexibility:** Create new characters by adding a JSON file, without touching code.
