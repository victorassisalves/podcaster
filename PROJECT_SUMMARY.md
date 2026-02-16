# Project Roadmap & Execution Plan

## Executive Summary
We are building a "Hybrid Agentic Swarm" for autonomous podcasting. The goal is to move from a scripted sequence to a dynamic, real-time conversation between AI agents that can be interrupted by a human user.

## The Scalability Strategy
To support user-created agents in the future, we are adopting the **"Shell & Soul" architecture**.
* **Scalability:** We can spawn 100 different hosts using the same Docker image, just by injecting different JSON configs.
* **Modularity:** The "Thinking" (Producer) is decoupled from the "Speaking" (Host) via Redis.

## Master Prompt List
Use these prompts to guide Jules through the development phases.

### Prompt 1: Phase 1 (Foundation)
> "Jules, we are building 'Podcaster 360' using a **Hexagonal Architecture**.
> 1. **Structure:** Create the folder structure `src/core`, `src/infrastructure`, and `src/agents`.
> 2. **Domain:** In `src/core/domain.py`, define Pydantic models for `TopicGraph` (list of nodes) and `HostPersona` (name, voice_id, system_prompt).
> 3. **Interfaces:** In `src/core/interfaces.py`, define an abstract `StateStore` class with methods for `acquire_talking_stick(agent_id)` and `get_topic_graph()`.
> 4. **Infrastructure:** Implement `src/infrastructure/redis_store.py` using `redis-py` to fulfill the `StateStore` interface."

### Prompt 2: Phase 2 (The Brain)
> "Create the **Producer Agent** in `src/agents/producer/`.
> * It should use `gemini-2.0-pro-exp`.
> * It needs an MCP tool for research (mock it for now).
> * **Logic:** Take a topic -> Generate a 5-node `TopicGraph` JSON -> Save it to Redis using the `StateStore` interface."

### Prompt 3: Phase 3 (The Body)
> "Build the **Universal Host Agent** in `src/agents/universal_host/`.
> 1. **The Engine:** Create `engine.py` with a class `HostEngine`. It accepts a `HostPersona` and `StateStore`.
> 2. **The Loop:** Implement `run_loop()`: Check Redis for `TopicNode` -> Acquire Stick -> Generate text using persona's prompt.
> 3. **The Entry Point:** Create `main.py` that reads `PERSONA_JSON` from Env Vars, parses it, and launches the engine."

### Prompt 4: Phase 3.5 (The Ears)
> "Integrate **LiveKit** into the Host Engine.
> * Create `src/infrastructure/livekit_adapter.py`.
> * Implement connecting to a room and streaming audio.
> * Connect the `HostEngine` output to this adapter."
