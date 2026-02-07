# Local Development Guide

This guide explains how to run the Podcaster AI platform locally using Docker Compose.

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. **Environment Variables**:
   A `.env` file has been created in the root directory with your provided keys.
   If you need to change them, edit the `.env` file.

2. **Google Cloud Credentials**:
   The `google-creds.json` file in the root directory contains your Service Account key. This is mounted into the backend and agent containers.

3. **LiveKit Configuration**:
   The `livekit.yaml` file configures the local LiveKit server. It uses the API keys defined in your `.env`.

## Running the Platform

To start the entire stack (LiveKit, Backend, Frontend, and Agent):

```bash
docker-compose up --build
```

Once the containers are running:
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **LiveKit Server**: `ws://localhost:7880`

### Services Overview
- **livekit**: Local LiveKit server for real-time audio.
- **backend**: FastAPI server handling research, persistence, and tokens.
- **frontend**: Next.js dashboard and live room.
- **agent**: The AI podcast agent that joins the room automatically.

## Troubleshooting

### Port Conflicts
Ensure ports `3000`, `8000`, `7880`, and `7881` (UDP) are not being used by other applications.

### Google Cloud Permissions
If you see permission errors, ensure the Service Account in `google-creds.json` has the following roles:
- Firestore User
- Storage Object Admin
- Vertex AI User (for Gemini)

### LiveKit Connection Issues
If the frontend cannot connect to LiveKit, ensure `NEXT_PUBLIC_LIVEKIT_URL` in `.env` is set to `ws://localhost:7880`.
