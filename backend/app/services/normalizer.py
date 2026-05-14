"""
app/services/normalizer.py

Camada de normalização: converte os payloads validados pelos schemas Pydantic
em registros planos prontos para o banco de dados.

Responsabilidades:
  - Flatten de estruturas aninhadas
  - Upsert (INSERT OR UPDATE) baseado no ID único — evita duplicatas (Constituição 3)
  - Garantir que parlamentar exista antes de inserir autoria
  - Garantir que PL exista antes de inserir tramitação
"""

import logging
from typing import Optional

from pydantic import ValidationError
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.models import (
    AutoriaCamara,
    AutoriaSenado,
    Parlamentar,
    PlCamara,
    PlSenado,
    TramitacaoCamara,
    TramitacaoSenado,
)
from app.schemas.camara import (
    CamaraAutoresResponse,
    CamaraDetalheResponse,
    CamaraProposicaoItem,
    CamaraTramitacoesResponse,
)
from app.schemas.senado import (
    SenadoDetalheEnvelope,
    SenadoListagemEnvelope,
    SenadoMovimentacoesEnvelope,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Câmara — Upsert de proposição
# ---------------------------------------------------------------------------

def upsert_pl_camara(
    session: Session,
    item_raw: dict,
    detalhe_raw: Optional[dict],
    dados_raw_original: dict,
) -> Optional[int]:
    """
    Valida e persiste um PL da Câmara. Retorna o ID ou None se inválido.
    Usa INSERT ... ON CONFLICT DO UPDATE para garantir idempotência (CA1).
    """
    try:
        item = CamaraProposicaoItem(**item_raw)
    except ValidationError as exc:
        logger.warning("Schema Câmara inválido (id=%s): %s", item_raw.get("id"), exc)
        return None

    detalhe_situacao = None
    detalhe_despacho = None
    descricao_tipo = None

    if detalhe_raw:
        try:
            detalhe = CamaraDetalheResponse(dados=detalhe_raw).dados
            descricao_tipo = detalhe.descricaoTipo
            if detalhe.statusProposicao:
                detalhe_situacao = detalhe.statusProposicao.descricaoSituacao
                detalhe_despacho = detalhe.statusProposicao.despacho
        except ValidationError as exc:
            logger.warning("Detalhe Câmara inválido (id=%s): %s", item.id, exc)

    stmt = pg_insert(PlCamara).values(
        id=item.id,
        numero=item.numero,
        ano=item.ano,
        sigla_tipo=item.siglaTipo,
        uri=item.uri,
        data_apresentacao=item.dataApresentacao,
        ementa=item.ementa,
        descricao_tipo=descricao_tipo,
        descricao_situacao=detalhe_situacao,
        despacho=detalhe_despacho,
        dados_raw=dados_raw_original,
    ).on_conflict_do_update(
        index_elements=["id"],
        set_={
            "descricao_situacao": detalhe_situacao,
            "despacho": detalhe_despacho,
            "dados_raw": dados_raw_original,
        },
    )
    session.execute(stmt)
    return item.id


def upsert_tramitacoes_camara(
    session: Session,
    id_pl: int,
    tramitacoes_raw: list[dict],
) -> None:
    """
    Insere tramitações novas da Câmara. Ignora as já existentes pela
    combinação (id_pl, sequencia).
    """
    try:
        parsed = CamaraTramitacoesResponse(dados=tramitacoes_raw)
    except ValidationError as exc:
        logger.warning("Tramitações Câmara inválidas (pl=%s): %s", id_pl, exc)
        return

    for t in parsed.dados:
        if t.sequencia is None:
            continue
        stmt = pg_insert(TramitacaoCamara).values(
            id_pl=id_pl,
            data_tramitacao=t.dataHora,
            situacao=t.descricaoSituacao,
            descricao=t.descricaoTramitacao,
            local=t.siglaOrgao,
            sequencia=t.sequencia,
            dados_raw=t.model_dump(),
        ).on_conflict_do_nothing()
        session.execute(stmt)


def upsert_autores_camara(
    session: Session,
    id_pl: int,
    autores_raw: list[dict],
) -> None:
    """
    Persiste parlamentares autores de um PL da Câmara.
    Garante que o parlamentar exista antes de inserir a autoria.
    """
    try:
        parsed = CamaraAutoresResponse(dados=autores_raw)
    except ValidationError as exc:
        logger.warning("Autores Câmara inválidos (pl=%s): %s", id_pl, exc)
        return

    for autor in parsed.dados:
        if not autor.uri:
            continue

        # Extrai o ID do deputado da URI (último segmento numérico)
        try:
            dep_id_str = autor.uri.rstrip("/").split("/")[-1]
            dep_id = int(dep_id_str)
        except (ValueError, IndexError):
            logger.warning("URI de autor inválida (pl=%s): %s", id_pl, autor.uri)
            continue

        parlamentar_id = f"cam_{dep_id}"

        # Upsert do parlamentar (mínimo — detalhes enriquecidos pelo coletor)
        stmt_parl = pg_insert(Parlamentar).values(
            id=parlamentar_id,
            casa="Câmara",
            nome_eleitoral=autor.nome,
            sigla_partido="",     # será atualizado pelo coletor de parlamentares
            sexo="M",             # será atualizado pelo coletor de parlamentares
        ).on_conflict_do_nothing()
        session.execute(stmt_parl)

        # Upsert da autoria
        stmt_aut = pg_insert(AutoriaCamara).values(
            id_pl=id_pl,
            id_parlamentar=parlamentar_id,
            tipo_autoria="Autor" if autor.proponente else "Coautor",
        ).on_conflict_do_nothing()
        session.execute(stmt_aut)


# ---------------------------------------------------------------------------
# Senado — Upsert de proposição
# ---------------------------------------------------------------------------

def upsert_pl_senado(
    session: Session,
    item_raw: dict,
    dados_raw_original: dict,
) -> Optional[int]:
    """
    Valida e persiste uma matéria do Senado. Retorna o id interno ou None.
    """
    try:
        envelope = SenadoListagemEnvelope(
            PesquisaBasicaMateria={"Materias": {"Materia": [item_raw]}}
        )
        if not envelope.materias:
            return None
        item = envelope.materias[0]
    except (ValidationError, Exception) as exc:
        logger.warning("Schema Senado inválido: %s", exc)
        return None

    if not item.ementa:
        logger.warning("Matéria Senado sem ementa (codMateria=%s) — ignorada.", item.codigo_materia)
        return None

    dados_basicos = item.DadosBasicosMateria

    stmt = pg_insert(PlSenado).values(
        id=item.codigo_materia,
        codigo_materia=item.codigo_materia,
        identificacao=item.identificacao or "",
        data_apresentacao=dados_basicos.DataApresentacaoMateria if dados_basicos else None,
        ementa=item.ementa,
        tipo_documento=item.IdentificacaoMateria.SiglaSubtipoMateria,
        tramitando=item.tramitando,
        dados_raw=dados_raw_original,
    ).on_conflict_do_update(
        index_elements=["id"],
        set_={
            "tramitando": item.tramitando,
            "dados_raw": dados_raw_original,
        },
    )
    session.execute(stmt)
    return item.codigo_materia


def upsert_tramitacoes_senado(
    session: Session,
    id_pl: int,
    movimentacoes_raw: dict,
) -> None:
    """Insere movimentações (tramitação) de uma matéria do Senado."""
    try:
        envelope = SenadoMovimentacoesEnvelope(**movimentacoes_raw)
    except (ValidationError, Exception) as exc:
        logger.warning("Movimentações Senado inválidas (pl=%s): %s", id_pl, exc)
        return

    for i, mov in enumerate(envelope.movimentacoes):
        seq = mov.SequenciaMovimentacao if mov.SequenciaMovimentacao is not None else i
        stmt = pg_insert(TramitacaoSenado).values(
            id_pl=id_pl,
            data_tramitacao=mov.DataMovimentacao,
            situacao=mov.DescricaoMovimentacao,
            descricao=mov.DescricaoMovimentacao,
            local=mov.DescricaoLocal,
            sequencia=seq,
            dados_raw=mov.model_dump(mode="json"),
        ).on_conflict_do_nothing()
        session.execute(stmt)


def upsert_autores_senado(
    session: Session,
    id_pl: int,
    detalhe_raw: dict,
) -> None:
    """Persiste autores de uma matéria do Senado a partir do detalhe."""
    try:
        envelope = SenadoDetalheEnvelope(**detalhe_raw)
        if not envelope.materia:
            return
        autores = envelope.materia.autores()
    except (ValidationError, Exception) as exc:
        logger.warning("Autores Senado inválidos (pl=%s): %s", id_pl, exc)
        return

    for autor in autores:
        cod = autor.codigo_parlamentar
        nome = autor.nome
        if not cod or not nome:
            continue

        parlamentar_id = f"sen_{cod}"
        stmt_parl = pg_insert(Parlamentar).values(
            id=parlamentar_id,
            casa="Senado",
            nome_eleitoral=nome,
            sigla_partido="",
            sexo="M",
        ).on_conflict_do_nothing()
        session.execute(stmt_parl)

        stmt_aut = pg_insert(AutoriaSenado).values(
            id_pl=id_pl,
            id_parlamentar=parlamentar_id,
            tipo_autoria="Autor",
        ).on_conflict_do_nothing()
        session.execute(stmt_aut)