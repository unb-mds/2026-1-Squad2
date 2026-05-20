"""
app/main.py

Ponto de entrada do FastAPI.
Registra o agendador de coleta incremental no evento de startup.
"""

import asyncio
import logging

from fastapi import FastAPI

from app.database import get_session
from app.routers import admin
from app.services.collector import loop_coleta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="Mapa L.I.L.A.S",
    description="API para coleta e consulta de proposições legislativas sobre feminicídio.",
    version="0.1.0",
)

app.include_router(admin.router)


@app.on_event("startup")
async def startup_agendador() -> None:
    """
    Inicia o loop de coleta incremental em background ao subir o servidor.
    O primeiro ciclo só roda após INTERVALO_HORAS (2h) — não no boot.
    Para popular o banco imediatamente, use POST /admin/coleta/historica.
    """
    asyncio.create_task(loop_coleta(get_session))


@app.get("/", include_in_schema=False)
def health_check():
    return {"status": "ok"}