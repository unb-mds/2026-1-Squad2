"""initial_schema

Revision ID: 001
Revises:
Create Date: 2025-01-01 00:00:00.000000

Cria todas as tabelas do Mapa L.I.L.A.S:
  - pls_senado
  - pls_camara
  - parlamentares
  - autoria_camara / autoria_senado
  - tramitacao_senado / tramitacao_camara  (RF05)

Índices para os padrões de filtro dos critérios de aceitação:
  - UF (mapa de calor)
  - data_apresentacao (filtro por período)
  - situacao/status (filtro por tramitação)
  - ementa (full-text search em português)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    # ── pls_senado ────────────────────────────────────────────────────────
    op.create_table(
        "pls_senado",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("codigo_materia", sa.Integer(), nullable=False),
        sa.Column("identificacao", sa.String(), nullable=False),
        sa.Column("data_apresentacao", sa.Date(), nullable=True),
        sa.Column("data_deliberacao", sa.Date(), nullable=True),
        sa.Column("ementa", sa.Text(), nullable=False),
        sa.Column("objetivo", sa.String(), nullable=True),
        sa.Column("tipo_documento", sa.String(), nullable=True),
        sa.Column("tramitando", sa.Boolean(), nullable=True),
        sa.Column("sigla_tipo_deliberacao", sa.String(), nullable=True),
        sa.Column("dados_raw", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_pls_senado_data_apresentacao", "pls_senado", ["data_apresentacao"])
    op.create_index("ix_pls_senado_tramitando", "pls_senado", ["tramitando"])
    op.create_index("ix_pls_senado_tipo_documento", "pls_senado", ["tipo_documento"])
    op.execute(
        "CREATE INDEX ix_pls_senado_ementa_fts ON pls_senado "
        "USING gin(to_tsvector('portuguese', ementa))"
    )

    # ── pls_camara ────────────────────────────────────────────────────────
    op.create_table(
        "pls_camara",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("numero", sa.Integer(), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=True),
        sa.Column("sigla_tipo", sa.String(), nullable=True),
        sa.Column("uri", sa.String(), nullable=True),
        sa.Column("data_apresentacao", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ementa", sa.Text(), nullable=False),
        sa.Column("descricao_tipo", sa.String(), nullable=True),
        sa.Column("descricao_situacao", sa.String(), nullable=True),
        sa.Column("despacho", sa.Text(), nullable=True),
        sa.Column("dados_raw", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_pls_camara_data_apresentacao", "pls_camara", ["data_apresentacao"])
    op.create_index("ix_pls_camara_descricao_situacao", "pls_camara", ["descricao_situacao"])
    op.create_index("ix_pls_camara_sigla_tipo", "pls_camara", ["sigla_tipo"])
    op.create_index("ix_pls_camara_ano", "pls_camara", ["ano"])
    op.execute(
        "CREATE INDEX ix_pls_camara_ementa_fts ON pls_camara "
        "USING gin(to_tsvector('portuguese', ementa))"
    )

    # ── parlamentares ─────────────────────────────────────────────────────
    op.create_table(
        "parlamentares",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("casa", sa.String(), nullable=False),
        sa.Column("nome_eleitoral", sa.String(), nullable=False),
        sa.Column("nome_civil", sa.String(), nullable=True),
        sa.Column("sigla_partido", sa.String(), nullable=False),
        sa.Column("sigla_uf", sa.String(2), nullable=True),
        sa.Column("sexo", sa.String(1), nullable=False),
        sa.Column("url_foto", sa.String(), nullable=True),
        sa.Column("status_mandato", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("casa IN ('Câmara', 'Senado')", name="ck_parlamentares_casa"),
        sa.CheckConstraint("sexo IN ('F', 'M')", name="ck_parlamentares_sexo"),
    )
    op.create_index("ix_parlamentares_sigla_uf", "parlamentares", ["sigla_uf"])
    op.create_index("ix_parlamentares_sexo", "parlamentares", ["sexo"])
    op.create_index("ix_parlamentares_casa", "parlamentares", ["casa"])

    # ── autoria_camara ────────────────────────────────────────────────────
    op.create_table(
        "autoria_camara",
        sa.Column("id_pl", sa.Integer(), nullable=False),
        sa.Column("id_parlamentar", sa.String(), nullable=False),
        sa.Column("tipo_autoria", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["id_pl"], ["pls_camara.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["id_parlamentar"], ["parlamentares.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id_pl", "id_parlamentar"),
    )
    op.create_index("ix_autoria_camara_id_parlamentar", "autoria_camara", ["id_parlamentar"])

    # ── autoria_senado ────────────────────────────────────────────────────
    op.create_table(
        "autoria_senado",
        sa.Column("id_pl", sa.Integer(), nullable=False),
        sa.Column("id_parlamentar", sa.String(), nullable=False),
        sa.Column("tipo_autoria", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["id_pl"], ["pls_senado.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["id_parlamentar"], ["parlamentares.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id_pl", "id_parlamentar"),
    )
    op.create_index("ix_autoria_senado_id_parlamentar", "autoria_senado", ["id_parlamentar"])

    # ── tramitacao_senado ─────────────────────────────────────────────────
    op.create_table(
        "tramitacao_senado",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_pl", sa.Integer(), nullable=False),
        sa.Column("data_tramitacao", sa.Date(), nullable=True),
        sa.Column("situacao", sa.String(), nullable=True),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("local", sa.String(), nullable=True),
        sa.Column("sequencia", sa.Integer(), nullable=True),
        sa.Column("dados_raw", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["id_pl"], ["pls_senado.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tramitacao_senado_id_pl", "tramitacao_senado", ["id_pl"])
    op.create_index("ix_tramitacao_senado_ordem", "tramitacao_senado", ["id_pl", "sequencia"])

    # ── tramitacao_camara ─────────────────────────────────────────────────
    op.create_table(
        "tramitacao_camara",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_pl", sa.Integer(), nullable=False),
        sa.Column("data_tramitacao", sa.DateTime(timezone=True), nullable=True),
        sa.Column("situacao", sa.String(), nullable=True),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("local", sa.String(), nullable=True),
        sa.Column("sequencia", sa.Integer(), nullable=True),
        sa.Column("dados_raw", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["id_pl"], ["pls_camara.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tramitacao_camara_id_pl", "tramitacao_camara", ["id_pl"])
    op.create_index("ix_tramitacao_camara_ordem", "tramitacao_camara", ["id_pl", "sequencia"])

    # ── Trigger: updated_at automático ────────────────────────────────────
    op.execute("""
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    for table in ("pls_senado", "pls_camara", "parlamentares"):
        op.execute(f"""
            CREATE TRIGGER trg_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        """)


def downgrade() -> None:
    for table in ("pls_senado", "pls_camara", "parlamentares"):
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table};")
    op.execute("DROP FUNCTION IF EXISTS set_updated_at();")

    op.drop_table("tramitacao_camara")
    op.drop_table("tramitacao_senado")
    op.drop_table("autoria_senado")
    op.drop_table("autoria_camara")
    op.drop_table("parlamentares")
    op.drop_table("pls_camara")
    op.drop_table("pls_senado")