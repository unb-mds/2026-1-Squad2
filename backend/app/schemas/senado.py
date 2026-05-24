"""
app/schemas/senado.py

Modelos Pydantic para validação dos payloads da API do Senado Federal.

A API do Senado retorna estruturas profundamente aninhadas. Os validators
aqui "achatam" os dados em objetos planos antes de passá-los ao normalizer.

Endpoints cobertos:
  GET /materia/pesquisa/lista     → SenadoMateriaItem (listagem)
  GET /materia/{codMateria}       → SenadoMateriaDetalhe
  GET /materia/{codMateria}/movimentacoes → SenadoMovimentacaoItem
"""

from datetime import date
from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------------------------
# Identificação da matéria (presente em listagem e detalhe)
# ---------------------------------------------------------------------------

class SenadoIdentificacaoMateria(BaseModel):
    CodigoMateria: str
    SiglaSubtipoMateria: Optional[str] = None
    NumeroMateria: Optional[str] = None
    AnoMateria: Optional[str] = None
    DescricaoIdentificacaoMateria: Optional[str] = None      # "PL 2325/2021"


# ---------------------------------------------------------------------------
# Dados básicos da matéria
# ---------------------------------------------------------------------------

class SenadoDadosBasicos(BaseModel):
    EmentaMateria: Optional[str] = None
    DataApresentacaoMateria: Optional[date] = None
    IndicadorTramitando: Optional[str] = None                # "Sim" | "Não"


# ---------------------------------------------------------------------------
# Autor individual (estrutura dentro de AutoriaMateria)
# ---------------------------------------------------------------------------

class SenadoAutorItem(BaseModel):
    NomeAutor: Optional[str] = None
    IdentificacaoParlamentar: Optional[dict[str, Any]] = None

    @property
    def nome(self) -> Optional[str]:
        if self.NomeAutor:
            return self.NomeAutor
        if self.IdentificacaoParlamentar:
            return self.IdentificacaoParlamentar.get("NomeParlamentar")
        return None

    @property
    def codigo_parlamentar(self) -> Optional[str]:
        if self.IdentificacaoParlamentar:
            return self.IdentificacaoParlamentar.get("CodigoParlamentar")
        return None


# ---------------------------------------------------------------------------
# Listagem — GET /materia/pesquisa/lista
# ---------------------------------------------------------------------------

class SenadoMateriaItem(BaseModel):
    """
    Item da pesquisa básica do Senado.
    A API retorna um envelope com vários níveis de nesting:
    PesquisaBasicaMateria > Materias > Materia[]
    """

    IdentificacaoMateria: SenadoIdentificacaoMateria
    DadosBasicosMateria: Optional[SenadoDadosBasicos] = None

    @property
    def codigo_materia(self) -> int:
        return int(self.IdentificacaoMateria.CodigoMateria)

    @property
    def identificacao(self) -> Optional[str]:
        return self.IdentificacaoMateria.DescricaoIdentificacaoMateria

    @property
    def ementa(self) -> Optional[str]:
        if self.DadosBasicosMateria:
            return self.DadosBasicosMateria.EmentaMateria
        return None

    @property
    def tramitando(self) -> bool:
        if self.DadosBasicosMateria:
            return self.DadosBasicosMateria.IndicadorTramitando == "Sim"
        return False


class SenadoListagemEnvelope(BaseModel):
    """
    Envelope raiz da listagem:
    { "PesquisaBasicaMateria": { "Materias": { "Materia": [...] } } }
    A API pode retornar um objeto único quando há só 1 resultado.
    """

    materias: list[SenadoMateriaItem] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def extrair_materias(cls, data: Any) -> Any:
        try:
            raw = (
                data
                .get("PesquisaBasicaMateria", {})
                .get("Materias", {})
                .get("Materia", [])
            )
            # API retorna dict (1 item) ou list (múltiplos)
            if isinstance(raw, dict):
                raw = [raw]
            return {"materias": raw or []}
        except (AttributeError, TypeError):
            return {"materias": []}


# ---------------------------------------------------------------------------
# Detalhe — GET /materia/{codMateria}
# ---------------------------------------------------------------------------

class SenadoMateriaDetalhe(BaseModel):
    """
    Estrutura do endpoint de detalhe:
    DetalheMateria > Materia > { IdentificacaoMateria, DadosBasicosMateria,
                                  AutoriaMateria, SituacaoAtual }
    """

    IdentificacaoMateria: SenadoIdentificacaoMateria
    DadosBasicosMateria: Optional[SenadoDadosBasicos] = None
    AutoriaMateria: Optional[dict[str, Any]] = None
    SituacaoAtual: Optional[dict[str, Any]] = None

    def autores(self) -> list[SenadoAutorItem]:
        """Extrai e normaliza a lista de autores do campo aninhado."""
        if not self.AutoriaMateria:
            return []
        raw = self.AutoriaMateria.get("Autor", [])
        if isinstance(raw, dict):
            raw = [raw]
        result = []
        for a in raw:
            try:
                result.append(SenadoAutorItem(**a))
            except Exception:
                pass
        return result

    def situacao_atual(self) -> Optional[str]:
        """Extrai descrição da situação atual de dentro de SituacaoAtual."""
        if not self.SituacaoAtual:
            return None
        return (
            self.SituacaoAtual
            .get("Autuacoes", {})
            .get("Autuacao", {})
            .get("SituacaoAtual", {})
            .get("DescricaoSituacao")
        )


class SenadoDetalheEnvelope(BaseModel):
    materia: Optional[SenadoMateriaDetalhe] = None

    @model_validator(mode="before")
    @classmethod
    def extrair_materia(cls, data: Any) -> Any:
        try:
            m = data.get("DetalheMateria", {}).get("Materia", None)
            return {"materia": m}
        except (AttributeError, TypeError):
            return {"materia": None}


# ---------------------------------------------------------------------------
# Movimentações (tramitação) — GET /materia/{codMateria}/movimentacoes
# ---------------------------------------------------------------------------

class SenadoMovimentacaoItem(BaseModel):
    DescricaoMovimentacao: Optional[str] = None
    DataMovimentacao: Optional[date] = None
    DescricaoLocal: Optional[str] = None
    SequenciaMovimentacao: Optional[int] = None


class SenadoMovimentacoesEnvelope(BaseModel):
    movimentacoes: list[SenadoMovimentacaoItem] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def extrair_movimentacoes(cls, data: Any) -> Any:
        try:
            raw = (
                data
                .get("MovimentacaoMateria", {})
                .get("Materia", {})
                .get("Movimentacoes", {})
                .get("Movimentacao", [])
            )
            if isinstance(raw, dict):
                raw = [raw]
            return {"movimentacoes": raw or []}
        except (AttributeError, TypeError):
            return {"movimentacoes": []}