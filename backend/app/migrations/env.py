"""
app/migrations/env.py

Ponto de entrada do Alembic. Conecta o engine SQLAlchemy aos modelos
do projeto para que o Alembic saiba quais tabelas gerenciar.

Este arquivo é executado pelo Alembic toda vez que um comando de migração
é chamado (upgrade, downgrade, revision --autogenerate).
"""

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Importa Base para que autogenerate detecte todos os modelos registrados.
# O caminho funciona porque alembic.ini define prepend_sys_path = .
# (raiz do Backend/), então "app.models" resolve corretamente.
from app.models import Base

config = context.config

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError(
        "DATABASE_URL não definida. "
        "Verifique se o arquivo .env está presente e foi carregado pelo Docker Compose."
    )
config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Gera SQL puro sem conectar ao banco.
    Útil para revisar o que será executado antes de aplicar:

        alembic upgrade head --sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Conecta ao banco e aplica as migrações."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()