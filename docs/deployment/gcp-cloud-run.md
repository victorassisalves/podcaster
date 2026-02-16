# GCP Deployment Guide (Cloud Run)

This guide details how to deploy Podcaster 360 to Google Cloud Platform using Cloud Run for the application layer and Compute Engine for the LiveKit Server (Proof of Concept).

## Prerequisites
*   Google Cloud Project (with Billing enabled).
*   APIs Enabled:
    *   Cloud Run
    *   Artifact Registry
    *   Firestore (or Redis Enterprise if not self-hosting)
    *   Cloud Storage
    *   Vertex AI

## 1. LiveKit Server (Compute Engine)

For a cost-effective POC, we run LiveKit on a VM to ensure stable WebRTC performance.

1.  **Provision:** Create an `e2-medium` instance (Ubuntu 22.04 LTS).
2.  **Firewall:** Allow UDP ports `50000-60000`, TCP `443`, `80`, `7880` (API).
3.  **Setup:**
    SSH into the VM and use the official LiveKit Docker setup:
    ```bash
    curl -sSL https://get.livekit.io | bash
    ```
4.  **Note Key Details:**
    *   Public IP / Domain
    *   API Key
    *   API Secret

## 2. Backend & Agents (Cloud Run)

### Backend Service
1.  **Build Image:**
    ```bash
    gcloud auth configure-docker
    docker build -t gcr.io/[PROJECT_ID]/podcaster-backend ./backend
    docker push gcr.io/[PROJECT_ID]/podcaster-backend
    ```

2.  **Deploy:**
    ```bash
    gcloud run deploy podcaster-backend \
      --image gcr.io/[PROJECT_ID]/podcaster-backend \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --env-vars-file .env.yaml
    ```

### Host Agents
Agents can also run on Cloud Run, but require **Session Affinity** and extended **Request Timeout** (up to 60m) since they maintain WebSocket connections.

1.  **Build Image:**
    Reuse the backend image or build a dedicated agent image.
    ```bash
    docker build -f backend/Dockerfile.agent -t gcr.io/[PROJECT_ID]/podcaster-agent ./backend
    ```

2.  **Deploy:**
    ```bash
    gcloud run deploy podcaster-agent-host \
      --image gcr.io/[PROJECT_ID]/podcaster-agent \
      --timeout 3600 \
      --concurrency 1 \
      --set-env-vars PERSONA_ID=host_sascha
    ```
    *Note: For production, consider GKE or Compute Engine for agents to avoid cold starts and connection limits.*

## 3. Frontend (Cloud Run)

1.  **Build:**
    ```bash
    docker build -t gcr.io/[PROJECT_ID]/podcaster-frontend ./frontend
    docker push gcr.io/[PROJECT_ID]/podcaster-frontend
    ```

2.  **Deploy:**
    ```bash
    gcloud run deploy podcaster-frontend \
      --image gcr.io/[PROJECT_ID]/podcaster-frontend \
      --allow-unauthenticated
    ```

## 4. Environment Variables (`.env.yaml`)
Ensure your `.env.yaml` contains:
```yaml
GOOGLE_API_KEY: "..."
LIVEKIT_URL: "wss://<your-vm-ip>"
LIVEKIT_API_KEY: "..."
LIVEKIT_API_SECRET: "..."
REDIS_URL: "redis://<redis-host>:6379"
```
