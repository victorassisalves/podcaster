from google.cloud import firestore
import os
from typing import List, Optional, Dict
from pydantic import BaseModel
import uuid

class AgentProfile(BaseModel):
    id: str
    name: str
    role: str
    personality: str
    voice_id: str
    provider: str = "google"

class Episode(BaseModel):
    id: str
    theme: str
    script_outline: Optional[Dict] = None
    status: str = "created"
    agent_ids: List[str] = []
    recording_url: Optional[str] = None

class PersistenceManager:
    def __init__(self):
        self.db = None
        self._mock_agents: List[AgentProfile] = [
            AgentProfile(id="1", name="Alex", role="Host", personality="Friendly and inquisitive", voice_id="Puck"),
            AgentProfile(id="2", name="Jordan", role="Tech Expert", personality="Analytical and deep-diving", voice_id="Charley"),
            AgentProfile(id="3", name="Sam", role="Skeptic", personality="Questioning and critical", voice_id="Stevie")
        ]
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            try:
                self.db = firestore.Client()
            except Exception:
                print("Firestore client could not be initialized. Using mock persistence.")

    def get_agents(self) -> List[AgentProfile]:
        if not self.db:
            return self._mock_agents

        docs = self.db.collection("agents").stream()
        agents = [AgentProfile(**doc.to_dict(), id=doc.id) for doc in docs]
        return agents if agents else self._mock_agents

    def save_agent(self, agent: AgentProfile):
        if not self.db:
            # In mock mode, we append to the list if not exists
            if not any(a.id == agent.id for a in self._mock_agents):
                self._mock_agents.append(agent)
            return
        self.db.collection("agents").document(agent.id).set(agent.dict())

    def get_episode(self, episode_id: str) -> Optional[Episode]:
        if not self.db: return None
        doc = self.db.collection("episodes").document(episode_id).get()
        if doc.exists:
            return Episode(**doc.to_dict(), id=doc.id)
        return None

    def save_episode(self, episode: Episode):
        if not self.db: return
        self.db.collection("episodes").document(episode.id).set(episode.dict())

persistence = PersistenceManager()
