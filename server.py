from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"
CONFIG_EXAMPLE_PATH = BASE_DIR / "config.example.json"


def load_config() -> dict:
    path = CONFIG_PATH if CONFIG_PATH.exists() else CONFIG_EXAMPLE_PATH
    with open(path) as f:
        return json.load(f)


def save_config(config: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")


CONFIG = load_config()
MODEL = CONFIG.get("model", "claude-sonnet-4-6")
MAX_TOKENS = CONFIG.get("max_tokens", 4096)
HOST = CONFIG.get("host", "0.0.0.0")
PORT = CONFIG.get("port", 8765)
SYSTEM_PROMPT_TEMPLATE = CONFIG["prompts"]["system"]
INTRO_PROMPT = CONFIG["prompts"]["intro"]
DATA_DIR = BASE_DIR / "learning_data"
CHATS_DIR = DATA_DIR / "chats"
EXPORTS_DIR = DATA_DIR / "exports"
NOTES_FILE = DATA_DIR / "learning_notes.md"

for d in [DATA_DIR, CHATS_DIR, EXPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)
if not NOTES_FILE.exists():
    NOTES_FILE.write_text("# Learning Notes\n")

app = FastAPI()
client = anthropic.Anthropic()


def slugify(text: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", text.lower()))


def get_themes() -> dict:
    """Return themes dict from current config."""
    config = load_config()
    return config.get("themes", {})


def get_theme_topics(theme_slug: str) -> dict[str, str] | None:
    themes = get_themes()
    theme = themes.get(theme_slug)
    if not theme:
        return None
    return theme.get("topics", {})


def get_topic_name(theme_slug: str, topic_slug: str) -> str | None:
    topics = get_theme_topics(theme_slug)
    if not topics:
        return None
    for name in topics:
        if slugify(name) == topic_slug:
            return name
    return None


def theme_chats_dir(theme_slug: str) -> Path:
    d = CHATS_DIR / theme_slug
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_history(theme_slug: str, topic_slug: str) -> dict:
    path = theme_chats_dir(theme_slug) / f"{topic_slug}.json"
    if path.exists():
        return json.loads(path.read_text())
    topic_name = get_topic_name(theme_slug, topic_slug)
    return {"topic": topic_name or topic_slug, "topic_slug": topic_slug, "messages": []}


def save_history(theme_slug: str, topic_slug: str, history: dict):
    path = theme_chats_dir(theme_slug) / f"{topic_slug}.json"
    path.write_text(json.dumps(history, indent=2))


def get_system_prompt(theme_slug: str, topic: str) -> str:
    topics = get_theme_topics(theme_slug) or {}
    desc = topics.get(topic, "")
    topic_full = f"{topic}: {desc}" if desc else topic
    return SYSTEM_PROMPT_TEMPLATE.replace("{topic}", topic_full)


def parse_assistant_response(raw: str) -> dict:
    """Parse response with trailing <!--META:{...}--> comment."""
    meta = {"key_concepts": [], "frustration_detected": False, "importance": "low"}
    response_text = raw

    m = re.search(r"<!--META:(.*?)-->\s*$", raw, re.DOTALL)
    if m:
        response_text = raw[:m.start()].rstrip()
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    else:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict) and "response" in parsed:
                return parsed
        except json.JSONDecodeError:
            pass

    return {
        "response": response_text,
        "key_concepts": meta.get("key_concepts", []),
        "frustration_detected": meta.get("frustration_detected", False),
        "importance": meta.get("importance", "low"),
    }


def append_notes(topic: str, key_concepts: list[str], importance: str, frustration: bool, user_msg: str):
    content = NOTES_FILE.read_text()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    topic_header = f"\n## {topic}\n"

    if f"## {topic}" not in content:
        content += f"{topic_header}### Key Details\n\n### Frustration Points\n\n"

    if frustration:
        marker = f"## {topic}\n"
        idx = content.index(marker) + len(marker)
        rest = content[idx:]
        frust_idx = rest.index("### Frustration Points\n") + len("### Frustration Points\n")
        insert_pos = idx + frust_idx
        entry = f"- [{now}] User confused about: \"{user_msg[:100]}\"\n"
        content = content[:insert_pos] + entry + content[insert_pos:]

    if key_concepts and importance == "high":
        marker = f"## {topic}\n"
        idx = content.index(marker) + len(marker)
        rest = content[idx:]
        key_idx = rest.index("### Key Details\n") + len("### Key Details\n")
        insert_pos = idx + key_idx
        entry = f"- [{now}] {', '.join(key_concepts)}\n"
        content = content[:insert_pos] + entry + content[insert_pos:]

    NOTES_FILE.write_text(content)


def build_api_messages(messages: list[dict]) -> list[dict]:
    api_msgs = []
    for m in messages:
        if m["role"] == "user":
            api_msgs.append({"role": "user", "content": m["content"]})
        else:
            api_msgs.append({"role": "assistant", "content": m["content"]})
    return api_msgs


class ChatRequest(BaseModel):
    message: str


class CreateThemeRequest(BaseModel):
    name: str
    topics: dict[str, str]


class AddTopicRequest(BaseModel):
    name: str
    description: str


# --- Frontend ---

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_path = BASE_DIR / "frontend.html"
    return HTMLResponse(html_path.read_text(), headers={"Cache-Control": "no-cache"})


# --- Theme APIs ---

@app.get("/api/themes")
async def list_themes():
    themes = get_themes()
    result = []
    for slug, theme in themes.items():
        result.append({
            "slug": slug,
            "name": theme["name"],
            "topic_count": len(theme.get("topics", {})),
        })
    return {"themes": result}


@app.post("/api/themes")
async def create_theme(req: CreateThemeRequest):
    config = load_config()
    theme_slug = slugify(req.name)
    if theme_slug in config.get("themes", {}):
        raise HTTPException(409, "Theme already exists")
    if "themes" not in config:
        config["themes"] = {}
    config["themes"][theme_slug] = {
        "name": req.name,
        "topics": req.topics,
    }
    save_config(config)
    theme_chats_dir(theme_slug)
    logger.info(f"Created theme: {req.name} ({len(req.topics)} topics)")
    return {"slug": theme_slug, "name": req.name}


@app.post("/api/themes/{theme_slug}/topics")
async def add_topic(theme_slug: str, req: AddTopicRequest):
    config = load_config()
    themes = config.get("themes", {})
    if theme_slug not in themes:
        raise HTTPException(404, "Theme not found")
    themes[theme_slug]["topics"][req.name] = req.description
    save_config(config)
    logger.info(f"Added topic '{req.name}' to theme '{theme_slug}'")
    return {"topic": req.name, "description": req.description}


@app.delete("/api/themes/{theme_slug}/topics/{topic_slug}")
async def remove_topic(theme_slug: str, topic_slug: str):
    config = load_config()
    themes = config.get("themes", {})
    if theme_slug not in themes:
        raise HTTPException(404, "Theme not found")
    topic_name = None
    for name in themes[theme_slug]["topics"]:
        if slugify(name) == topic_slug:
            topic_name = name
            break
    if not topic_name:
        raise HTTPException(404, "Topic not found")
    del themes[theme_slug]["topics"][topic_name]
    save_config(config)
    logger.info(f"Removed topic '{topic_name}' from theme '{theme_slug}'")
    return {"removed": topic_name}


# --- Topic & Chat APIs ---

@app.get("/api/topics/{theme_slug}")
async def list_topics(theme_slug: str):
    topics = get_theme_topics(theme_slug)
    if topics is None:
        raise HTTPException(404, "Theme not found")
    return {"topics": list(topics.keys())}


@app.get("/api/history/{theme_slug}/{topic_slug}")
async def get_history(theme_slug: str, topic_slug: str):
    topic_name = get_topic_name(theme_slug, topic_slug)
    if not topic_name:
        raise HTTPException(404, "Topic not found")

    history = load_history(theme_slug, topic_slug)

    if not history["messages"]:
        logger.info(f"Generating initial message for topic: {topic_name}")
        system = get_system_prompt(theme_slug, topic_name)
        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system,
            messages=[{"role": "user", "content": INTRO_PROMPT}],
        )
        raw = resp.content[0].text
        parsed = parse_assistant_response(raw)
        now = datetime.now(timezone.utc).isoformat()
        history["messages"].append({
            "role": "assistant",
            "content": parsed["response"],
            "timestamp": now,
            "meta": {
                "key_concepts": parsed.get("key_concepts", []),
                "frustration_detected": parsed.get("frustration_detected", False),
                "importance": parsed.get("importance", "high"),
            },
        })
        save_history(theme_slug, topic_slug, history)
        if parsed.get("key_concepts") and parsed.get("importance") == "high":
            append_notes(topic_name, parsed["key_concepts"], "high", False, "")

    return history


@app.post("/api/chat/{theme_slug}/{topic_slug}")
async def chat(theme_slug: str, topic_slug: str, req: ChatRequest):
    topic_name = get_topic_name(theme_slug, topic_slug)
    if not topic_name:
        raise HTTPException(404, "Topic not found")

    history = load_history(theme_slug, topic_slug)
    now = datetime.now(timezone.utc).isoformat()
    history["messages"].append({
        "role": "user",
        "content": req.message,
        "timestamp": now,
    })
    save_history(theme_slug, topic_slug, history)

    system = get_system_prompt(theme_slug, topic_name)
    api_messages = build_api_messages(history["messages"])

    logger.info(f"Chat request for {topic_name}: {req.message[:80]}")

    async def stream_response():
        full_text = ""
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system,
            messages=api_messages,
        ) as stream:
            for text in stream.text_stream:
                full_text += text
                yield f"data: {json.dumps({'type': 'chunk', 'content': text})}\n\n"

        parsed = parse_assistant_response(full_text)
        resp_now = datetime.now(timezone.utc).isoformat()
        history["messages"].append({
            "role": "assistant",
            "content": parsed["response"],
            "timestamp": resp_now,
            "meta": {
                "key_concepts": parsed.get("key_concepts", []),
                "frustration_detected": parsed.get("frustration_detected", False),
                "importance": parsed.get("importance", "low"),
            },
        })
        save_history(theme_slug, topic_slug, history)

        frustration = parsed.get("frustration_detected", False)
        key_concepts = parsed.get("key_concepts", [])
        importance = parsed.get("importance", "low")

        if frustration or (key_concepts and importance == "high"):
            append_notes(topic_name, key_concepts, importance, frustration, req.message)

        yield f"data: {json.dumps({'type': 'done', 'response': parsed['response'], 'meta': {'key_concepts': key_concepts, 'frustration_detected': frustration, 'importance': importance}})}\n\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")


# --- Export ---

SLIDE_SYSTEM_PROMPT = """You are a presentation designer. Given a learning conversation about a topic, create concise, visually engaging slide content in HTML for reveal.js.

RULES:
- Each slide must be a <section> element
- Use bullet points (<ul><li>) for key ideas — max 4-5 bullets per slide
- Keep text SHORT: each bullet should be one line, not a paragraph
- Use HTML tables for comparisons (e.g. pros vs cons, method A vs B)
- Use emoji as visual markers
- For processes/flows, use numbered steps with emoji arrows
- Include a short title <h3> on each slide
- If there's a key formula or definition, highlight it in a styled box: <div style="background:#f0f4ff;padding:12px 18px;border-radius:8px;border-left:4px solid #3b82f6;margin:12px 0;font-size:0.85em;">content</div>
- For code snippets, use <code> with dark background styling
- Do NOT reproduce the full conversation — distill into the essential takeaways
- Split long content across multiple <section> elements (one idea per slide)
- Style inline: use font-size:0.75em for body text, 0.65em for tables/code

OUTPUT FORMAT:
Return ONLY the <section> elements, no surrounding HTML. Multiple slides = multiple <section> tags."""


def summarize_for_slides(topic: str, exchanges: list[dict]) -> str:
    conversation_summary = []
    for ex in exchanges:
        entry = ""
        if ex.get("question"):
            entry += f"Q: {ex['question']}\n"
        entry += f"A: {ex['answer'][:2000]}"
        if ex.get("key_concepts"):
            entry += f"\nKey concepts: {', '.join(ex['key_concepts'])}"
        conversation_summary.append(entry)

    prompt = (
        f"Topic: {topic}\n\n"
        f"Here are the key exchanges from a learning session:\n\n"
        + "\n\n---\n\n".join(conversation_summary)
        + "\n\nCreate presentation slides that distill these into "
        "concise, visually structured content. "
        "Aim for 1-2 slides per exchange, focusing on the core ideas."
    )

    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SLIDE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


@app.post("/api/export/{theme_slug}")
async def export_slides(theme_slug: str):
    chats_path = theme_chats_dir(theme_slug)
    all_histories = []
    for f in sorted(chats_path.glob("*.json")):
        hist = json.loads(f.read_text())
        if hist.get("messages"):
            all_histories.append(hist)

    if not all_histories:
        raise HTTPException(400, "No chat history to export")

    themes = get_themes()
    theme_name = themes.get(theme_slug, {}).get("name", theme_slug)
    today = datetime.now().strftime("%Y-%m-%d")
    topic_names = [h["topic"] for h in all_histories]

    slides_html = []
    topics_list = "".join(f"<li>{t}</li>" for t in topic_names)
    slides_html.append(f"""<section>
<h1>{theme_name}</h1>
<h3>{today}</h3>
<ul style="list-style:none;font-size:0.8em;">{topics_list}</ul>
</section>""")

    all_key_concepts = []

    for hist in all_histories:
        topic = hist["topic"]
        exchanges = []
        for i, msg in enumerate(hist["messages"]):
            if msg["role"] != "assistant":
                continue
            meta = msg.get("meta", {})
            importance = meta.get("importance", "low")
            key_concepts = meta.get("key_concepts", [])
            if importance == "high" or key_concepts:
                user_q = ""
                if i > 0 and hist["messages"][i - 1]["role"] == "user":
                    user_q = hist["messages"][i - 1]["content"]
                exchanges.append({
                    "question": user_q,
                    "answer": msg["content"],
                    "key_concepts": key_concepts,
                })
                all_key_concepts.extend(key_concepts)

        if not exchanges:
            continue

        slides_html.append(
            f'<section><section><h1>{topic}</h1>'
            f'<p style="color:#64748b;font-size:0.7em;">'
            f'{len(exchanges)} key exchanges</p></section>'
        )

        logger.info(f"Generating slides for topic: {topic} ({len(exchanges)} exchanges)")
        try:
            topic_slides = summarize_for_slides(topic, exchanges)
            slides_html.append(topic_slides)
        except Exception as e:
            logger.error(f"Slide generation failed for {topic}: {e}")
            for ex in exchanges:
                slide = "<section>"
                if ex["question"]:
                    q_esc = ex["question"][:150].replace("&", "&amp;").replace("<", "&lt;")
                    slide += f"<h3>{q_esc}</h3>"
                if ex["key_concepts"]:
                    items = "".join(f"<li>{c}</li>" for c in ex["key_concepts"])
                    slide += f'<ul style="font-size:0.75em;">{items}</ul>'
                slide += "</section>"
                slides_html.append(slide)

        topic_concepts = []
        for msg in hist["messages"]:
            if msg["role"] == "assistant":
                topic_concepts.extend(msg.get("meta", {}).get("key_concepts", []))
        if topic_concepts:
            unique = list(dict.fromkeys(topic_concepts))
            items = "".join(f'<li>{c}</li>' for c in unique)
            slides_html.append(
                f'<section><h2>{topic}</h2>'
                f'<h4 style="color:#64748b;">Key Concepts</h4>'
                f'<ul style="list-style:none;font-size:0.75em;">{items}</ul></section>'
            )
        slides_html.append("</section>")

    if all_key_concepts:
        unique_all = list(dict.fromkeys(all_key_concepts))[:30]
        mid = (len(unique_all) + 1) // 2
        col1 = "".join(f"<li>{c}</li>" for c in unique_all[:mid])
        col2 = "".join(f"<li>{c}</li>" for c in unique_all[mid:])
        slides_html.append(
            f'<section><h1>Key Takeaways</h1>'
            f'<div style="display:flex;gap:40px;font-size:0.7em;">'
            f'<ul style="flex:1;">{col1}</ul>'
            f'<ul style="flex:1;">{col2}</ul>'
            f'</div></section>'
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"learning_slides_{theme_slug}_{timestamp}.html"

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{theme_name} — {today}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
<style>
.reveal ul {{ text-align: left; }}
.reveal li {{ margin-bottom: 0.4em; }}
.reveal table {{ font-size: 0.65em; margin: 0 auto; border-collapse: collapse; }}
.reveal th, .reveal td {{ padding: 8px 14px; border: 1px solid #e2e8f0; text-align: left; }}
.reveal th {{ background: #f1f5f9; font-weight: 600; }}
.reveal code {{ background: #1e293b; color: #e2e8f0; padding: 2px 6px; border-radius: 4px; font-size: 0.85em; }}
.reveal pre {{ text-align: left; }}
</style>
</head>
<body>
<div class="reveal"><div class="slides">
{''.join(slides_html)}
</div></div>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script>Reveal.initialize({{hash: true, slideNumber: true, transition: 'slide'}});</script>
</body>
</html>"""

    out_path = EXPORTS_DIR / filename
    out_path.write_text(html)
    logger.info(f"Exported slides to {out_path}")
    return {"file": str(out_path), "url": f"/exports/{filename}"}


@app.get("/exports/{filename}")
async def serve_export(filename: str):
    path = EXPORTS_DIR / filename
    if not path.exists():
        raise HTTPException(404, "File not found")
    return FileResponse(path, media_type="text/html")


@app.get("/api/exports")
async def list_exports():
    files = sorted(EXPORTS_DIR.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [
        {"filename": f.name, "url": f"/exports/{f.name}", "size": f.stat().st_size}
        for f in files
    ]


@app.get("/api/notes")
async def get_notes():
    return {"content": NOTES_FILE.read_text()}


if __name__ == "__main__":
    import webbrowser
    import threading

    def open_browser():
        import time
        time.sleep(1.5)
        webbrowser.open(f"http://localhost:{PORT}")

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host=HOST, port=PORT)
