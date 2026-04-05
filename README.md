# Learning with AI

An interactive AI-powered learning platform that lets you study any topic through conversation with a Claude tutor. Define your own topics and themes in a config file, then learn at your own pace through a local web interface.

## Features

- **Configurable topics** — define themes and subtopics in `config.json` (ships with LLM and ML fundamentals as examples)
- **Persistent chat history** — conversations are saved per topic as JSON, so you can pick up where you left off
- **Frustration detection** — the tutor detects when you're struggling and adapts its explanations
- **Auto-generated learning notes** — key concepts and frustration points are logged automatically to `learning_data/learning_notes.md`
- **Export to slides** — generate reveal.js presentations from high-signal exchanges across all topics
- **Streaming responses** — real-time markdown rendering with syntax-highlighted code blocks

## Prerequisites

- Python 3.11+
- `ANTHROPIC_API_KEY` environment variable set

## Install dependencies

```bash
uv venv
uv pip install fastapi uvicorn anthropic
```

## Run

```bash
python server.py
```

The platform opens automatically at **http://localhost:8765**.

## Usage

1. **Select a topic** from the sidebar — an introductory lesson is generated on first visit
2. **Ask questions** in the chat (send with **Shift+Enter** or the Send button)
3. **View Notes** — see auto-collected key concepts and frustration points
4. **Export Slides** — generate a reveal.js presentation from your learning sessions

## Data

All data is stored in `learning_data/`:

- `chats/` — per-topic chat history (JSON)
- `exports/` — exported slide decks (HTML)
- `learning_notes.md` — auto-generated learning notes

## Demo Data

The `examples/` directory contains sample chat histories, learning notes, and an exported slide deck for reference. To use them as starting data:

```bash
cp -r examples/chats/* learning_data/chats/
cp examples/learning_notes.md learning_data/learning_notes.md
```
