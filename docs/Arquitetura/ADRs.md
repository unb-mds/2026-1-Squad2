# ⚖️ Decisões Arquiteturais (ADRs)

Este documento registra os *Architecture Decision Records* (ADRs). Cada seção abaixo documenta uma decisão importante de tecnologia ou design adotada no projeto, acompanhada de seu contexto e de suas consequências.

---

## ADR-001: FastAPI como framework de backend

**Contexto:**
Necessidade de um backend em Python com validação automática, suporte a rotinas assíncronas (async) para alta performance de rede e documentação OpenAPI gerada automaticamente.

**Decisão:**
Usar o framework **FastAPI** em conjunto com a biblioteca **Pydantic v2**.

**Consequências:**
- Validação automática e robusta de inputs e tipagem de dados.
- Geração gratuita e em tempo real de documentação Swagger.
- Suporte nativo a operações assíncronas, acelerando chamadas paralelas às APIs externas (Câmara e Senado).

---

## ADR-002: PostgreSQL como banco de dados

**Contexto:**
Os dados de PLs têm estruturas heterogêneas dependendo da fonte de origem (a Câmara dos Deputados organiza dados de forma diferente do Senado Federal).

**Decisão:**
Adotar **PostgreSQL** utilizando uma coluna do tipo `JSONB` (`dados_raw`) para armazenar a resposta bruta da API original.

**Consequências:**
- Flexibilidade máxima para suportar diferentes estruturas de dados.
- Previne a necessidade de migrações complexas a cada mudança no esquema das APIs governamentais.
- Mantém a integridade relacional padrão para colunas vitais e normalizadas (como IDs, Datas, etc.).

---

## ADR-003: Ingestão Assíncrona e Persistência Local (ETL)

**Contexto:**
As requisições dinâmicas diretas às APIs do Senado e da Câmara são muito lentas, sujeitas a quedas constantes e retornam esquemas diferentes de JSON. Fazer o Frontend esperar o Backend bater no Governo em tempo real degradaria a experiência do usuário.

**Decisão:**
Implementar uma arquitetura de extração, transformação e carga (ETL). Criar scripts isolados (`services/` e `popular_banco.py`) que rodam em background (ou via Cron), puxam todos os dados do Governo, normalizam e salvam no nosso banco PostgreSQL. As rotas públicas consumidas pelo Frontend (`routers/`) consultam apenas o nosso banco local.

**Consequências:**
- **Performance:** O Frontend recebe dados instantâneos do nosso banco de dados.
- **Resiliência:** Se as APIs da Câmara ou Senado caírem, a nossa plataforma continua 100% no ar, servindo o último dado cacheado no PostgreSQL.
- Maior complexidade operacional, pois exige agendamento de rotinas para manter o banco atualizado (sincronização).

---

## ADR-004: Classificador via NLP no backend

**Contexto:**
A pauta de projetos de lei precisa ser categorizada com altíssima precisão por temas vitais como "feminicídio" ou "violência doméstica", algo que as APIs padrão muitas vezes falham em taguear.

**Decisão:**
Desenvolver um Componente Classificador (`Classifier`) combinando heurísticas, **Regex** e algoritmos de **PNL** (Processamento de Linguagem Natural) via Python no Backend.

**Consequências:**
- Classificação automática da lei sem nenhuma intervenção humana.
- Arquitetura extremamente extensível, permitindo o acoplamento de LLMs ou modelos de IA preditivos mais complexos no futuro.
