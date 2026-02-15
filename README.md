# Podcaster AI

A multi-agent live podcast platform hosted on GCP.

## Features
- **Deep Research**: Uses Gemini 2.0 Deep Research to generate comprehensive podcast scripts.
- **Multi-Agent Orchestration**: LangGraph-powered workflows for pre-production and LiveKit for real-time interaction.
- **Live Interaction**: Real-time WebRTC audio with AI agents and human participants.
- **Realistic Voices**: Integrated with Google TTS (Journey voices) and Gemini Live API.
- **Recording**: Automated recording via LiveKit Egress to Google Cloud Storage.

## Project Structure
- `backend/`: Python FastAPI, LangGraph, and LiveKit Agents.
- `frontend/`: Next.js dashboard and live room.
- `infra/`: Deployment instructions for GCP.

## Getting Started
See `infra/DEPLOYMENT.md` for setup and deployment instructions.

## Docker Development (Offline/Local)
To run the entire stack locally using Docker:

1.  **Prerequisites**:
    *   Docker and Docker Compose installed.
    *   `google-creds.json` in the project root (if using Google Cloud services).
    *   `local.env` or `.env` file created from `.env.example`.

2.  **Setup**:
    ```bash
    cp .env.example .env
    # Fill in your credentials in .env
    ```

3.  **Run**:
    ```bash
    docker-compose up --build
    ```

    *   Backend API: http://localhost:8000
    *   Frontend: http://localhost:3000

    The backend code is mounted from `./backend`, so changes will reload automatically.
