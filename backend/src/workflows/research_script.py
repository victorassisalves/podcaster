from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from google import genai
from google.genai import types
import os
import json

class State(TypedDict):
    theme: str
    research_report: Optional[str]
    script_outline: Optional[dict]
    errors: List[str]

def research_node(state: State):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"errors": ["GOOGLE_API_KEY not found"]}

    client = genai.Client(api_key=api_key)
    try:
        model_id = "deep-research-pro-preview-12-2025"
        prompt = f"Perform deep research on the following podcast theme: {state['theme']}. "                  f"Provide a detailed report including key facts, recent news, and interesting angles."

        # Using the Interactions API for Deep Research
        interaction = client.interactions.create(
            model=model_id,
            input=prompt
        )

        # Extract content from interaction.outputs
        report = ""
        if interaction.outputs:
            for part in interaction.outputs:
                # The 'part' seems to be a Content-like object or has a text attribute
                if hasattr(part, 'text'):
                    report += part.text
                elif isinstance(part, str):
                    report += part
                elif hasattr(part, 'candidates'): # Fallback for some types
                    for cand in part.candidates:
                        for p in cand.content.parts:
                            report += p.text

        if not report:
            # Final fallback, try to get anything from the interaction
            report = str(interaction)

        return {"research_report": report}
    except Exception as e:
        return {"errors": state.get("errors", []) + [str(e)]}

def scriptwriter_node(state: State):
    if state.get("errors"):
        return state

    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    try:
        model_id = "gemini-2.0-flash"

        prompt = f"Based on this research: {state['research_report']}, create a structured podcast script outline. "                  f"Include: duration, topics to approach, topics to avoid, specific questions, and guest roles."                  f"Format the output as a JSON object with keys: duration, topics_to_approach, topics_to_avoid, questions, roles."

        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        outline = json.loads(response.text)
        return {"script_outline": outline}
    except Exception as e:
        return {"errors": state.get("errors", []) + [str(e)]}

def create_research_workflow():
    workflow = StateGraph(State)

    workflow.add_node("research", research_node)
    workflow.add_node("scriptwriter", scriptwriter_node)

    workflow.set_entry_point("research")
    workflow.add_edge("research", "scriptwriter")
    workflow.add_edge("scriptwriter", END)

    return workflow.compile()
