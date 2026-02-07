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
