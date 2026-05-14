"""
backend/database.py

Configuração do engine SQLAlchemy e criação das tabelas.

Uso direto (criar tabelas):
    python -m backend.database

Uso no FastAPI (importar session):
    from backend.database import get_session
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.models import Base

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:suasenha@db:5432/mapa_lilas",
)

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session():
    """Dependency do FastAPI — uso: Depends(get_session)."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_tables() -> None:
    """Cria todas as tabelas definidas nos models. Idempotente: ignora tabelas que já existem."""
    print(f"[INFO] Conectando em: {DATABASE_URL.split('@')[-1]}")
    Base.metadata.create_all(bind=engine)
    print("[INFO] Tabelas criadas (ou já existentes):")
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename"
        ))
        for row in result:
            print(f"  ✓ {row[0]}")


if __name__ == "__main__":
    create_tables()