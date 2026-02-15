# Learnings

## Technical
- **LangGraph Streaming**: Using `workflow.stream(inputs)` is effective for iterating over graph events. When streaming via FastAPI, using `StreamingResponse` with NDJSON (NewLine Delimited JSON) is a robust way to send events (logs, progress, results) to the frontend.
- **MUI with Next.js App Router**: MUI components work well in client components (`"use client"`). However, proper theme registry setup is recommended for production to avoid FOUC.
- **MUI Grid v2**: In recent MUI versions (v6+), the `Grid` component has evolved. `Grid` (v2) uses the `size` prop instead of `item` and `xs/sm/md`. It is important to check the specific version installed.

## Domain
- **Podcast Workflow**: The workflow involves distinct stages: Configuration -> Research -> Script Generation -> Review -> Recording. Separating these stages in the UI (Wizard pattern) improves UX significantly.
- **Agent Roles**: Defining agent roles (Host, Guest, etc.) *before* script generation allows the LLM to write more specific and character-driven scripts.
