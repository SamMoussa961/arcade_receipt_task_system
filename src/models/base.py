import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_DIR = os.getenv("DB_DIR")
DB = os.getenv("DB")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / DB_DIR
DB_PATH = DATA_DIR / DB
DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"DATABASE_URL: {DATABASE_URL}")


engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
    )

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
