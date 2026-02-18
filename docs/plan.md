FastAPI + SQLAlchemy CRUD API Plan
Context
Add a FastAPI layer to expose CRUD operations on the existing SQLite database (data/arcade.db). SQLAlchemy ORM models live in their own src/models/ directory (separate from the API layer) so they can be shared across the codebase. The existing db_tools/db.py (raw sqlite3) is left untouched — the LLM pipeline and printer continue using it unchanged.

Final Directory Structure

src/
├── models/                  ← NEW: SQLAlchemy ORM (shared, not API-only)
│   ├── __init__.py          # re-exports all model classes + Base/engine/SessionLocal
│   ├── base.py              # engine, SessionLocal, DeclarativeBase
│   ├── todo.py              # Todo, TodoLine (TODOS + TODO_LINES — CASCADE parent-child)
│   ├── category.py          # Category, Streak (CATEGORIES + STREAKS — 1:1 CASCADE)
│   ├── game_run.py          # GameRun (GAME_RUNS — top-level, referenced by tasks+scoring)
│   ├── task.py              # Task, TaskLine (TASKS + TASK_LINES — CASCADE parent-child)
│   ├── scoring.py           # Scoring (SCORING — junction/ledger table)
│   └── llm_log.py           # LlmLog (LLM_LOGS — audit table)
│
├── api/                     ← NEW: FastAPI application
│   ├── __init__.py
│   ├── app.py               # FastAPI() instance, router registration, lifespan
│   ├── dependencies.py      # get_db() → yields SQLAlchemy Session
│   ├── middleware.py        # register_middleware(): CORS + request timing logger
│   ├── schemas/             # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── todo.py
│   │   ├── category.py
│   │   ├── game_run.py
│   │   ├── task.py
│   │   ├── scoring.py
│   │   └── llm_log.py
│   └── routes/              # APIRouter instances, one file per resource group
│       ├── __init__.py
│       ├── todos.py
│       ├── categories.py
│       ├── game_runs.py
│       ├── tasks.py
│       ├── scoring.py
│       └── llm_logs.py
│
├── db_tools/                ← UNCHANGED
│   └── db.py                # get_connection(), initialize_db() — raw sqlite3
...
Key Design Decisions
src/models/ at the src/ level (not inside api/)
Models represent the DB schema and are not API-specific. Placing them at the src/ level allows the LLM pipeline or printer to eventually use SQLAlchemy too without a circular import.

db_tools/db.py and SQLAlchemy coexist — one DB file, two access paths
db_tools/db.py → raw sqlite3 → used by process_input.py, setup.py, main.py, printer/
src/models/base.py → SQLAlchemy engine → used by FastAPI routes only
Both resolve to the same data/arcade.db. One-way dependency rule: api → models → base, never the reverse into existing modules.
initialize_db() (from db_tools) is still the single source of truth for schema creation. No Base.metadata.create_all() — this preserves triggers, views, indexes, and seed data from db.sql that SQLAlchemy doesn't know about.
Critical Files
File	Purpose
src/models/base.py	Engine + SessionLocal + Base. DB_PATH must resolve to data/arcade.db same as db_tools/db.py
src/db_tools/db.py	Path resolution pattern to mirror; boundary never to cross
data/db.sql	Ground truth for all table names, columns, constraints — SQLAlchemy models must match exactly
src/api/dependencies.py	get_db() generator — controls session lifecycle per request
src/api/app.py	Router registration; lifespan calls initialize_db() from db_tools as safety net
src/models/base.py (keystone file)

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# src/models/base.py → .parent=models → .parent=src → .parent=project_root
# Matches db_tools/db.py path resolution exactly
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "arcade.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},  # required for SQLite + multi-threaded FastAPI
    echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
Table → Model File Grouping Rationale
Model File	Tables	Why together
todo.py	TODOS + TODO_LINES	ON DELETE CASCADE, no meaning apart
category.py	CATEGORIES + STREAKS	1:1 with ON DELETE CASCADE, streaks own by category
game_run.py	GAME_RUNS	Top-level entity; isolated to avoid circular imports with task.py and scoring.py
task.py	TASKS + TASK_LINES	ON DELETE CASCADE, ordered subtasks owned by task
scoring.py	SCORING	Junction/ledger; isolated to avoid circular imports
llm_log.py	LLM_LOGS	Audit table; ON DELETE RESTRICT from TODO_LINES
Pydantic Schema Pattern (per resource)
Each schema file defines three classes:

*Create — required fields to create the resource
*Update — all fields Optional for partial PATCH
*Read — full representation returned by API, with model_config = {"from_attributes": True} (Pydantic v2)
Routes and Endpoints
GET/POST /todos, GET/DELETE /todos/{id}, GET /todos/{id}/lines
GET/POST /categories, PATCH/DELETE /categories/{id}, GET/PATCH /categories/{id}/streak
Guard: system categories (IS_SYSTEM=1) blocked from DELETE
GET/POST /game-runs, GET/PATCH /game-runs/{id}, GET /game-runs/{id}/tasks, GET /game-runs/{id}/scoring
GET/POST /tasks, GET/PATCH/DELETE /tasks/{id}, GET/POST /tasks/{id}/lines, PATCH/DELETE /tasks/{id}/lines/{line_id}
PATCH task_line to status=completed → sets COMPLETED_AT server-side + creates SCORING record in same transaction
GET/POST /scoring, GET/PATCH/DELETE /scoring/{id}, GET /scoring/details (queries SCORING_DETAILS view via text())
GET /llm-logs, GET/DELETE /llm-logs/{id} (read-only from API — pipeline writes via raw sqlite3)
Packages to Add to requirements.txt

fastapi==0.115.6
uvicorn[standard]==0.34.0
sqlalchemy==2.0.36
pydantic==2.10.4
python-dotenv==1.0.1
SQLAlchemy 2.0 style is required (DeclarativeBase, not legacy declarative_base()).
Pydantic v2 is required (from_attributes not orm_mode).

Run Command

uvicorn src.api.app:app --reload
From project root. Interactive docs at http://127.0.0.1:8000/docs.

Implementation Order (dependency-safe)
requirements.txt — add packages
src/models/base.py
src/models/todo.py, category.py, game_run.py
src/models/task.py (depends on game_run, todo, category)
src/models/scoring.py (depends on game_run, task)
src/models/llm_log.py (depends on todo)
src/models/__init__.py
src/api/dependencies.py
src/api/middleware.py
src/api/schemas/*.py
src/api/routes/*.py
src/api/app.py
src/api/__init__.py, routes/__init__.py, schemas/__init__.py
Verification
Install dependencies: pip install fastapi uvicorn[standard] sqlalchemy pydantic python-dotenv
Start server: uvicorn src.api.app:app --reload
Open http://127.0.0.1:8000/docs — confirm all routers appear
GET /categories → should return the 5 seeded system categories from db.sql
POST /game-runs → create a game run, note the returned game_run_id
GET /game-runs/{id} → confirm retrieval
PATCH /tasks/{id}/lines/{line_id} with status=completed → confirm SCORING record created in same transaction
GET /scoring/details → confirm SCORING_DETAILS view is queryable
Run process_input.py while API is running → confirm raw sqlite3 pipeline still works independently
