# A2A Discovery & Manifests

To enable seamless discovery and interaction between agents in the Google ADK ecosystem, each agent must expose a standardized manifest.

## The Agent Card (`agent.json`)

Every agent service must serve a JSON manifest at `/.well-known/agent.json`. This file describes the agent's identity, capabilities, and connection endpoints.

### Schema Structure

```json
{
  "kind": "Agent",
  "apiVersion": "a2a.googleapis.com/v1alpha1",
  "metadata": {
    "name": "host-agent-sascha",
    "displayName": "Sascha (Host)",
    "description": "A skeptical tech journalist host for Podcaster 360.",
    "version": "1.0.0",
    "labels": {
      "role": "host",
      "persona": "skeptic"
    }
  },
  "spec": {
    "capabilities": [
      {
        "type": "conversation",
        "modalities": ["AUDIO", "TEXT"]
      }
    ],
    "endpoints": [
      {
        "name": "livekit-stream",
        "protocol": "livekit",
        "url": "${LIVEKIT_URL}",
        "authType": "token"
      }
    ]
  }
}
```

## Field Definitions

*   **`metadata.name`**: Unique identifier for the agent instance.
*   **`metadata.labels`**: Key-value pairs used for discovery (e.g., finding all agents with `role=host`).
*   **`spec.capabilities`**:
    *   `type`: The primary function (e.g., `conversation`, `search`, `planning`).
    *   `modalities`: Supported I/O formats.
*   **`spec.endpoints`**: Connection details.
    *   `protocol`: `livekit`, `http`, `grpc`, etc.
    *   `url`: The entry point URL.

## Implementation Guide

In `src/agents/base.py`, the `BaseAgent` should ideally implement a method to generate this structure based on its configuration, or the FastAPI wrapper should serve this static file.

### Serving with FastAPI

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/.well-known/agent.json")
async def get_agent_manifest():
    return JSONResponse(content={
        "kind": "Agent",
        "metadata": { ... },
        ...
    })
```
