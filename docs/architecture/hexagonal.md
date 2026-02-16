# Hexagonal Architecture (Ports & Adapters)

Podcaster 360 adheres to a strict **Hexagonal Architecture** to ensure modularity, testability, and independence from external frameworks.

## Directory Structure & Rules

The codebase is organized into three concentric layers:

### 1. The Inner Hexagon: `src/core/`
This layer contains the business logic and domain entities. It must **NOT** depend on any external infrastructure (no `livekit`, `redis`, or `google-genai` imports).

*   **`src/core/domain.py`**:
    *   **Entities:** Pure Python classes or Pydantic models (e.g., `TopicGraph`, `TopicNode`, `HostPersona`).
    *   **Value Objects:** Immutable data structures.
*   **`src/core/interfaces.py`**:
    *   **Ports:** Abstract Base Classes (ABCs) defining the interfaces for external dependencies (e.g., `StateStore`, `AudioProvider`, `LlmProvider`).

### 2. The Adapters: `src/infrastructure/`
This layer implements the interfaces defined in the Core. It acts as the bridge between the application and the external world.

*   **`src/infrastructure/redis_store.py`**:
    *   Implements `StateStore` using `redis-py`.
*   **`src/infrastructure/livekit_adapter.py`**:
    *   Implements `AudioProvider` using the `livekit` SDK.
*   **`src/infrastructure/gemini_adapter.py`** (if applicable):
    *   Implements `LlmProvider` using `google-genai`.

### 3. The Application Layer: `src/agents/`
This layer orchestrates the logic using the Interfaces. It connects the "Ports" to the "Adapters".

*   **`src/agents/producer/`**:
    *   The "Brain". Uses `LlmProvider` to research and generate content.
*   **`src/agents/universal_host/`**:
    *   The "Body". Uses `AudioProvider` and `StateStore` to conduct the podcast.

## dependency Rule

Dependencies must always point **inwards**.
*   `infrastructure` depends on `core`.
*   `agents` depends on `core`.
*   `core` depends on **nothing**.

## Benefits

*   **Testability:** We can easily mock `StateStore` or `AudioProvider` to test agent logic without running Redis or LiveKit.
*   **Flexibility:** Switching from Redis to Firestore or LiveKit to Agora requires only writing a new Adapter, without changing the Core domain logic.
