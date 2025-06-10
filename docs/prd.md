### Telegram Message Format
Telegram sends updates as JSON-serialized **`Update`** objects, delivered either by long-polling (`getUpdates`) or an HTTPS POST webhook.  
For a plain text message the payload looks like:

```json
{
  "update_id": 123456789,
  "message": {
    "message_id": 51,
    "from": { ... },
    "chat": { ... },
    "date": 1686400000,
    "text": "Hello, sage!"
  }
}
```

The user request is always in `update["message"]["text"]`.

## Product Requirements Document — “SageBot v1.0”

### 1. Overview / Problem
People often need quick, pithy life advice. Creating a Telegram bot that turns any user phrase into a concise, slightly ironic, philosophical response from a “sage” powered by the free Llama 3.1 8B model will let them get that advice instantly without opening a browser.

### 2. Key User Flows
1. **Ask-and-answer**  
   * User sends any text to @SageBot.  
   * Bot forwards the text (with fixed system role) to OpenRouter → Llama 3.1 8B.  
   * Bot returns the model’s short reply (≤ 60 tokens) to the same chat.  
2. **(v1.1) Contextual dialogue**  
   * Within the same chat, multiple questions maintain short conversational history (last N Q&A pairs) so the sage can give deeper follow-ups.

### 3. Functional Requirements
| ID | Requirement |
|----|-------------|
| F1 | Poll updates or receive webhook; extract `message.text`; ignore non-text payloads. |
| F2 | Compose OpenRouter request with: system prompt “You are a witty sage…”, user content, `max_tokens=60`, `model=meta-llama/llama-3.1-8b`. |
| F3 | Send HTTPS POST to `https://openrouter.ai/api/v1/chat/completions` with `Authorization: Bearer $OPENROUTER_KEY`. |
| F4 | Return only the assistant’s `content` field to the user. |
| F5 | Graceful error handling: network failure, rate limit, empty text ⇒ fallback reply “🧘‍♂️ Мудрец молчит…”. |
| F6 | Rate-limit to one response per user per 2 s to save tokens. |
| F7 | Configuration via env vars: `TELEGRAM_TOKEN`, `OPENROUTER_KEY`, `RAILWAY_ENV`. |
| F8 | Implementation stays inside **`main.py`** (≈ 50 LOC) using `requests` and `python-telegram-bot` 14+. |
| F9 | Ready-to-deploy `requirements.txt`, `Procfile`, and Railway `service.toml`. |
| F10 | Logging to stdout only. |

### 4. Non-Goals
* Voice, photo, sticker, inline-mode support.  
* Advanced prompt-engineering or paid OpenAI models.  
* Analytics, databases, admin panels.  
* Fine-grained per-user memory beyond simple rolling context (v1.1).

### 5. Milestones & Release Plan
| Date | Milestone | Deliverables |
|------|-----------|--------------|
| **Tonight (v1.0)** | MVP & deploy | `main.py`, helper files; live bot replying w/ single-shot sage advice. |
| +1 week (v1.1) | Context memory | In-memory rolling chat context (last 5 Q&A); env var `CONTEXT_SIZE`. |
| Later | Hardening | Caching, better rate-limit, tests, CI. |
