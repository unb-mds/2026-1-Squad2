"""
app/services/senado_client.py

Cliente HTTP para a API de Dados Abertos do Senado Federal.
Responsabilidade exclusiva: fazer requisições e retornar JSON bruto.

Base URL: https://legis.senado.leg.br/dadosabertos
"""

import logging
from typing import Any, Iterator, Optional

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://legis.senado.leg.br/dadosabertos"
TIMEOUT = 30

PALAVRAS_CHAVE = [
    "feminicídio",
    "violência doméstica",
    "direitos da mulher",
    "mulher",
]

# Códigos de assunto geral do Senado para afunilar a busca (spec)
CODIGOS_ASSUNTO = [130, 143]   # 130 = Direito Penal, 143 = Direitos Humanos/Minorias

SIGLAS_TIPO = ["PL", "PLP"]


def _get(path: str, params: Optional[dict] = None) -> Optional[dict[str, Any]]:
    """
    Faz GET na API do Senado requisitando JSON.
    Retorna None em caso de falha (resiliência — CA5).
    """
    url = f"{BASE_URL}/{path.lstrip('/')}"
    headers = {"Accept": "application/json"}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as exc:
        logger.warning("Senado API indisponível [%s]: %s", url, exc)
        return None


def pesquisar_materias(
    keyword: str,
    codigo_assunto: int,
    sigla_tipo: str,
    ano_inicial: Optional[int] = None,
    numdias: Optional[int] = None,
) -> dict[str, Any]:
    """
    Busca matérias pelo endpoint de pesquisa básica.

    - Para carga histórica: passa ano_inicial, itera anos externamente.
    - Para coleta incremental: passa numdias=1 (spec CA1).

    Retorna o JSON bruto para validação posterior pelo schema Pydantic.
    """
    params: dict[str, Any] = {
        "palavraChave": keyword,
        "codigoAssuntoGeral": codigo_assunto,
        "sigla": sigla_tipo,
    }
    if ano_inicial:
        params["anoMateria"] = ano_inicial
    if numdias:
        params["numdias"] = numdias

    return _get("/materia/pesquisa/lista", params) or {}


def buscar_detalhe(cod_materia: int) -> Optional[dict[str, Any]]:
    """Retorna JSON bruto do endpoint de detalhe de uma matéria."""
    return _get(f"/materia/{cod_materia}")


def buscar_movimentacoes(cod_materia: int) -> Optional[dict[str, Any]]:
    """Retorna JSON bruto das movimentações (tramitação) de uma matéria."""
    return _get(f"/materia/{cod_materia}/movimentacoes")