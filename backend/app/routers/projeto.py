from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, or_, cast, String, Integer, null, Boolean
from app.database import get_db
from app.models import (
    PlCamara, PlSenado, Parlamentar, AutoriaCamara, AutoriaSenado,
    TramitacaoCamara, TramitacaoSenado
)
from app.services.normalizer import normalizar_status_camara, normalizar_status_senado
import math

router = APIRouter(prefix="/api/projetos-de-lei")

@router.get("")
def listar_projetos(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    keyword: str = None,
    partido: str = None,
    uf: str = None,
    status: str = None,
    ano: int = None,
    ordenar: str = Query("recentes")
):
    # 1. Subqueries para a última atualização (Otimização de Performance)
    subq_camara = (
        select(TramitacaoCamara.id_pl, func.max(TramitacaoCamara.data_tramitacao).label("ultima_atualizacao"))
        .group_by(TramitacaoCamara.id_pl)
        .subquery()
    )
    
    subq_senado = (
        select(TramitacaoSenado.id_pl, func.max(TramitacaoSenado.data_tramitacao).label("ultima_atualizacao"))
        .group_by(TramitacaoSenado.id_pl)
        .subquery()
    )

    # 2. Query Base da Câmara
    query_camara = (
        select(
            func.cast(PlCamara.id, String).label("raw_id"),
            func.cast(PlCamara.numero, String).label("numero"),
            PlCamara.ano.label("ano"), # Geralmente já é Integer no banco
            func.cast("CÂMARA DOS DEPUTADOS", String).label("casa"),
            func.cast(PlCamara.descricao_situacao, String).label("raw_status"),
            PlCamara.ementa.label("ementa"),
            Parlamentar.nome_eleitoral.label("autor_nome"),
            Parlamentar.sigla_partido.label("autor_partido"),
            Parlamentar.sigla_uf.label("autor_uf"),
            func.coalesce(subq_camara.c.ultima_atualizacao, PlCamara.updated_at).label("ultima_atualizacao"),
            # Campos extras para manter compatibilidade no union caso necessário
            func.cast(null(), String).label("senado_sigla_deliberacao"),
            func.cast(null(), Boolean).label("senado_tramitando")
        )
        .outerjoin(subq_camara, subq_camara.c.id_pl == PlCamara.id)
        .outerjoin(AutoriaCamara, AutoriaCamara.id_pl == PlCamara.id)
        .outerjoin(Parlamentar, Parlamentar.id == AutoriaCamara.id_parlamentar)
    )

    # 3. Query Base do Senado
    numero_senado = func.split_part(func.replace(PlSenado.identificacao, "PL ", ""), "/", 1)
    ano_senado = func.split_part(func.replace(PlSenado.identificacao, "PL ", ""), "/", 2)

    query_senado = (
        select(
            func.cast(PlSenado.id, String).label("raw_id"),
            func.cast(numero_senado, String).label("numero"),
            func.cast(ano_senado, Integer).label("ano"), # Forçando Integer para bater com a Câmara
            func.cast("SENADO FEDERAL", String).label("casa"),
            func.cast(null(), String).label("raw_status"), # null() ao invés de None solto
            PlSenado.ementa.label("ementa"),
            Parlamentar.nome_eleitoral.label("autor_nome"),
            Parlamentar.sigla_partido.label("autor_partido"),
            Parlamentar.sigla_uf.label("autor_uf"),
            func.coalesce(subq_senado.c.ultima_atualizacao, PlSenado.updated_at).label("ultima_atualizacao"),
            func.cast(PlSenado.sigla_tipo_deliberacao, String).label("senado_sigla_deliberacao"),
            func.cast(PlSenado.tramitando, Boolean).label("senado_tramitando")
        )
        .outerjoin(subq_senado, subq_senado.c.id_pl == PlSenado.id)
        .outerjoin(AutoriaSenado, AutoriaSenado.id_pl == PlSenado.id)
        .outerjoin(Parlamentar, Parlamentar.id == AutoriaSenado.id_parlamentar)
    )

    # 4. UNION ALL
    query_unificada = query_camara.union_all(query_senado).subquery()
    
    final_query = select(query_unificada)

    # 5. Aplicação de Filtros
    if keyword:
        termo = f"%{keyword}%"
        final_query = final_query.where(
            or_(
                query_unificada.c.ementa.ilike(termo),
                query_unificada.c.numero.ilike(termo)
            )
        )
    if partido:
        final_query = final_query.where(query_unificada.c.autor_partido == partido)
    if uf:
        final_query = final_query.where(query_unificada.c.autor_uf == uf)
    if ano:
        final_query = final_query.where(query_unificada.c.ano == ano)

    # 6. Ordenação
    if ordenar == "recentes":
        final_query = final_query.order_by(query_unificada.c.ultima_atualizacao.desc())
    elif ordenar == "antigos":
        final_query = final_query.order_by(query_unificada.c.ultima_atualizacao.asc())
    elif ordenar == "numero_asc":
        # Fazendo cast para Integer apenas na hora de ordenar, para o "2" vir antes do "10"
        final_query = final_query.order_by(cast(query_unificada.c.numero, Integer).asc())

    # 7. Execução e Paginação
    total_items = db.execute(select(func.count()).select_from(final_query.subquery())).scalar()
    
    offset = (page - 1) * per_page
    final_query = final_query.offset(offset).limit(per_page)
    
    resultados = db.execute(final_query).fetchall()

    # 8. Montagem do Payload de Resposta
    projetos = []
    for row in resultados:
        if row.casa == "CÂMARA DOS DEPUTADOS":
            status_final = normalizar_status_camara(row.raw_status)
        else:
            status_final = normalizar_status_senado(row.senado_sigla_deliberacao, row.senado_tramitando)
            
        if status and status_final != status:
            continue
            
        projetos.append({
            "id": f"pl-{row.numero}-{row.ano}",
            "numero": str(row.numero),
            "ano": int(row.ano) if row.ano else None,
            "casa": row.casa,
            "status": status_final,
            "autor_nome": row.autor_nome,
            "autor_partido": row.autor_partido,
            "autor_uf": row.autor_uf,
            "ementa": row.ementa,
            "ultima_atualizacao": row.ultima_atualizacao.strftime("%Y-%m-%d") if row.ultima_atualizacao else None
        })

    if status:
        total_items = len(projetos)

    return {
        "total": total_items,
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(total_items / per_page) if total_items else 0,
        "projetos": projetos
    }

@router.get("/filtros")
def listar_filtros(db: Session = Depends(get_db)):
    # Busca Partidos (excluindo nulos e strings vazias)
    partidos_query = db.query(Parlamentar.sigla_partido).filter(
        Parlamentar.sigla_partido.isnot(None), 
        Parlamentar.sigla_partido != ""
    ).distinct().order_by(Parlamentar.sigla_partido).all()
    
    # Busca UFs (excluindo nulos e strings vazias)
    ufs_query = db.query(Parlamentar.sigla_uf).filter(
        Parlamentar.sigla_uf.isnot(None), 
        Parlamentar.sigla_uf != ""
    ).distinct().order_by(Parlamentar.sigla_uf).all()
    
    # Busca Anos (Câmara - Campo Inteiro)
    anos_camara = db.query(PlCamara.ano).filter(PlCamara.ano.isnot(None)).distinct().all()
    anos_set = {ano[0] for ano in anos_camara}
    
    # Busca Anos (Senado - Extraindo da string 'PL 648/2019')
    identificacoes_senado = db.query(PlSenado.identificacao).filter(PlSenado.identificacao.isnot(None)).all()
    for id_senado in identificacoes_senado:
        texto = id_senado[0]  # Ex: "PL 648/2019"
        if "/" in texto:
            try:
                ano_str = texto.split("/")[-1].strip()
                anos_set.add(int(ano_str))
            except ValueError:
                continue
                
    # Ordena a lista de anos gerada
    anos_lista = sorted(list(anos_set))
    
    return {
        "partidos": [p[0] for p in partidos_query],
        "ufs": [u[0] for u in ufs_query],
        "anos": anos_lista
    }