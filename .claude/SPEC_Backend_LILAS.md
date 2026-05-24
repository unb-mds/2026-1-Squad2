# SPEC — Back End (L.I.L.A.S.)


> **Versão:** 2.0
> **Release:** Release 1
> **Responsável:** Equipe MDS 2026.1
> **Status:** Pronto para implementação


---


## 1. Visão Geral


O back end expõe uma REST API (FastAPI) para consumo pelo front end React. Os dados já estão armazenados no PostgreSQL — os endpoints abaixo consultam e retornam as proposições legislativas da Câmara dos Deputados e do Senado Federal de forma unificada.


> **Atenção:** os nomes dos campos da resposta JSON devem ser **exatamente** iguais aos definidos nesta spec. Qualquer divergência quebra os badges e filtros do front end.


---


## 2. Stack


| Componente | Tecnologia |
|---|---|
| Framework Web | FastAPI `[standard]` |
| Servidor ASGI | Uvicorn |
| ORM | SQLAlchemy |
| Driver PostgreSQL | psycopg2-binary |
| Migrações | Alembic |
| HTTP Client (ingestão) | requests `>=2.31.0` |


---


## 3. Estrutura de Pastas


```
backend/
├── app/
│   ├── __pycache__/
│   ├── migrations/
│   ├── schemas/
│   │   ├── camara.py
│   │   └── senado.py
│   ├── services/
│   │   ├── camara_client.py
│   │   ├── senado_client.py
│   │   ├── collector.py
│   │   └── normalizer.py
│   ├── .gitignore
│   ├── database.py
│   ├── main.py
│   └── models.py
├── .env
├── alembic.ini
├── dockerfile
├── entrypoint.sh
├── popular_banco.py
└── requirements.txt
```


---


## 3.1. Normalização de Status


A Câmara e o Senado retornam descrições de situação com textos variados. O `normalizer.py` é responsável por persistir os dados no banco — a normalização de status para o endpoint deve ser implementada **nesse mesmo arquivo**, como uma função auxiliar chamada no momento de montar a resposta da API.


### Contexto do `normalizer.py`


O arquivo já contém as funções de upsert que gravam PLs, autores e tramitações no banco. A função de normalização de status deve ser adicionada nele, seguindo o mesmo padrão já existente:


```python
# app/services/normalizer.py  (trecho relevante — adicionar ao final do arquivo)


def normalizar_status_camara(descricao_situacao: Optional[str]) -> str:
   """
   Converte descricao_situacao da Câmara nos 3 valores aceitos pelo front end.
   Usar no endpoint ao montar a resposta, não no upsert.
   """
   if not descricao_situacao:
       return "em_tramitacao"
   if descricao_situacao == "Transformado em Norma Jurídica":
       return "aprovado"
   if descricao_situacao == "Arquivada":
       return "arquivado"
   return "em_tramitacao"




def normalizar_status_senado(sigla_tipo_deliberacao: Optional[str], tramitando: Optional[bool]) -> str:
   """
   Converte sigla_tipo_deliberacao + tramitando do Senado nos 3 valores aceitos pelo front end.
   Usar no endpoint ao montar a resposta, não no upsert.
   """
   if sigla_tipo_deliberacao in ("AP", "SAN"):
       return "aprovado"
   if sigla_tipo_deliberacao in ("RETIRADO_PELO_AUTOR", "ARQUIVADO_FIM_LEGISLATURA"):
       return "arquivado"
   return "em_tramitacao"
```


### Tarefas


- [ ] Adicionar `normalizar_status_camara()` ao final de `normalizer.py`
- [ ] Adicionar `normalizar_status_senado()` ao final de `normalizer.py`
- [ ] Importar e usar essas funções no endpoint `GET /api/projetos-de-lei` ao montar cada item da resposta
- [ ] Importar e usar essas funções no endpoint `GET /api/projetos-de-lei/filtros` ao montar cada item da resposta


### Câmara (`descricao_situacao`)


| Valor normalizado | Texto exato retornado pela API da Câmara |
|---|---|
| `aprovado` | `"Transformado em Norma Jurídica"` |
| `arquivado` | `"Arquivada"` |
| `em_tramitacao` | Qualquer outro valor (inclusive nulo) |


### Senado (`sigla_tipo_deliberacao` + `tramitando`)


| Valor normalizado | Condição |
|---|---|
| `aprovado` | `sigla_tipo_deliberacao IN ('AP', 'SAN')` |
| `arquivado` | `sigla_tipo_deliberacao IN ('RETIRADO_PELO_AUTOR', 'ARQUIVADO_FIM_LEGISLATURA')` |
| `em_tramitacao` | Qualquer outro caso (inclusive nulo) |


### Casos de Borda


| Situação | Comportamento esperado |
|---|---|
| `descricao_situacao` é `None` ou vazio (Câmara) | Retornar `em_tramitacao` |
| `sigla_tipo_deliberacao` é `None` ou vazio (Senado) | Retornar `em_tramitacao` |
| Valor desconhecido não mapeado em nenhuma casa | Retornar `em_tramitacao` |
| PL do Senado com `tramitando = false` mas sem `sigla_tipo_deliberacao` | Retornar `em_tramitacao` (não inferir arquivado sem sigla explícita) |
| PL da Câmara com texto parcial como `"Arquivada por..."` | **Não** normalizar — só `"Arquivada"` exato vira `arquivado` |


> **Regra geral:** o que não for claramente `aprovado` ou `arquivado` deve ser classificado como `em_tramitacao`.


---
## 4. Modelagem do Banco de Dados


As tabelas já estão implementadas em `app/models.py`. Abaixo o resumo das entidades e seus papéis no contexto dos endpoints expostos.


### 4.1 Tabelas Principais


| Tabela | Casa | Campos-chave para a API |
|---|---|---|
| `pls_senado` | Senado Federal | `id`, `codigo_materia`, `identificacao`, `data_apresentacao`, `ementa`, `tramitando`, `updated_at` |
| `pls_camara` | Câmara dos Deputados | `id`, `numero`, `ano`, `sigla_tipo`, `data_apresentacao`, `ementa`, `descricao_situacao`, `updated_at` |
| `parlamentares` | Câmara + Senado | `id` (`cam_xxx` / `sen_xxx`), `nome_eleitoral`, `sigla_partido`, `sigla_uf`, `sexo` |
| `autoria_camara` | Câmara | `id_pl → pls_camara`, `id_parlamentar → parlamentares` |
| `autoria_senado` | Senado | `id_pl → pls_senado`, `id_parlamentar → parlamentares` |
| `tramitacao_camara` | Câmara | `id_pl`, `data_tramitacao`, `situacao`, `sequencia` |
| `tramitacao_senado` | Senado | `id_pl`, `data_tramitacao`, `situacao`, `sequencia` |


### 4.2 Mapeamento: campos do banco → resposta da API


O endpoint `GET /api/projetos-de-lei` retorna uma lista **unificada** das duas casas. O serviço executa um UNION das duas fontes, mapeando os campos conforme abaixo:


| Campo JSON (response) | Origem Câmara | Origem Senado |
|---|---|---|
| `id` | `"pl-" + pls_camara.id`+”-”+pls_camara.ano | `"pl-" + pls_senado.id’+”-”+pls_senado.ano |
| `numero` | `pls_camara.numero` | extraído de `pls_senado.identificacao` |
| `ano` | `pls_camara.ano` | extraído de `pls_senado.identificacao` |
| `casa` | `"CÂMARA DOS DEPUTADOS"` | `"SENADO FEDERAL"` |
| `status` | normalizar `pls_camara.descricao_situacao` | normalizar `pls_senado.tramitando` |
| `autor_nome` | `parlamentares.nome_eleitoral` via `autoria_camara` | `parlamentares.nome_eleitoral` via `autoria_senado` |
| `autor_partido` | `parlamentares.sigla_partido` | `parlamentares.sigla_partido` |
| `autor_uf` | `parlamentares.sigla_uf` | `parlamentares.sigla_uf` |
| `ementa` | `pls_camara.ementa` | `pls_senado.ementa` |
| `ultima_atualizacao` | SELECT MAX(data_tramitacao) FROM tramitacao_camara WHERE id_pl = :id
 | SELECT MAX(data_tramitacao) FROM tramitacao_senado WHERE id_pl = :id
|


## 5. Endpoints


### 5.1 `GET /api/projetos-de-lei`


Listagem paginada de proposições de ambas as casas, com filtros e ordenação.


#### Query Parameters


| Parâmetro | Tipo | Padrão | Obrigatório | Descrição |
|---|---|---|---|---|
| `page` | `int` | `1` | Não | Número da página |
| `per_page` | `int` | `10` | Não | Itens por página |
| `keyword` | `string` | — | Não | Busca em `numero` e `ementa` (case-insensitive) |
| `partido` | `string` | — | Não | Sigla do partido (ex: `MDB`) |
| `uf` | `string` | — | Não | Sigla do estado (ex: `MG`) |
| `status` | `string` | — | Não | `em_tramitacao`, `aprovado` ou `arquivado` |
| `ano` | `int` | — | Não | Ano do PL (ex: `2023`) |
| `ordenar` | `string` | `recentes` | Não | `recentes`, `antigos` ou `numero_asc` |


#### Exemplo de requisição


```
GET /api/projetos-de-lei?page=1&per_page=10&status=em_tramitacao&ordenar=recentes
```


#### Resposta 200 OK


```json
{
 "total": 145,
 "page": 1,
 "per_page": 10,
 "total_pages": 15,
 "projetos": [
   {
     "id": "pl-123-2023",
     "numero": "123",
     "ano": 2023,
     "casa": "Senado",
     "status": "em_tramitacao",
     "autor_nome": "Sen. Ana Soares",
     "autor_partido": "MDB",
     "autor_uf": "MG",
     "ementa": "Altera a Lei Maria da Penha para tipificar o monitoramento eletrônico do agressor em casos de risco de feminicídio.",
     "ultima_atualizacao": "2023-10-15"
   },
   {
     "id": "pl-1234-2022",
     "numero": "1234",
     "ano": 2022,
     "casa": "Senado",
     "status": "aprovado",
     "autor_nome": "Sen. Carlos Mendes",
     "autor_partido": "PL",
     "autor_uf": "RJ",
     "ementa": "Altera a Lei nº 11.340/2006 (Lei Maria da Penha) para determinar o uso obrigatório de tornozeleira eletrônica para agressores submetidos a medidas protetivas de urgência.",
     "ultima_atualizacao": "2023-09-02"
   }
 ]
}
```


#### ⚠️ Valores aceitos para campos críticos


Os campos abaixo devem conter **exatamente** esses valores — qualquer divergência quebra os badges e filtros do front end.


**`status`:**


| Valor | Descrição |
|---|---|
| `em_tramitacao` | PL em tramitação ou situação indefinida |
| `aprovado` | PL aprovado e transformado em norma |
| `arquivado` | PL arquivado |


**`casa`:**


| Valor |
|---|
| `SENADO FEDERAL` |
| `CÂMARA DOS DEPUTADOS` |


**`ultima_atualizacao`** — formato `YYYY-MM-DD` (ISO 8601). Deve ser buscada nas tabelas de tramitação, **não** no campo `updated_at` do PL, pois este pode estar desatualizado. A lógica é:


```sql
-- Câmara
SELECT MAX(data_tramitacao) FROM tramitacao_camara WHERE id_pl = :id


-- Senado
SELECT MAX(data_tramitacao) FROM tramitacao_senado WHERE id_pl = :id
```


Se não houver tramitações registradas, usar `pls_camara.updated_at` ou `pls_senado.updated_at` como fallback.


#### Ordenação


| Valor de `ordenar` | Comportamento |
|---|---|
| `recentes` (padrão) | Mais recentes primeiro (por `MAX(data_tramitacao)` DESC) |
| `antigos` | Mais antigos primeiro (por `MAX(data_tramitacao)` ASC) |
| `numero_asc` | Menor número primeiro |


#### Regras de negócio


- Filtros combinados são aplicados com `AND`.
- `keyword` busca em `ementa` e `numero` de ambas as casas (case-insensitive).
- Sem filtros, retorna todos os PLs paginados com `ordenar=recentes`.
- Sem resultados retorna `total=0` e `projetos=[]`.


---


### 5.2 `GET /api/projetos-de-lei/filtros`


Retorna os valores disponíveis para popular os dropdowns do front end. Não recebe parâmetros.


#### Resposta 200 OK


```json
{
 "partidos": ["MDB", "PL", "PSDB", "PT", "PDT"],
 "ufs": ["MG", "RJ", "PR", "SP", "BA"],
 "anos": [2021, 2022, 2023, 2024, 2025, 2026]
}
```


#### Regras de negócio


- `partidos`: siglas distintas de `parlamentares.sigla_partido`, ordenadas A→Z.
- `ufs`: siglas distintas de `parlamentares.sigla_uf` (excluindo nulos), ordenadas A→Z.
- `anos`: union dos anos de `pls_camara` e `pls_senado`, em ordem crescente.


---


## 6. Tratamento de Erros


| Situação | HTTP Status | Body |
|---|---|---|
| Parâmetro inválido | `422 Unprocessable Entity` | `{ "detail": [...] }` — padrão FastAPI |
| Erro interno | `500 Internal Server Error` | `{ "detail": "Erro interno. Tente novamente." }` |
| Banco indisponível | `503 Service Unavailable` | `{ "detail": "Serviço temporariamente indisponível." }` |


---


## 7. Critérios de Aceite — Release 1


- [ ] **AC-01** `GET /api/projetos-de-lei` retorna HTTP `200` com a estrutura de campos exata
- [ ] **AC-02** `keyword` busca em `ementa` e `numero` de ambas as casas
- [ ] **AC-03** Filtro por `status` retorna apenas PLs com o valor normalizado correto
- [ ] **AC-04** Filtros por `partido`, `uf` e `ano` funcionam isolados e combinados
- [ ] **AC-05** Paginação respeita `page` e `per_page`; `total_pages` calculado corretamente
- [ ] **AC-06** Ordenações `recentes`, `antigos` e `numero_asc` alteram a ordem dos resultados
- [ ] **AC-07** Requisição sem filtros retorna todos os PLs paginados (`total > 0`)
- [ ] **AC-08** `GET /api/projetos-de-lei/filtros` retorna `partidos`, `ufs` e `anos` não vazios
- [ ] **AC-09** Campo `status` contém apenas `em_tramitacao`, `aprovado` ou `arquivado`
- [ ] **AC-10** Campo `casa` contém apenas `Senado` ou `Câmara`
- [ ] **AC-11** Campo `ultima_atualizacao` vem de `MAX(data_tramitacao)` das tabelas de tramitação, serializado no formato `YYYY-MM-DD`
- [ ] **AC-12** CORS permite requisições do domínio do front end


---


*Este documento deve ser versionado junto ao repositório e atualizado sempre que houver mudanças no contrato de API.*



