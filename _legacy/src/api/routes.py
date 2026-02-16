from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.workflows.research_script import create_research_workflow

router = APIRouter()

class ResearchRequest(BaseModel):
    theme: str

@router.post("/research")
async def start_research(request: ResearchRequest):
    workflow = create_research_workflow()
    result = workflow.invoke({"theme": request.theme, "errors": []})

    if result.get("errors"):
        raise HTTPException(status_code=500, detail=result["errors"])

    return result

from src.api.persistence import persistence, AgentProfile, Episode
import uuid

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

from livekit import api
import os

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
