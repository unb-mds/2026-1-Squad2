# 🛡️ Qualidade e Operação

Este documento cobre as estratégias não funcionais do sistema, focando em manter a plataforma robusta, segura, auditável e escalável para cenários de alta demanda jornalística ou picos de consulta.

---

## 1. Considerações de Segurança

O sistema adota abordagens práticas de *Security by Design* para mitigar os principais vetores de ameaça:

| Aspecto | Medida e Mitigação |
|---|---|
| **Validação de inputs** | O modelo `FilterParams` do Pydantic valida agressivamente todos os parâmetros de entrada vindos da web. |
| **Rate Limiting** | Bloqueios sistemáticos de IPs por excesso de chamadas em rotas públicas do FastAPI (Prevenção de DDoS simples). |
| **SQL Injection** | Acesso ao banco de dados sempre utilizando ORM e *queries parametrizadas* nativas do framework (nunca queries concatenadas string puro). |
| **Dados Sensíveis** | Exposição nula. Não retemos informações pessoais sensíveis. As senhas de administradores são encriptadas via bcrypt. |
| **APIs Externas** | Comunicação unidirecional de busca (GET). Não injetamos nem enviamos chaves de autenticação da nossa aplicação nas APIs do governo. |
| **HTTPS (SSL/TLS)** | Obrigatório em ambiente de produção em todas as pontas (Frontend <-> Backend <-> Banco). |

---

## 2. Escalabilidade e Resiliência

Para não sofrer timeouts e sobrecargas ao lidar com dezenas de milhares de Leis e requisições concorrentes, a aplicação garante alta resiliência separando o consumo da ingestão.

### 2.1 Estratégia de Isolamento de Banco de Dados

Em vez de atuar como um *Proxy* para as instáveis APIs do governo, nosso backend aplica uma **Estratégia ETL**:

```mermaid
flowchart LR
    subgraph FrontendClient [Frontend Client]
        Req[Requisição do Usuário]
    end
    
    subgraph APIRest [API Rest / Routers]
        App[FastAPI Endpoints]
        DB[(PostgreSQL Local)]
    end
    
    subgraph BackgroundJobs [Background Jobs / Services]
        Script[Rotina de População]
        APIgov[Câmara / Senado]
    end

    %% O front conversa SÓ com o banco
    Req <-->|Instantâneo| App
    App <-->|Consulta Rápida| DB
    
    %% O job atualiza o banco isoladamente
    Script -->|Baixa Dados Lentos| APIgov
    Script -->|Atualiza (Upsert)| DB
    
    classDef banco fill:#311b92,stroke:#b39ddb,stroke-width:2px,color:#fff;
    class DB banco;
```

Nesse modelo, se as APIs do governo ficarem fora do ar durante todo o fim de semana, o **Mapa L.I.L.A.S** continuará 100% responsivo para os jornalistas, servindo os dados consolidados da última atualização bem-sucedida.

### 2.2 Logs e Monitoramento Recomendados

Identificar falhas rapidamente é crucial quando dependemos de ecossistemas externos (gov.br).

| Componente | O que deve ser Monitorado ativamente |
|---|---|
| **Backend API** | Tempo médio de resposta, pico de Erros 4xx e 5xx, latência média na comunicação entre o nosso backend e os servidores do governo. |
| **Banco PostgreSQL** | Deadlocks, lentidão nas queries JSONB e picos de conexão no pool. |
| **Sistemas Externos** | Quedas ou manutenção nos sites da Câmara ou do Senado. |
| **Frontend Web** | Exceptions não tratadas em JS/React estourando no cliente, *Time to Interactive* (TTI). |

---

## 3. Pontos de Extensão Futuros (Roadmap Arquitetural)

As tecnologias escolhidas viabilizam as seguintes implementações estratégicas num futuro próximo:

*   🔔 **Notificações Ativas:** Disparo de e-mails ou Webhooks imediatos quando o status de um PL crítico for modificado no plenário.
*   📊 **Exportação Crua:** Criação de rotas `/export/csv` dedicadas para consumo direto por Data Scientists investigativos.
*   🔐 **Painel Analítico Privado:** Autenticação (OAuth) que permite a usuários premium ou ONGs salvarem coleções privadas de PLs e dashboards montados sob medida.
*   📚 **API Pública do L.I.L.A.S:** Expor nossas rotas agregadas (`Senado + Câmara`) para a sociedade civil através de chaves de API próprias, poupando que outras startups refaçam esse trabalho exaustivo de garimpo.
