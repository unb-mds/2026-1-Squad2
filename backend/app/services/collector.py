"""
app/services/collector.py

Orquestrador de coleta: coordena clientes HTTP → schemas → normalizer → banco.
"""

import asyncio
import logging
from datetime import date
from typing import Optional
import time
from sqlalchemy.orm import Session

from app import services  
from app.services import camara_client, senado_client
from app.services.normalizer import (
    upsert_autores_camara,
    upsert_autores_senado,
    upsert_pl_camara,
    upsert_pl_senado,
    upsert_tramitacoes_camara,
    upsert_tramitacoes_senado,
)

logger = logging.getLogger(__name__)

INTERVALO_HORAS = 2

# ---------------------------------------------------------------------------
# Câmara
# ---------------------------------------------------------------------------

def coletar_camara(session: Session, ano_inicial: Optional[int] = None) -> int:
    total = 0
    for sigla in camara_client.SIGLAS_TIPO:
        for kw in camara_client.PALAVRAS_CHAVE:
            logger.info("Câmara — coletando %s | keyword='%s'", sigla, kw)
            for item_raw in camara_client.listar_proposicoes(sigla, kw, ano_inicial):
                pl_id = item_raw.get("id")
                if not pl_id:
                    continue

                detalhe_raw = camara_client.buscar_detalhe(pl_id)
                id_salvo = upsert_pl_camara(session, item_raw, detalhe_raw, item_raw)
                if not id_salvo:
                    continue

                autores_raw = camara_client.buscar_autores(pl_id)
                
                # ENRIQUECIMENTO DE CACHE: Deputados
                for autor in autores_raw:
                    uri = autor.get("uri")
                    if uri and "/deputados/" in uri:
                        dep_id = uri.rstrip("/").split("/")[-1]
                        detalhes = camara_client.buscar_deputado(dep_id)
                        if detalhes:
                            autor["detalhes_deputado"] = detalhes
                            
                upsert_autores_camara(session, id_salvo, autores_raw)

                tramitacoes_raw = camara_client.buscar_tramitacoes(pl_id)
                upsert_tramitacoes_camara(session, id_salvo, tramitacoes_raw)

                session.commit()
                total += 1

    logger.info("Câmara — ciclo concluído. %d registros processados.", total)
    return total

# ---------------------------------------------------------------------------
# Senado
# ---------------------------------------------------------------------------

def coletar_senado(
    session: Session,
    ano_inicial: Optional[int] = None,
    numdias: Optional[int] = None,
) -> int:
    total = 0
    for sigla in senado_client.SIGLAS_TIPO:
        for kw in senado_client.PALAVRAS_CHAVE:
            for cod_assunto in senado_client.CODIGOS_ASSUNTO:
                logger.info(
                    "Senado — coletando %s | keyword='%s' | assunto=%d",
                    sigla, kw, cod_assunto,
                )
                raw = senado_client.pesquisar_materias(
                    keyword=kw,
                    codigo_assunto=cod_assunto,
                    sigla_tipo=sigla,
                    ano_inicial=ano_inicial,
                    numdias=numdias,
                )
                if isinstance(raw, list):
                    materias_raw = raw
                elif isinstance(raw, dict):
                    materias_raw = raw.get("Processos", raw.get("ListaProcessos", [raw]))
                else:
                    materias_raw = []
                
                if isinstance(materias_raw, dict):
                    materias_raw = [materias_raw]

                for item_raw in (materias_raw or []):
                    id_salvo = upsert_pl_senado(session, item_raw, item_raw)
                    if not id_salvo:
                        continue

                    detalhe_raw = senado_client.buscar_detalhe(id_salvo)
                    
                    if detalhe_raw:
                        # ENRIQUECIMENTO DE CACHE: Senadores
                        autores = detalhe_raw.get("autoriaIniciativa", []) or detalhe_raw.get("documento", {}).get("autoria", [])
                        if isinstance(autores, dict): autores = [autores]
                        
                        for autor in autores:
                            cod = autor.get("codigoParlamentar") or autor.get("CodigoParlamentar")
                            if cod:
                                detalhes = senado_client.buscar_senador(cod)
                                if detalhes:
                                    autor["detalhes_senador"] = detalhes

                        upsert_autores_senado(session, id_salvo, detalhe_raw)
                        upsert_tramitacoes_senado(session, id_salvo, detalhe_raw)

                    session.commit()
                    total += 1

    logger.info("Senado — ciclo concluído. %d registros processados.", total)
    return total

# ---------------------------------------------------------------------------
# Coleta incremental e Agendador
# ---------------------------------------------------------------------------

def executar_ciclo_incremental(session: Session) -> None:
    logger.info("Iniciando ciclo incremental — %s", date.today())
    try:
        coletar_camara(session)
    except Exception as exc:
        logger.warning("Falha no ciclo incremental da Câmara: %s", exc)
    try:
        coletar_senado(session, numdias=1)
    except Exception as exc:
        logger.warning("Falha no ciclo incremental do Senado: %s", exc)

async def loop_coleta(get_session_func) -> None:
    while True:
        await asyncio.sleep(INTERVALO_HORAS * 3600)
        logger.info("Agendador: disparando ciclo incremental.")
        try:
            await asyncio.to_thread(_ciclo_incremental_thread, get_session_func)
        except Exception as exc:
            logger.warning("Agendador: ciclo incremental falhou: %s", exc)

def _ciclo_incremental_thread(get_session_func) -> None:
    session: Session = next(get_session_func())
    try:
        executar_ciclo_incremental(session)
    finally:
        session.close()