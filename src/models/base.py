import os
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration with validation
DB_DIR = os.getenv("DB_DIR")
DB = os.getenv("DB")

if not DB_DIR or not DB:
    raise ValueError(
        "Missing required environment variables. "
        "Please set DB_DIR and DB in .env file"
    )

# Calculate paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / DB_DIR
DB_PATH = DATA_DIR / DB
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Debug output
print(f"[INFO] Database directory: {DATA_DIR}")
print(f"[INFO] Database path: {DB_PATH}")
print(f"[INFO] Database exists: {DB_PATH.exists()}")
print(f"[INFO] Database URL: {DATABASE_URL}")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
class Base(DeclarativeBase):
    pass