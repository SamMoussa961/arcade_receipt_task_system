import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "arcade.db"
SCHEMA_PATH = DATA_DIR / "db.sql"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
