## Purpose

This file gives concise, actionable guidance for AI coding agents (Copilot / automation) to be immediately productive in this repository.

NOTE: a quick workspace scan found no existing agent instruction files. I made a small number of conservative assumptions based on the workspace name ("FastAPI Udemy\React App"). If any paths or technologies differ, update the file or tell the agent which paths to use.

## Agent contract
- Input: repository files and the user's prompt/issue. When running commands, assume a Windows PowerShell environment.
- Output: small, well-tested code changes, minimal edits, and a short summary explaining why each change was made.
- Error modes: if a file or directory referenced below doesn't exist, stop and ask the user for the correct path rather than guessing.

## High-level architecture (what to look for)
- Expected split: a FastAPI backend (Python) and a React frontend (JavaScript/TypeScript). Typical locations to check:
  - `backend/` or `server/` or top-level Python files like `main.py` or an `app/` package
  - `frontend/` or `client/` or `react-app/` with `package.json`, `src/`, `public/`
- Data flow: frontend calls REST/HTTP endpoints exposed by the FastAPI app. Look for CORS middleware, an `api` or `routers` package, and axios/fetch usage in React.

## Critical developer workflows (what agents should run / suggest)
- Dev startup (typical):
  - Backend: `python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; uvicorn backend.main:app --reload`
  - Frontend: `cd frontend; npm install; npm start` (or `yarn` if `yarn.lock` exists)
- Tests:
  - Backend: look for `pytest` config and run `pytest backend/tests` when present.
  - Frontend: run `npm test` (Jest) inside `frontend/` if `package.json` contains a `test` script.
- Lint / format:
  - Backend: `ruff`/`black`/`isort` if config files exist (pyproject.toml, .flake8). Suggest fix PRs with `black --check` and `ruff check` results.
  - Frontend: `eslint`/`prettier` if `package.json` scripts or config files exist.

## Project-specific conventions and patterns to detect
- Single API entrypoint: prefer editing `backend/main.py` or `backend/app/__init__.py` where `FastAPI()` is instantiated.
- Routers: look for `routers/` or `api/` packages. Add routes there, not in `main.py`, when possible.
- Dependency injection / startup events: check for `@app.on_event("startup")` or `lifespan` usage and register DB connections there.
- Env config: prefer `.env` plus `pydantic.BaseSettings` usage. If `.env` is missing, ask before adding secrets.
- Tests location: backend tests under `backend/tests/` and frontend under `frontend/src/__tests__/` or `frontend/tests/`.

## Integration points & external dependencies
- Typical integrations to search for:
  - Database (Postgres): look for `DATABASE_URL` or `sqlalchemy` imports
  - Redis: `redis`/`aioredis` imports
  - Message queues: `celery`, `rabbitmq` mentions
  - Third-party auth: `fastapi.security`, oauth libs
- When adding code that touches infra (DB migrations, new env vars), always add a short README note and ask about deployment processes.

## Examples (what to change and where)
- Adding a new API endpoint: add a router file under `backend/app/routers/` and register it in `backend/main.py` (or central router registry).
- Fixing a failing test: run `pytest -q backend/tests/<test_file>::<TestClass>::<test_method>` locally, include minimal fixture/data changes, and update tests.

## What agents must NOT do
- Do not commit secrets (.env with credentials, private keys). If a change requires secrets, stop and request sanitized values or CI secret names.
- Don’t assume build tools: if `poetry.lock`, `pyproject.toml`, `requirements.txt`, or `package.json` are missing, ask the user before adding one.

## When to ask the user (examples)
- Missing or ambiguous project root (no `backend/` or `frontend/`): ask where the main app files live.
- New infra requirements (DB migration or new external service): ask for deployment and secrets guidance.

## Quick checklist for PRs created by an agent
1. Explain the change in 3 lines or fewer (why, what files, how tested).
2. Include or update tests (one happy path + one edge case) where feasible.
3. Run lint/format and include the commands used in PR description.
4. Add one-line entry to `CHANGELOG.md` (if present) or the PR description.

## Next steps for the user
- If the repository structure differs from the assumptions above, tell the agent (or update this file) with the correct paths and the preferred dev start commands.

---
Please review this draft and point out any non-standard paths, missing frameworks, or preferred scripts so I can update the guidance to be exact for this codebase.
