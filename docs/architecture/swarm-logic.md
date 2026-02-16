# Swarm Logic & Architecture

## Philosophy: Swarm vs. Monolith

In traditional podcast generation systems, a single script is generated and then read by text-to-speech engines. Podcaster 360 adopts a **"Hybrid Agentic Swarm"** approach.

### Key Differences
- **Decentralized Control:** No single "master script". Agents react to each other and external events in real-time.
- **Dynamic Conversation:** Dialogue is improvised based on persona constraints and the current topic node, allowing for natural flow and interruptions.
- **Scalability:** The system can support an arbitrary number of hosts and producers without linear complexity growth.

## The Pub/Sub Flow

Communication between agents and the system is managed via **Redis** using a Pub/Sub model and Streams.

### Core Channels & Streams
1.  **`EPISODE_READY` (Channel):**
    -   **Publisher:** Producer Agent.
    -   **Subscriber:** All Host Agents.
    -   **Payload:** Signal that the `TopicGraph` is ready in Redis.

2.  **`conversation_stream` (Stream):**
    -   **Publisher:** Host Agents, LiveKit Adapter (System Signals).
    -   **Subscriber:** All Host Agents, Frontend Dashboard.
    -   **Payload:**
        -   `type`: `SPEECH` | `SYSTEM_SIGNAL`
        -   `agent_id`: ID of the speaker.
        -   `content`: Transcript or signal data.
        -   `metadata`: Contextual info (e.g., interruption timestamps).

3.  **`state_store` (Key-Value):**
    -   **Usage:** Stores the shared `TopicGraph` and current `talking_stick` holder.
    -   **Access:** Atomic operations to prevent race conditions during turn-taking.

## "Shell & Soul" Architecture

To support user-created agents and infinite scalability, we use the **"Shell & Soul"** pattern.

### The Shell (Container)
-   **Generic Host Engine:** A standardized Docker container running the `UniversalHostAgent`.
-   **Capabilities:**
    -   Connects to LiveKit (WebRTC).
    -   Listens to Redis events.
    -   Manages the "Talking Stick" protocol.
    -   Handles interruptions (Cognitive Rewind).

### The Soul (Persona)
-   **Configuration:** A JSON payload injected at runtime.
-   **Attributes:**
    -   `name`: Display name.
    -   `voice_id`: TTS voice identifier (e.g., ElevenLabs, Google Journey).
    -   `system_prompt`: Behavioral instructions and personality traits.
    -   `interruption_sensitivity`: Threshold for yielding the floor.

### Benefits
1.  **Modularity:** The "Thinking" (Producer) is decoupled from the "Speaking" (Host).
2.  **Reusability:** We can spawn 100 different hosts using the same Docker image, just by injecting different JSON configs.
3.  **Hot-Swapping:** Personas can potentially be updated or swapped without restarting the underlying infrastructure.
