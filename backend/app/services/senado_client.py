"""
app/services/senado_client.py
"""

import logging
from typing import Any, Optional
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

CODIGOS_ASSUNTO = [130, 143]
SIGLAS_TIPO = ["PL", "PLP"]

# Dicionário de Cache em memória para não repetir requisições
_cache_senadores = {}

def _get(path: str, params: Optional[dict] = None) -> Optional[dict[str, Any]]:
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
    params: dict[str, Any] = {
        "termo": keyword,
        "codAssuntoEspecifico": codigo_assunto,
        "sigla": sigla_tipo,
    }
    if ano_inicial:
        params["anoMateria"] = ano_inicial
    if numdias:
        params["numdias"] = numdias

    return _get("/processo", params) or {}

def buscar_detalhe(cod_materia: int) -> Optional[dict[str, Any]]:
    return _get(f"/processo/{cod_materia}")

def buscar_movimentacoes(cod_materia: int) -> Optional[dict[str, Any]]:
    return _get(f"/processo/{cod_materia}/movimentacoes")

def buscar_senador(cod_parlamentar: int) -> Optional[dict[str, Any]]:
    """Busca detalhes de um senador, usando cache em memória."""
    cod_str = str(cod_parlamentar)
    if cod_str in _cache_senadores:
        return _cache_senadores[cod_str]
        
    raw = _get(f"/senador/{cod_str}")
    if not raw:
        return None
        
    _cache_senadores[cod_str] = raw
    return raw