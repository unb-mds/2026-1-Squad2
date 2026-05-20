"""
app/routers/admin.py

Endpoints administrativos do Mapa L.I.L.A.S.
Não expostos publicamente — prefixo /admin.

POST /admin/coleta/historica
  Dispara carga histórica retroativa a partir de um ano-base configurável.
  Roda como BackgroundTask para não bloquear a resposta HTTP.
"""

import logging
from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_session
from app.services.collector import coletar_camara, coletar_senado

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])

ANO_MINIMO = 2006   # Lei Maria da Penha sancionada em 2006


class CargaHistoricaRequest(BaseModel):
    ano_base: int = Field(
        default=2015,
        ge=ANO_MINIMO,
        le=date.today().year,
        description="Ano a partir do qual a coleta retroativa será iniciada.",
    )
    apenas_camara: bool = False
    apenas_senado: bool = False


class CargaHistoricaResponse(BaseModel):
    status: str
    mensagem: str


def _executar_carga(ano_base: int, apenas_camara: bool, apenas_senado: bool, session: Session) -> None:
    """Função síncrona executada em background pelo FastAPI."""
    try:
        if not apenas_senado:
            logger.info("Carga histórica — Câmara desde %d", ano_base)
            for ano in range(ano_base, date.today().year + 1):
                coletar_camara(session, ano_inicial=ano)

        if not apenas_camara:
            logger.info("Carga histórica — Senado desde %d", ano_base)
            for ano in range(ano_base, date.today().year + 1):
                coletar_senado(session, ano_inicial=ano)

        logger.info("Carga histórica concluída.")
    except Exception as exc:
        logger.error("Carga histórica falhou: %s", exc)
    finally:
        session.close()


@router.post(
    "/coleta/historica",
    response_model=CargaHistoricaResponse,
    summary="Dispara carga histórica retroativa de PLs",
)
def iniciar_carga_historica(
    body: CargaHistoricaRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
) -> CargaHistoricaResponse:
    """
    Inicia a varredura retroativa de PLs a partir do ano_base informado.
    A coleta roda em background — a resposta é imediata.

    Atenção: para anos anteriores a 2015, o volume de requisições pode
    ser alto. Monitore os logs do servidor.
    """
    if body.apenas_camara and body.apenas_senado:
        raise HTTPException(
            status_code=400,
            detail="apenas_camara e apenas_senado não podem ser verdadeiros simultaneamente.",
        )

    background_tasks.add_task(
        _executar_carga,
        body.ano_base,
        body.apenas_camara,
        body.apenas_senado,
        session,
    )

    return CargaHistoricaResponse(
        status="iniciado",
        mensagem=f"Carga histórica a partir de {body.ano_base} iniciada em background. Acompanhe os logs.",
    )