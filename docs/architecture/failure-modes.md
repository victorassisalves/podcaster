# System Failure Modes & Recovery

In a distributed swarm architecture, components can fail independently. This document outlines the expected failure modes and the system's recovery strategies.

## 1. Redis Unavailability

**Scenario:** The Redis instance goes down or becomes unreachable.

*   **Impact:**
    *   `StateStore` operations fail.
    *   "Talking Stick" cannot be acquired/released.
    *   Pub/Sub messages (`EPISODE_READY`) are lost.
*   **Behavior:**
    *   Agents will raise `ConnectionError`.
    *   **Recovery:**
        *   Implement a **Circuit Breaker** in `RedisStateStore`.
        *   Agents should retry with exponential backoff.
        *   If Redis is down for > 30s, agents should enter a `SafeMode` (e.g., generic fallback response or silence) and alert the dashboard.

## 2. Agent Timeout (The "Hogging" Problem)

**Scenario:** An agent acquires the "Talking Stick" but crashes or hangs before releasing it.

*   **Impact:** The conversation stalls. No other agent can speak.
*   **Behavior:**
    *   The `talking_stick` key in Redis remains locked indefinitely.
*   **Recovery:**
    *   **TTL (Time-To-Live):** The `talking_stick` key must have a specialized TTL (e.g., 15 seconds).
    *   **Watchdog:** A separate "Director" process (or the Producer) monitors the stream. If silence > 10s, it forcibly resets the stick.

## 3. Gemini API Rate Limits

**Scenario:** The Google Gemini API returns a `429 Too Many Requests`.

*   **Impact:** Host agent cannot generate text/audio.
*   **Behavior:**
    *   Agent throws an exception during generation.
*   **Recovery:**
    *   **Backoff:** Implement exponential backoff for API calls.
    *   **Fallback:**
        *   Switch to a lower-tier model (e.g., `gemini-1.5-flash` instead of `pro`).
        *   Play a pre-recorded "filler" audio (e.g., "Hmm, let me think about that," or "Hold on a second.") while retrying.

## 4. LiveKit Disconnection

**Scenario:** The WebRTC connection to LiveKit is lost.

*   **Impact:** Audio stops streaming. Agent is "deaf" and "mute".
*   **Behavior:**
    *   `LiveKitAdapter` emits a `disconnected` event.
*   **Recovery:**
    *   **Auto-Reconnect:** The adapter should attempt to reconnect automatically.
    *   **State Reset:** Upon reconnection, the agent should query Redis to check the current conversation state and avoid interrupting if someone else started speaking.
