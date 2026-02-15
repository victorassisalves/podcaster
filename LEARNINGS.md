# Learnings

## Technical
- **LangGraph Streaming**: Using `workflow.stream(inputs)` is effective for iterating over graph events. When streaming via FastAPI, using `StreamingResponse` with NDJSON (NewLine Delimited JSON) is a robust way to send events (logs, progress, results) to the frontend.
- **MUI with Next.js App Router**: MUI components work well in client components (`"use client"`). However, proper theme registry setup is recommended for production to avoid FOUC.
- **MUI Grid v2**: In recent MUI versions (v6+), the `Grid` component has evolved. `Grid` (v2) uses the `size` prop instead of `item` and `xs/sm/md`. It is important to check the specific version installed.

## Domain
- **Podcast Workflow**: The workflow involves distinct stages: Configuration -> Research -> Script Generation -> Review -> Recording. Separating these stages in the UI (Wizard pattern) improves UX significantly.
- **Agent Roles**: Defining agent roles (Host, Guest, etc.) *before* script generation allows the LLM to write more specific and character-driven scripts.

## Frontend Theme
- **MUI with Next.js App Router**: When using MUI with App Router, a client-side  is required to wrap the children in . This registry must handle  and  to prevent FOUC and ensure styles are injected correctly.
- **Dark Mode**: Explicitly setting  in the theme palette ensures all MUI components (TextFields, Cards, Typography) adapt their colors for high contrast against a dark background. Removing manual CSS backgrounds and relying on  is the correct approach.

## Frontend Theme
- **MUI with Next.js App Router**: When using MUI with App Router, a client-side `ThemeRegistry` is required to wrap the children in `layout.tsx`. This registry must handle `EmotionCache` and `ThemeProvider` to prevent FOUC and ensure styles are injected correctly.
- **Dark Mode**: Explicitly setting `mode: 'dark'` in the theme palette ensures all MUI components (TextFields, Cards, Typography) adapt their colors for high contrast against a dark background. Removing manual CSS backgrounds and relying on `CssBaseline` is the correct approach.

## Agent Management
- **Mock Persistence Strategy**: When using mock persistence (in-memory lists), modifying the list inside the class instance () works for the lifespan of the server process. However, this data is lost on restart. For a real app, Firestore or a local JSON file is needed.
- **Frontend Dialogs**: Using , , , and  provides a clean UX for forms without navigating away from the main wizard flow.

## Agent Management
- **Mock Persistence Strategy**: When using mock persistence (in-memory lists), modifying the list inside the class instance (`self._mock_agents`) works for the lifespan of the server process. However, this data is lost on restart. For a real app, Firestore or a local JSON file is needed.
- **Frontend Dialogs**: Using `Dialog`, `DialogTitle`, `DialogContent`, and `DialogActions` provides a clean UX for forms without navigating away from the main wizard flow.
