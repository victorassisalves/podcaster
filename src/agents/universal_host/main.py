import os
import asyncio
import logging
from .engine import UniversalHostAgent
from ...infrastructure.redis_store import RedisStateStore
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    persona_id = os.environ.get("HOST_PERSONA_ID", "host_sascha")
    # Agent name convention: host_{persona_id}
    agent_name = f"host_{persona_id}"

    redis_url = os.environ.get("REDIS_URL", "redis://redis:6379")
    store = RedisStateStore(redis_url)

    logger.info(f"Initializing Universal Host Agent: {agent_name}")
    agent = UniversalHostAgent(name=agent_name, persona_id=persona_id, state_store=store)

    # Create Agent Card dynamically from Persona
    # Assuming persona is loaded by __init__
    if not agent.persona:
        logger.error("Persona not loaded. Exiting.")
        return

    # Use environment variable for the host/port to be correct in Docker network
    host_env = os.environ.get("HOST", "0.0.0.0")
    port_env = int(os.environ.get("PORT", "8000"))
    # The URL reported in the card must be reachable by others (e.g. Producer)
    # In Docker Compose, service name might be used.
    # We'll use a placeholder or ENV var for the external URL base.
    external_url = os.environ.get("A2A_EXTERNAL_URL", f"http://localhost:{port_env}/a2a")

    card = AgentCard(
        name=agent.persona.name,
        description=agent.persona.system_prompt[:200] + "...",
        version="0.1.0",
        url=external_url,
        skills=[
            AgentSkill(
                id="perform_dialogue",
                name="Perform Dialogue",
                description="Improvise podcast dialogue based on topics.",
                tags=["host", "podcast"]
            )
        ],
        capabilities=AgentCapabilities(),
        defaultInputModes=["text"],
        defaultOutputModes=["text"]
    )

    logger.info(f"Generated Agent Card for {agent.persona.name}")

    # Wrap with A2A
    app = to_a2a(agent, agent_card=card)

    # Start the agent's main loop in the background
    # We store the task to prevent garbage collection (though loop is infinite)
    loop_task = asyncio.create_task(agent.run_loop())

    # Run the A2A server
    logger.info(f"Starting A2A server on {host_env}:{port_env}")
    config = uvicorn.Config(app, host=host_env, port=port_env, log_level="info")
    server = uvicorn.Server(config)

    try:
        await server.serve()
    except asyncio.CancelledError:
        logger.info("Server cancelled")
    finally:
        loop_task.cancel()
        try:
            await loop_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(main())
