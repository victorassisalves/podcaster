# Project Context: Podcaster 360 (v3.0)

> **For the AI Developer (Jules):** This document serves as the Source of Truth for the Podcaster 360 architecture. Please strictly adhere to the Hexagonal Architecture patterns defined here.

## 1. Project Vision
Podcaster 360 is an autonomous, multi-agent audio swarm. Unlike linear text-to-speech readers, it uses a team of decentralized AI agents to research topics, plan episodes, and improvise dialogue in real-time via WebRTC (LiveKit).

## 2. Architectural Pattern: Hexagonal (Ports & Adapters)
To ensure modularity and prevent vendor lock-in, we use a strict Hexagonal Architecture.

### Directory Structure & Rules
* **`src/core/` (The Inner Hexagon)**
    * **Rule:** NO external infrastructure imports allowed here (No `livekit`, `redis`, or `google-genai`).
    * **Content:** Pure Python data models (Pydantic), Abstract Base Classes (Interfaces), and business logic.
    * `src/core/domain.py`: Entities like `TopicGraph`, `TopicNode`, `HostPersona`.
    * `src/core/interfaces.py`: Abstract classes like `StateStore`, `AudioProvider`, `LlmProvider`.
* **`src/infrastructure/` (The Adapters)**
    * **Rule:** Implement the interfaces defined in `core`.
    * `src/infrastructure/redis_store.py`: Implements `StateStore`.
    * `src/infrastructure/livekit_adapter.py`: Implements `AudioProvider`.
* **`src/agents/` (The Application Layer)**
    * **Rule:** Orchestrates the logic using Interfaces.
    * `src/agents/producer/`: The "Brain" that generates the Topic Graph.
    * `src/agents/universal_host/`: The "Body" (Generic Engine) that drives the characters.
* **`src/personas/` (Configuration)**
    * **Rule:** JSON files only. Defines specific characters (e.g., "The Skeptic", "The Optimist").

---

## 3. Core Design Pattern: "Shell & Soul"
We do **NOT** create a new folder for every host agent. Instead, we use a single generic container ("The Shell") that loads a specific personality ("The Soul") at runtime.

### The Shell (`src/agents/universal_host/`)
* Contains the `HostEngine` class.
* Implements the loop: `Wait for Talking Stick` -> `Think` -> `Speak`.
* Does not know *who* it is until initialized.

### The Soul (`HostPersona` Model)
* Defined in `src/core/domain.py`.
* Loaded from JSON or Environment Variables at startup.
```json
{
  "id": "host_sascha",
  "name": "Sascha",
  "voice_id": "elevenlabs_id_123",
  "system_prompt": "You are a skeptical tech journalist...",
  "interruption_sensitivity": 0.8
}
```

## 4. Execution Phases
### Phase 1: Foundation (Infrastructure)
* Setup Docker Compose (Redis + Python).
* Define Pydantic models in `src/core/domain.py`.
* Define Interfaces in `src/core/interfaces.py`.
* Implement `RedisStateStore`.

### Phase 2: The Producer (The Brain)
* Build the ProducerAgent (Gemini 3.0 Pro).
* Implement MCP Tool for Google Search.
* Logic: Research Topic -> Generate TopicGraph -> Save to Redis.

### Phase 3: The Universal Host (The Body)
* Build HostEngine class in `src/agents/universal_host/`.
* Implement LiveKitAdapter in `src/infrastructure/`.
* Logic: Connect to Room -> Wait for 'Talking Stick' -> Generate Audio based on loaded Persona.

### Phase 4: Interruption Handling (The Ears)
* Integrate Silero VAD via LiveKit.
* Logic: If user speaks -> Interrupt Host -> Update Redis ([User Interrupted]).

### Phase 5: Visualization (The Face)
* Next.js 14 Dashboard.
* Read TopicGraph from Redis.
* Display active node and audio levels.

## 5. Coding Guidelines for Jules
* **Type Hinting:** Use Python type hints strictly.
* **Async/Await:** All I/O (Redis, LLM, WebRTC) must be asynchronous.
* **Error Handling:** Never let an agent crash the loop. Log errors and retry.
* **No Hardcoding:** Always refer to `src/personas/` or Env Vars for character data.
