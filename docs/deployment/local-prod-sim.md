# Local Production Simulation

Before deploying to the cloud, it is critical to verify the system behavior in a "production-like" local environment. This means running the full swarm with multiple agents, distinct services, and network constraints.

## Goal
Simulate a live episode with:
1.  One Producer Agent.
2.  Two Host Agents (e.g., "Sascha" and "Kai").
3.  A Redis instance.
4.  A local LiveKit server (or connection to LiveKit Cloud).

## Step-by-Step

### 1. The `docker-compose.prod.yml`
Create a `docker-compose.prod.yml` (or extend the default one) to spawn multiple agent containers.

```yaml
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  producer:
    build:
      context: .
      dockerfile: Dockerfile
    command: python -m src.agents.producer.main
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis

  host-sascha:
    build:
      context: .
      dockerfile: Dockerfile
    command: python -m src.agents.universal_host.main
    environment:
      - PERSONA_ID=host_sascha
      - REDIS_URL=redis://redis:6379
      - LIVEKIT_URL=${LIVEKIT_URL}
    depends_on:
      - redis

  host-kai:
    build:
      context: .
      dockerfile: Dockerfile
    command: python -m src.agents.universal_host.main
    environment:
      - PERSONA_ID=host_kai
      - REDIS_URL=redis://redis:6379
      - LIVEKIT_URL=${LIVEKIT_URL}
    depends_on:
      - redis
```

### 2. Execution
Run the simulation:
```bash
docker-compose -f docker-compose.prod.yml up --build
```

### 3. Verification Points
*   **Logs:** Check `docker-compose logs -f` to see if both hosts connect to Redis and LiveKit.
*   **Redis:** Use `redis-cli monitor` to watch the message flow.
    *   Do you see `EPISODE_READY` published by the producer?
    *   Do you see `talking_stick` keys being set and deleted?
*   **LiveKit:** Use the CLI or Dashboard to verify both agents are in the room and subscribing to each other.

### 4. Stress Testing (Optional)
To test robustness, manually kill one of the host containers:
```bash
docker kill <container_id_host_sascha>
```
Observe if the other host ("Kai") takes over or if the system hangs. This tests the "Failure Modes" logic.
