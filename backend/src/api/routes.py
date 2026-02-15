from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json
from src.workflows.research_script import create_research_workflow
from src.api.persistence import persistence, AgentProfile, Episode
from livekit import api
import os
import uuid

router = APIRouter()

class ResearchRequest(BaseModel):
    theme: str
    duration: int = 15
    tone: str = "engaging"
    agent_ids: List[str] = []

@router.post("/research")
async def start_research(request: ResearchRequest):
    # Resolve agent ids to profiles
    all_agents = persistence.get_agents()
    selected_agents = [a.dict() for a in all_agents if a.id in request.agent_ids]

    inputs = {
        "theme": request.theme,
        "duration": request.duration,
        "tone": request.tone,
        "agent_profiles": selected_agents,
        "errors": []
    }

    async def event_generator():
        yield json.dumps({"type": "log", "message": f"Starting deep research on '{request.theme}'..."}) + "\n"
        yield json.dumps({"type": "progress", "stage": "research", "percent": 10}) + "\n"

        workflow = create_research_workflow()

        # Note: In a production app with sync nodes, run this in a threadpool
        # For now we iterate the sync generator
        try:
            for event in workflow.stream(inputs):
                if "research" in event:
                    data = event["research"]
                    if data.get("errors"):
                        yield json.dumps({"type": "error", "message": str(data["errors"])}) + "\n"
                    else:
                        yield json.dumps({"type": "log", "message": "Deep Research complete. Analyzing..."}) + "\n"
                        yield json.dumps({"type": "progress", "stage": "research", "percent": 50}) + "\n"
                        # Optional: yield partial report?

                if "scriptwriter" in event:
                    data = event["scriptwriter"]
                    if data.get("errors"):
                        yield json.dumps({"type": "error", "message": str(data["errors"])}) + "\n"
                    else:
                        yield json.dumps({"type": "log", "message": "Script generated successfully."}) + "\n"
                        yield json.dumps({"type": "progress", "stage": "script", "percent": 100}) + "\n"
                        yield json.dumps({"type": "result", "data": data.get("script_outline")}) + "\n"
        except Exception as e:
            yield json.dumps({"type": "error", "message": f"Workflow execution failed: {str(e)}"}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

@router.get("/agents")
async def get_agents():
    return persistence.get_agents()

@router.post("/episodes")
async def create_episode(theme: str):
    episode_id = str(uuid.uuid4())
    episode = Episode(id=episode_id, theme=theme)
    persistence.save_episode(episode)
    return episode

@router.get("/episodes/{episode_id}")
async def get_episode(episode_id: str):
    episode = persistence.get_episode(episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return episode

@router.get("/token")
async def get_token(room: str, identity: str):
    token = api.AccessToken(
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET")
    ).with_identity(identity).with_name(identity).with_grants(api.VideoGrants(
        room_join=True,
        room=room,
    ))
    return {"token": token.to_jwt()}
