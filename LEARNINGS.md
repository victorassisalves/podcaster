# Learnings from Podcaster AI Implementation

## Gemini Deep Research API
- The `deep-research-pro-preview-12-2025` model requires the **Interactions API** (`client.interactions.create`).
- It is a stateful interaction that can take significant time (minutes) to complete.
- Results are found in the `outputs` attribute of the interaction object.

## LiveKit Agents with Gemini Live
- Use `google.realtime.RealtimeModel` for the Gemini Live API.
- The `AgentSession` in `livekit-agents` 1.4+ simplifies the orchestration of LLM, TTS, and VAD.
- Separate TTS can be used with native audio models by setting modalities to `[TEXT]`.

## GCP Infrastructure for Live Media
- **Cloud Run** is excellent for stateless APIs and the Next.js frontend.
- **Compute Engine** is preferred for the LiveKit server POC to ensure consistent network performance for WebRTC.
- **Firestore** provides a lightweight way to manage agent profiles and episode state.
- **Pydantic Inheritance:** When inheriting from a Pydantic model (like  -> ), new fields must be declared as type hints in the subclass to be recognized as fields. Passing them to  works if they are valid fields on the parent or subclass.
- **Redis Streams:** Use  for adding to streams. It returns the message ID.
- **Async GenAI Client:** The  library's  methods like  are synchronous by default and should be run in a thread executor () to avoid blocking the asyncio event loop.
- **A2A Discovery:**  requires an  with specific fields.  is required but can be empty.
- **Pydantic Inheritance:** When inheriting from a Pydantic model (like `BaseAgent` -> `LlmAgent`), new fields must be declared as type hints in the subclass to be recognized as fields. Passing them to `super().__init__` works if they are valid fields on the parent or subclass.
- **Redis Streams:** Use `xadd` for adding to streams. It returns the message ID.
- **Async GenAI Client:** The `google-genai` library's `Client` methods like `generate_content` are synchronous by default and should be run in a thread executor (`asyncio.to_thread`) to avoid blocking the asyncio event loop.
- **A2A Discovery:** `to_a2a` requires an `AgentCard` with specific fields. `AgentCapabilities` is required but can be empty.
