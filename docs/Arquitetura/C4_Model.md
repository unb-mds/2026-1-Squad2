# 🏗️ Modelagem C4

Esta seção aprofunda o nível de zoom da nossa arquitetura, detalhando como o sistema está quebrado em Containers (aplicações) e quais são seus Componentes internos.

---

## 1. Level 2 — Diagrama de Containers

### 1.1 Frontend Web
| Propriedade | Valor |
|---|---|
| **Tecnologia** | React + Tailwind CSS |
| **Protocolo** | HTTP (navegador do usuário) -> HTTP/REST (Backend API) |
| **Responsabilidades** | Renderização das páginas, busca de PLs, exibição de cards, filtros e alertas |
| **Porta padrão** | 3000 (dev) / 80 ou 443 (prod) |

### 1.2 Backend API
| Propriedade | Valor |
|---|---|
| **Tecnologia** | Python + FastAPI |
| **Protocolo** | HTTP/REST (Frontend) -> HTTP/REST (Sistemas Externos) e SQL (PostgreSQL) |
| **Responsabilidades** | Orquestração das consultas, normalização dos dados, classificação NLP, persistência |
| **Porta padrão** | 8000 |

### 1.3 Banco de Dados
| Propriedade | Valor |
|---|---|
| **Tecnologia** | PostgreSQL |
| **Protocolo** | SQL |
| **Responsabilidades** | Persistência de PLs, parlamentares, usuários, alertas e histórico de buscas |
| **Porta padrão** | 5432 |

### 2.4 Orquestração e Infraestrutura (Docker)
| Propriedade | Valor |
|---|---|
| **Tecnologia** | Docker e Docker Compose |
| **Responsabilidades** | Isolar o Frontend, Backend e Banco de Dados em ambientes containerizados independentes, mapeando portas e orquestrando o fluxo de subida do projeto via `docker-compose.yml`. |

---

## 2. Level 3 — Diagrama de Componentes

### 2.1 Frontend Web Application

| Componente | Tipo | Responsabilidade |
|---|---|---|
| `PáginaPrincipal` | React Component | Página raiz — orquestra busca e renderização dos resultados |
| `SearchForm` | React Component | Formulário de busca com termos, filtros de data, tipo e status |
| `PLCard` | React Component | Card individual de um PL com info de tramitação e metadados |
| `Header` | React (Tagmus) | Cabeçalho com logo, menu e dados de navegação |
| `InstPL Search` | Cortex/NLP | Busca semântica de PLs por termos e relevância |
| `AtomicComponents` | Frontend | Biblioteca de componentes UI reutilizáveis (Button, Input, Badge) |
| `Types & Constants` | Frontend | Contratos de dados: DTOs, enums de status, temas, filtros |

### 2.2 Backend API Application (Python + FastAPI)

| Componente | Tipo | Responsabilidade |
|---|---|---|
| `Routers / API` | API Core | Camada de rotas (`/app/routers`) que serve os dados do banco para o Frontend |
| `ETL Collector` | App Service | Script/Cron (`popular_banco.py`, `collector.py`) que orquestra a busca nos governos |
| `CamaraApiClient` | API Client | Realiza chamadas HTTP para extrair projetos da Câmara dos Deputados |
| `SenadoApiClient` | API Client | Realiza chamadas HTTP para extrair projetos do Senado Federal |
| `Normalizer` | Component | Limpa, padroniza e trata chaves duplicadas/encodings dos dados brutos do governo |
| `FilterParams` | Pydantic Model | Valida e parseia parâmetros de filtro solicitados pelo Frontend |
| `PostgreSQL Db` | Database | Única fonte da verdade do sistema, servindo respostas instantâneas ao Frontend |
