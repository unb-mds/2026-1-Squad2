"""
app/database.py

Engine SQLAlchemy e factory de sessão para o Mapa L.I.L.A.S.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:suasenha@db:5432/mapa_lilas",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session():
    """FastAPI dependency — uso: session: Session = Depends(get_session)."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()