# Local Development Guide

This guide details how to set up the Podcaster 360 development environment on your local machine.

## Prerequisites

Before starting, ensure you have the following installed:

### 1. System Dependencies
*   **Python 3.10+** (Recommended: 3.11)
*   **Node.js 18+** & `npm`
*   **Docker & Docker Compose**
*   **FFmpeg** (Required for audio processing)
    *   **macOS:** `brew install ffmpeg`
    *   **Ubuntu:** `sudo apt install ffmpeg`
    *   **Windows:** Download and add to PATH.
*   **PortAudio** (Required for `pyaudio` if running agents locally)
    *   **macOS:** `brew install portaudio`
    *   **Ubuntu:** `sudo apt install libportaudio2`

### 2. LiveKit CLI (Optional but Recommended)
Useful for monitoring rooms and simulating participants.
*   **Install:** `curl -sSL https://get.livekit.io/cli | bash`
*   **Verify:** `lk --version`

## Project Setup

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd podcaster-ai
    ```

2.  **Environment Variables:**
    Copy `.env.example` to `.env` and fill in your credentials.
    ```bash
    cp .env.example .env
    ```
    Required keys:
    -   `GOOGLE_API_KEY` (Gemini)
    -   `LIVEKIT_URL`
    -   `LIVEKIT_API_KEY`
    -   `LIVEKIT_API_SECRET`
    -   `REDIS_URL` (defaults to `redis://localhost:6379`)

## Running Services

### 1. Backend (FastAPI)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -e .
python3 -m src.main
```
*   API available at: `http://localhost:8000`

### 2. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
*   Dashboard available at: `http://localhost:3000`

### 3. Agents (Python)
To run a specific agent (e.g., the Host Agent) directly:
```bash
# Ensure you are in the root directory and venv is active
python3 -m src.agents.universal_host.main
```

## Monitoring LiveKit Rooms

You can use the LiveKit CLI to inspect active rooms and participants.

```bash
# List rooms
lk room list --url <your-livekit-url> --api-key <key> --api-secret <secret>

# Join a room to listen (Headless)
lk room join --url <url> --api-key <key> --api-secret <secret> <room_name> --identity "listener"
```
