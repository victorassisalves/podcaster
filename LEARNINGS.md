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
