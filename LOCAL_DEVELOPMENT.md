# Local Development Guide

This guide explains how to run the Podcaster AI platform locally using Docker Compose, connecting to LiveKit Cloud.

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. **Environment Variables**:
   A `.env` file has been created in the root directory with your provided keys.
   It is configured to connect to your LiveKit Cloud project at: `wss://podcaster-oc0f5phg.livekit.cloud`.

2. **Google Cloud Credentials**:
   The `google-creds.json` file in the root directory contains your Service Account key. This is mounted into the backend and agent containers.

## Running the Platform

To start the services (Backend, Frontend, and Agent):

```bash
docker-compose up --build
```

Once the containers are running:
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **LiveKit**: Connecting to LiveKit Cloud (`wss://podcaster-oc0f5phg.livekit.cloud`)

### Services Overview
- **backend**: FastAPI server handling research, persistence, and tokens.
- **frontend**: Next.js dashboard and live room.
- **agent**: The AI podcast agent that joins the cloud room automatically.

## Troubleshooting

### Port Conflicts
Ensure ports `3000` and `8000` are not being used by other applications.

### Google Cloud Permissions
If you see permission errors, ensure the Service Account in `google-creds.json` has the following roles:
- Firestore User
- Storage Object Admin
- Vertex AI User (for Gemini)

### LiveKit Connection
Since we are using LiveKit Cloud, ensure your local machine has internet access and that the API keys in `.env` are valid.
