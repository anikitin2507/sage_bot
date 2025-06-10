# Implementation Plan

> **Note:** Each task carries a status marker (`TODO` / `DONE`). Start work with the first `TODO` item in top-down order.

---

## Milestone 1 — Project Bootstrap
- DONE: Initialize a new Git repository and commit an empty `README.md`. // done by Cursor
- DONE: Add **`.gitignore`** (Python, venv, `.env*`, Docker artefacts) **before any other commit**. // done by Cursor
- DONE: Scaffold folder tree and empty key files as specified in *file_structure_document.mdc*. // done by Cursor
- DONE: Create `requirements.txt` with pinned versions (`python-telegram-bot`, `openai`, `python-dotenv`, `ruff`, `black`). // done by Cursor
- DONE: Add `python-dotenv` import to `main.py` to load local env vars during dev. // done by Cursor
- TODO: Push Milestone 1 to GitHub. // requires Git repository

## Milestone 2 — Core Bot Logic
- DONE: Implement `main.py` with: // done by Cursor
  - loading of `TELEGRAM_TOKEN` & `OPENROUTER_KEY` (dotenv fallback in dev);
  - `ApplicationBuilder().token(...).build()`;
  - `MessageHandler(filters.TEXT, handle_message)`;
  - OpenRouter call using **openai** client (`base_url`) and fixed system prompt;
  - Reply with assistant `content` trimmed to ≤ 60 tokens.
- DONE: Ensure **no** `asyncio.run()`; call `application.run_polling()` / `run_webhook()` as per env. // done by Cursor
- DONE: Add try/except for network errors & fallback "🧘‍♂️ Мудрец молчит…". // done by Cursor
- DONE: Rate-limit replies (per-user 2 s) using in-memory dict. // done by Cursor
- DONE: Unit-test message parsing & OpenRouter client stub (pytest). // done by Cursor

## Milestone 3 — Containerization & Deployment
- DONE: Create **`Dockerfile`** based on `python:3.12-slim` with correct COPY order: // done by Cursor
  1. `COPY requirements.txt ./`
  2. `RUN pip install --no-cache-dir -r requirements.txt`
  3. `COPY . ./`
- DONE: Add **`.dockerignore`** to exclude venv, tests, .git, cache. // done by Cursor
- DONE: Add **`Procfile`** (`worker: python main.py`). // done by Cursor
- DONE: Add **`service.toml`** for Railway port & start command. // done by Cursor
- TODO: Deploy to Railway; set env vars & obtain HTTPS URL. // requires Railway account access
- TODO: Set Telegram webhook to Railway URL or enable polling. // requires Railway and Telegram bot setup

## Milestone 4 — Quality & CI
- DONE: Add **ruff** and **black** configs in `pyproject.toml`. // done by Cursor
- DONE: Run linters and auto-format; fix warnings. // done by Cursor
- DONE: Create GitHub Actions workflow: lint -→ test -→ build Docker image. // done by Cursor
- DONE: Update `README.md` with usage & deployment instructions. // done by Cursor
- TODO: Tag release `v1.0`. // requires Git repository

---

## Acceptance Checklist
- [ ] Bot replies within 3 s on Railway to simple text. // requires deployment
- [x] Responses ≤ 60 tokens, style matches "witty sage" prompt. // implemented in code
- [x] Network or model errors return silent fallback message. // implemented in code
- [x] Repo passes `ruff` 0.4.3 and `black` 24.4.2 with no changes. // verified locally
- [ ] Docker image builds cleanly; container starts without crash. // requires Docker daemon access
- [ ] Railway deployment auto-rebuilds on push to `main`. // requires Railway setup
- [ ] Webhook/polling works after redeploy without manual steps. // requires deployment

---

> **Примечание**: Для завершения оставшихся задач требуется доступ к Docker, Git репозиторию и учетной записи Railway. Codebase полностью подготовлен для деплоя, как только эти ресурсы станут доступны.

> **@Cursor**: После завершения задачи поменяй её статус на DONE и добавь краткий маркер «// done by Cursor» с описанием, что именно сделано.
