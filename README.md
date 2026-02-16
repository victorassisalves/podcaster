# Podcaster 360

A multi-agent live podcast platform hosted on GCP.

## Overview
Podcaster 360 is a "Hybrid Agentic Swarm" where autonomous AI agents research topics, plan episodes, and improvise dialogue in real-time. It moves beyond static text-to-speech scripts to dynamic, interruptible conversations.

## Documentation

We have moved our documentation to the `docs/` directory for better organization.

### 🏗 Architecture
*   [Swarm Logic & Pub/Sub](docs/architecture/swarm-logic.md)
*   [Shell & Soul Pattern](docs/architecture/shell-and-soul.md)
*   [Hexagonal Architecture](docs/architecture/hexagonal.md)
*   [Interruption Handling](docs/architecture/interruption-handling.md)
*   [A2A Manifests](docs/architecture/a2a-manifests.md)
*   [Failure Modes](docs/architecture/failure-modes.md)

### 🚀 Setup
*   [Local Development Guide](docs/setup/local-dev.md) (Prerequisites, LiveKit CLI, Python)
*   [Docker Guide](docs/setup/docker-guide.md) (Compose, Troubleshooting)

### ☁️ Deployment
*   [GCP Cloud Run](docs/deployment/gcp-cloud-run.md)
*   [Local Production Simulation](docs/deployment/local-prod-sim.md)

### 🤖 Agents
*   [Producer Agent](docs/agents/producer.md) (The "Brain")
*   [Host Engine](docs/agents/host-engine.md) (The "Body")

## Quick Start (Local Docker)

1.  **Clone & Configure:**
    ```bash
    cp .env.example .env
    # Fill in API keys
    ```

2.  **Run:**
    ```bash
    docker-compose up --build
    ```

3.  **Access:**
    *   **Frontend:** http://localhost:3000
    *   **Backend:** http://localhost:8000

See [docs/setup/docker-guide.md](docs/setup/docker-guide.md) for details.
