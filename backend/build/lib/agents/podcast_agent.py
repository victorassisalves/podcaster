from livekit.agents import JobContext, WorkerOptions, cli, AgentSession
from livekit.plugins import google
import os

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent_name = os.getenv("AGENT_NAME", "Alex")
    agent_role = os.getenv("AGENT_ROLE", "Host")
    script_outline = os.getenv("SCRIPT_OUTLINE", "{}")

    instructions = f"""
    You are {agent_name}, the {agent_role} of this live podcast.
    Follow this script outline: {script_outline}

    Coordinate with other agents and humans in the room.
    Maintain a natural, conversational tone.
    """

    model = google.realtime.RealtimeModel(
        model="gemini-2.5-flash-native-audio-preview-12-2025",
        instructions=instructions,
        voice="Puck",
    )

    session = AgentSession(
        llm=model,
    )

    # Note: In the latest livekit-agents, we might need to join the room or start the session differently
    # But based on the provided snippet, this is the pattern.

    print(f"Agent {agent_name} ({agent_role}) ready in room {ctx.room.name}")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
