# Docker Development Guide

This guide explains how to run the entire Podcaster 360 stack using Docker Compose. This is the recommended method for simulating the full production environment locally.

## Architecture in Docker

The `docker-compose.yml` orchestrates the following services:
1.  **`backend`**: The FastAPI server.
2.  **`frontend`**: The Next.js dashboard.
3.  **`redis`**: Message broker for Pub/Sub and State Store.
4.  **`agent-host`**: A containerized instance of the `UniversalHostAgent`.
5.  **`agent-producer`**: A containerized instance of the `ProducerAgent`.

## Quick Start

1.  **Configuration:**
    Ensure your `.env` file is populated (see `local-dev.md`).

2.  **Build & Run:**
    ```bash
    docker-compose up --build
    ```

3.  **Access:**
    *   **Backend API:** `http://localhost:8000`
    *   **Frontend:** `http://localhost:3000`
    *   **Redis Commander (Optional):** If included, `http://localhost:8081`

## Troubleshooting

### "Port already in use"
If you see errors about ports 3000, 8000, or 6379 being occupied:
```bash
# Find what's using the port
lsof -i :8000
# Kill the process
kill -9 <PID>
```
Or, simply stop all docker containers:
```bash
docker stop $(docker ps -a -q)
```

### Dependency Issues
If you encounter `ModuleNotFoundError` inside a container, you may need to rebuild without cache:
```bash
docker-compose build --no-cache
```

### Networking
*   **Host Networking:** On Linux, you can add `network_mode: host` to `docker-compose.yml` for better network performance with WebRTC.
*   **DNS:** Services communicate via service names (e.g., `redis:6379`). Do not use `localhost` inside containers to refer to other services; use the service name.
