import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration
DB_DIR = os.getenv("DB_DIR")
DB = os.getenv("DB")
SCHEMA = os.getenv("SCHEMA")
CONFIG_DIR = os.getenv("CONFIG_DIR")

# Calculate paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / DB_DIR
DB_PATH = DATA_DIR / DB
CONFIG_DIR = BASE_DIR / CONFIG_DIR
SCHEMA_PATH = CONFIG_DIR / SCHEMA


def get_connection():
    """
    Create and return a raw sqlite3 connection.
    Used by existing pipeline
    """
    return sqlite3.connect(DB_PATH)


def initialize_db():
    """
    Initialize the database by running the schema SQL script.
    Creates data directory and database file if they don't exist.
    """
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if database already exists
    if DB_PATH.exists():
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='CATEGORIES'"
            ).fetchone()
            if row:
                print(f"[INFO] Database already initialized at {DB_PATH}")
                return
    
    print(f"[INFO] Initializing new database at {DB_PATH}")
    
    # Check if schema file exists
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Schema file not found: {SCHEMA_PATH}\n"
            f"Please ensure {SCHEMA} exists in the data directory."
        )
    
    try:
        # Connect and execute schema
        with sqlite3.connect(DB_PATH) as conn:
            print(f"[INFO] Reading schema from {SCHEMA_PATH}")
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            
            print(f"[INFO] Executing schema SQL...")
            conn.executescript(schema_sql)
            conn.commit()
            
        print(f"[SUCCESS] Database initialized successfully!")
        print(f"[INFO] Tables created, triggers added, 5 categories seeded")
        
    except sqlite3.Error as e:
        print(f"[ERROR] Failed to initialize database: {e}")
        # Clean up partial database file
        if DB_PATH.exists():
            DB_PATH.unlink()
        raise


def reset_db():
    """
    Delete and recreate the database from scratch.
    """
    if DB_PATH.exists():
        print(f"[WARNING] Deleting existing database: {DB_PATH}")
        DB_PATH.unlink()
    
    initialize_db()


if __name__ == "__main__":
    # Allow running this script directly to initialize DB
    initialize_db()