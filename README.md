# Learning Hub

An interactive AI-powered learning platform for studying topics through chat with a Claude tutor.

## Features

- **15 LLM-related topics** with dedicated AI tutors
- **Persistent chat history** per topic (saved as JSON)
- **Frustration detection** — the tutor adapts when you're struggling
- **Auto-generated learning notes** — key concepts and frustration points logged to `learning_data/learning_notes.md`
- **Export to slides** — generates reveal.js presentations from high-signal exchanges
- **Streaming responses** with markdown rendering and syntax highlighting

## Prerequisites

- Python 3.11+
- `ANTHROPIC_API_KEY` environment variable set

## Install dependencies

```bash
pip install fastapi uvicorn anthropic
```

## Run

```bash
cd learning_platform
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
