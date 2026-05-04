# Arquitetura Técnica — Mapa L.I.L.A.S

> **Mapa Legislativo Informativo de Leis de Acompanhamento Social**
> Buscador de projetos de lei sobre feminicídio, violência doméstica e direitos da mulher. Plataforma para busca e acompanhamento de projetos de lei sobre feminicídio e visualização de gráficos sobre o assunto.

---

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Level 1 — Mapa do Sistema](#2-level-1--mapa-do-sistema)
3. [Level 2 — Diagrama de Containers](#3-level-2--diagrama-de-containers)
4. [Level 3 — Diagrama de Componentes](#4-level-3--diagrama-de-componentes)
5. [Stack Tecnológica](#5-stack-tecnológica)
6. [Decisões Arquiteturais (ADRs)](#6-decisões-arquiteturais-adrs)
7. [Considerações de Segurança](#7-considerações-de-segurança)
8. [Escalabilidade e Observabilidade](#8-escalabilidade-e-observabilidade)

---

## 1. Visão Geral

O **Mapa L.I.L.A.S** é uma aplicação web para busca e acompanhamento de projetos de lei sobre feminicídio, violência doméstica e direitos da mulher, com visualização de gráficos sobre o assunto. Os dados provêm das APIs públicas do Senado Federal e da Câmara dos Deputados, tornando a informação legislativa acessível, pesquisável e visual para jornalistas, pesquisadores e cidadãos.

### Objetivos Arquiteturais

| Atributo           | Meta                                                                 |
|--------------------|----------------------------------------------------------------------|
| **Disponibilidade**| Alta disponibilidade do frontend e da API                            |
| **Manutenibilidade**| Separação clara entre frontend, backend e dados                     |
| **Extensibilidade**| Facilidade para adicionar novas fontes legislativas                  |
| **Desempenho**     | Respostas rápidas com cache e persistência local dos dados           |
| **Rastreabilidade**| Classificação e anotação de PLs com NLP                             |

---

## 2. Level 1 — Mapa do Sistema

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   👤 Usuário (Jornalista / Cidadão)                      │
│   Pessoa interessada no monitoramento legislativo        │
│   de feminicídio                                         │
│                                                          │
└────────────────────────┬─────────────────────────────────┘
                         │  Busca e analisa dados
                         │  legislativos sobre feminicídio
                         │  [HTTP]
                         ▼
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   🗺️  Mapa L.I.L.A.S                                    │
│   Agrega e exibe dados e projetos de lei                 │
│   sobre feminicídio                                      │
│                                                          │
└────────────────────────┬─────────────────────────────────┘
                         │  Consulta Projeto de Lei
                         │  [HTTP]
                         ▼
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   🏛️  API Senado / API Câmara  [Sistema Externo]         │
│   API externa que fornece acesso a dados de              │
│   proposições legislativas federais                      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Atores e Sistemas Externos

| Entidade | Tipo | Descrição |
|---|---|---|
| Usuário (Jornalista/Cidadão) | Pessoa | Acessa a plataforma para buscar e monitorar PLs sobre feminicídio |
| Mapa L.I.L.A.S | Sistema | Plataforma principal que agrega, processa e exibe os dados |
| API Senado Federal | Sistema externo | REST API pública com proposições, votações e tramitações do Senado |
| API Câmara dos Deputados | Sistema externo | REST API pública com projetos de lei e dados da Câmara |

---

## 3. Level 2 — Diagrama de Containers

### Containers Detalhados

#### 3.1 Frontend Web
| Propriedade | Valor |
|---|---|
| **Tecnologia** | React + Tailwind CSS |
| **Protocolo de entrada** | HTTP (navegador do usuário) |
| **Protocolo de saída** | HTTP/REST para o Backend API |
| **Responsabilidades** | Renderização das páginas, busca de PLs, exibição de cards, filtros e alertas |
| **Porta padrão** | 3000 (dev) / 80 ou 443 (prod) |

#### 3.2 Backend API
| Propriedade | Valor |
|---|---|
| **Tecnologia** | Python + FastAPI |
| **Protocolo de entrada** | HTTP/REST (vindo do Frontend) |
| **Protocolo de saída** | HTTP/REST (para APIs externas) + SQL (para PostgreSQL) |
| **Responsabilidades** | Orquestração das consultas, normalização dos dados, classificação NLP, persistência |
| **Porta padrão** | 8000 (HTTPS Porta 8000 / com CORS) |

#### 3.3 Banco de Dados
| Propriedade | Valor |
|---|---|
| **Tecnologia** | PostgreSQL |
| **Protocolo** | SQL |
| **Responsabilidades** | Persistência de PLs, parlamentares, usuários, alertas e histórico de buscas |
| **Porta padrão** | 5432 |

#### 3.4 API Senado / API Câmara (Sistema Externo)
| Propriedade | Valor |
|---|---|
| **Tipo** | Sistema externo (fora do controle da equipe) |
| **Protocolo** | HTTP/REST |
| **Dados fornecidos** | Proposições legislativas federais, tramitações, votações, autores |

---

## 4. Level 3 — Diagrama de Componentes

### 4.1 Frontend Web Application (React + Tailwind CSS)

#### Componentes do Frontend

| Componente | Tipo | Responsabilidade |
|---|---|---|
| `PáginaPrincipal` | React Component | Página raiz — orquestra busca e renderização dos resultados |
| `SearchForm` | React Component | Formulário de busca com termos, filtros de data, tipo e status |
| `PLCard` | React Component | Card individual de um PL com info de tramitação e metadados |
| `Header` | React (Tagmus) | Cabeçalho com logo, menu e dados de navegação |
| `InstPL Search` | Cortex/NLP | Busca semântica de PLs por termos e relevância |
| `AtomicComponents` | Frontend | Biblioteca de componentes UI reutilizáveis (Button, Input, Badge) |
| `Types & Constants` | Frontend | Contratos de dados: DTOs, enums de status, temas, filtros |

---

### 4.2 Backend API Application (FastAPI)

#### Componentes do Backend

| Componente | Tipo | Responsabilidade |
|---|---|---|
| `Flask App` | API Core | Configuração global: logs, CORS, rota raiz `/` |
| `PL+ Endpoint` | API Core | Endpoint principal que agrega e devolve PLs processados |
| `MonitorApiOrchestrator` | Application Service | Coordena chamadas às APIs, analisa textos e aplica filtros |
| `CamaraApiClient` | API Client | Realiza chamadas HTTP à API da Câmara dos Deputados |
| `SenadoApiClient` | API Client | Realiza chamadas HTTP à API do Senado Federal |
| `FilterParams` | Pydantic Model | Valida e parseia parâmetros de filtro (UF, tipo, status) |
| `Classifier` | Component | Classifica PLs por tema, tipo e estágio usando NLP/regex |
| `EncodingUser` | Pydantic/Schemas | Aplica codificação UTF-8 e resolve chaves duplicadas nas respostas |
| `PostgreSQL` | Container (Banco) | Persiste PLs, parlamentares, usuários e alertas |

---

---

## 5. Stack Tecnológica

| Camada | Tecnologia | Versão recomendada | Justificativa |
|---|---|---|---|
| **Frontend** | React | 18+ | Componentização e reatividade |
| **Estilização** | Tailwind CSS | 3+ | Utilitários rápidos e responsividade |
| **Backend** | Python | 3.11+ | Ecossistema NLP e integração com APIs |
| **Framework API** | FastAPI | 0.100+ | Performance, validação automática com Pydantic, docs OpenAPI |
| **Validação** | Pydantic | v2 | Tipagem forte dos modelos de dados |
| **Banco de Dados** | PostgreSQL | 15+ | Confiabilidade, queries complexas, suporte a JSONB |
| **APIs Externas** | API Senado + API Câmara | — | Dados legislativos federais oficiais |
| **NLP/Classifier** | Python (regex + NLP) | — | Classificação automática de PLs por tema |

---

## 6. Decisões Arquiteturais (ADRs)

### ADR-001: FastAPI como framework de backend
**Contexto:** Necessidade de um backend Python com validação automática, suporte a async e documentação OpenAPI.
**Decisão:** Usar FastAPI com Pydantic v2.
**Consequências:** Validação automática de inputs, geração de docs Swagger, suporte nativo a operações assíncronas para chamadas paralelas às APIs externas.

### ADR-002: PostgreSQL como banco de dados
**Contexto:** Os dados de PLs têm estrutura heterogênea entre Câmara e Senado.
**Decisão:** PostgreSQL com coluna `dados_raw JSONB` para armazenar a resposta bruta da API.
**Consequências:** Flexibilidade para diferentes estruturas de dados sem migrações constantes, mantendo integridade relacional nas colunas normalizadas.

### ADR-003: Aggregação das APIs no backend
**Contexto:** As APIs do Senado e da Câmara têm formatos diferentes.
**Decisão:** O `MonitorApiOrchestrator` no backend realiza a orquestração e normalização antes de devolver ao frontend.
**Consequências:** Frontend recebe dados já normalizados. Mudanças nas APIs externas impactam apenas o backend.

### ADR-004: Classificador NLP no backend
**Contexto:** PLs precisam ser categorizados por tema (feminicídio, violência doméstica, etc.).
**Decisão:** Componente `Classifier` com regras de regex + NLP em Python no backend.
**Consequências:** Classificação automática sem intervenção manual, extensível para modelos ML mais complexos futuramente.

---

## 7. Considerações de Segurança

| Aspecto | Medida |
|---|---|
| **CORS** | Configurado no Flask App para aceitar apenas origens autorizadas |
| **Validação de inputs** | FilterParams (Pydantic) valida todos os parâmetros de entrada |
| **Rate limiting** | Recomendado implementar rate limit nas rotas públicas |
| **SQL Injection** | Uso de ORM/queries parametrizadas (nunca SQL concatenado) |
| **Dados sensíveis** | Nenhum dado pessoal sensível além de e-mail de usuário |
| **APIs externas** | Chamadas são somente leitura (GET); sem autenticação necessária nas APIs públicas |
| **HTTPS** | Obrigatório em produção para todas as comunicações |

---

## 8. Escalabilidade e Observabilidade

### Estratégia de Cache

```
Requisição do Frontend
        │
        ▼
  ┌─────────────┐    HIT     ┌──────────────┐
  │  Redis Cache│──────────► │  Retorna     │
  │  (futuro)   │            │  resposta    │
  └──────┬──────┘            └──────────────┘
         │ MISS
         ▼
  Backend consulta APIs externas
  → Armazena resultado no cache (TTL: 1h)
  → Persiste no PostgreSQL
```

### Logs e Monitoramento Recomendados

| Componente | O que monitorar |
|---|---|
| Backend API | Tempo de resposta, erros 4xx/5xx, latência das chamadas às APIs externas |
| PostgreSQL | Queries lentas, conexões ativas, tamanho das tabelas |
| APIs Externas | Disponibilidade e tempo de resposta (Câmara/Senado podem ter instabilidade) |
| Frontend | Erros JS no console, tempo de carregamento inicial |

### Pontos de Extensão Futuros

- **Notificações por e-mail/push** quando um PL monitorado for atualizado
- **Exportação de dados** em CSV/JSON para jornalistas
- **Dashboard analítico** com evolução temporal dos PLs
- **Autenticação de usuários** para salvar buscas e alertas personalizados
- **Integração com Diário Oficial** para rastreamento de sanções e promulgações
- **API pública** do Mapa L.I.L.A.S para consumo por terceiros

---


