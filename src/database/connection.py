"""Database connection helpers using SQLAlchemy.

Usage:
  - Set `DATABASE_URL` in your environment or `.env` (e.g. postgresql://user:pass@localhost:5432/mydb)
  - Import `engine`, `get_session`, or `execute_query` from this module.
"""
import os
from typing import Optional, Dict, List
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

# Prefer a full DATABASE_URL if provided. Otherwise build it safely from parts
raw_database_url = os.getenv("DATABASE_URL")
if raw_database_url and raw_database_url.strip() != "":
    DATABASE_URL = raw_database_url.replace("postgresql://", "postgresql+psycopg://")
else:
    db_user = os.getenv("DB_USER") or os.getenv("PGUSER") or "agente_user"
    db_password = os.getenv("DB_PASSWORD") or os.getenv("DB_PASS") or os.getenv("PGPASSWORD") or "agente3_84p"
    db_host = os.getenv("DB_HOST") or os.getenv("PGHOST") or "localhost"
    db_port = os.getenv("DB_PORT") or os.getenv("PGPORT") or "5432"
    db_name = os.getenv("DB_NAME") or os.getenv("PGDATABASE") or "midb"
    # percent-encode credentials to be URL-safe (handles % and other special chars)
    db_user_enc = quote_plus(db_user)
    db_password_enc = quote_plus(db_password)
    DATABASE_URL = f"postgresql+psycopg://{db_user_enc}:{db_password_enc}@{db_host}:{db_port}/{db_name}"

# Create a synchronous engine and session factory
engine = create_engine(DATABASE_URL, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session():
    """Return a new SQLAlchemy session. Use in a `with` block or manually close it."""
    return SessionLocal()


def execute_query(sql: str, params: Optional[Dict] = None) -> List[Dict]:
    """Execute a raw SQL query parametrized and return rows as list of dicts.

    WARNING: still rely on parametrized queries to avoid SQL injection.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            # Try to return rows as list of dicts when possible
            try:
                rows = [dict(row._mapping) for row in result]
            except Exception:
                rows = []
            return rows
    except SQLAlchemyError:
        raise
