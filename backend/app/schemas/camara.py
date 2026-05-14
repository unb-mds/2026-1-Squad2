"""
app/schemas/camara.py

Modelos Pydantic para validação dos payloads da API da Câmara dos Deputados.

Critério de aceitação 3: validação obrigatória do schema antes de persistir.
Se os nós vitais mudarem de lugar, o modelo lança ValidationError,
interrompendo apenas aquele registro — não o job inteiro.

Endpoints cobertos:
  GET /proposicoes                    → CamaraProposicaoItem (listagem)
  GET /proposicoes/{id}               → CamaraProposicaoDetalhe
  GET /proposicoes/{id}/autores       → CamaraAutorItem
  GET /proposicoes/{id}/tramitacoes   → CamaraTramitacaoItem
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Listagem — GET /proposicoes
# ---------------------------------------------------------------------------

class CamaraProposicaoItem(BaseModel):
    """Item retornado na listagem paginada de proposições."""

    id: int
    uri: Optional[str] = None
    siglaTipo: str
    numero: int
    ano: int
    ementa: str
    dataApresentacao: Optional[datetime] = None

    @field_validator("ementa")
    @classmethod
    def ementa_nao_vazia(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Campo 'ementa' não pode ser vazio.")
        return v.strip()


class CamaraListagemResponse(BaseModel):
    """Envelope da listagem paginada."""

    dados: list[CamaraProposicaoItem] = Field(default_factory=list)
    links: list[dict[str, Any]] = Field(default_factory=list)

    def proxima_pagina(self) -> Optional[str]:
        """Retorna a URL da próxima página ou None se não houver."""
        for link in self.links:
            if link.get("rel") == "next":
                return link.get("href")
        return None


# ---------------------------------------------------------------------------
# Status atual de tramitação (campo aninhado no detalhe)
# ---------------------------------------------------------------------------

class CamaraStatusProposicao(BaseModel):
    descricaoSituacao: Optional[str] = None
    despacho: Optional[str] = None
    dataHora: Optional[datetime] = None
    siglaOrgao: Optional[str] = None


# ---------------------------------------------------------------------------
# Detalhe — GET /proposicoes/{id}
# ---------------------------------------------------------------------------

class CamaraProposicaoDetalhe(BaseModel):
    """Payload do endpoint de detalhe de uma proposição."""

    id: int
    uri: Optional[str] = None
    siglaTipo: Optional[str] = None
    numero: Optional[int] = None
    ano: Optional[int] = None
    ementa: str
    dataApresentacao: Optional[datetime] = None
    descricaoTipo: Optional[str] = None
    statusProposicao: Optional[CamaraStatusProposicao] = None

    @field_validator("ementa")
    @classmethod
    def ementa_nao_vazia(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Campo 'ementa' não pode ser vazio.")
        return v.strip()


class CamaraDetalheResponse(BaseModel):
    dados: CamaraProposicaoDetalhe


# ---------------------------------------------------------------------------
# Autores — GET /proposicoes/{id}/autores
# ---------------------------------------------------------------------------

class CamaraAutorItem(BaseModel):
    uri: Optional[str] = None
    nome: str
    tipo: Optional[str] = None
    ordemAssinatura: Optional[int] = None
    proponente: Optional[int] = None


class CamaraAutoresResponse(BaseModel):
    dados: list[CamaraAutorItem] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Tramitações — GET /proposicoes/{id}/tramitacoes
# ---------------------------------------------------------------------------

class CamaraTramitacaoItem(BaseModel):
    sequencia: Optional[int] = None
    dataHora: Optional[datetime] = None
    descricaoSituacao: Optional[str] = None
    descricaoTramitacao: Optional[str] = None
    siglaOrgao: Optional[str] = None
    despacho: Optional[str] = None


class CamaraTramitacoesResponse(BaseModel):
    dados: list[CamaraTramitacaoItem] = Field(default_factory=list)