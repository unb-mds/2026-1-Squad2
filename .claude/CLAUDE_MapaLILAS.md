# CLAUDE.md

## Projeto

Mapa L.I.L.A.S — Sistema de coleta e ordenação de dados Legislativos públicos relacionados ao feminicídio.

*Plataforma para apoiar a transparência, accountability e análise de políticas públicas, unificando e mapeando proposições da Câmara dos Deputados e do Senado Federal em painéis visuais interativos.*

---

## Constituição

### Confiabilidade e Integridade de Dados
1. **Normalização estrita:** Os dados provenientes das APIs da Câmara e do Senado devem ser sempre convertidos para um modelo de dados único e unificado antes de qualquer persistência.
2. **Rastreabilidade da fonte:** Toda lei ou proposição exibida deve ter sua fonte (Câmara ou Senado) e link original claramente identificáveis. Não gere dados órfãos.
3. **Evite duplicidade:** Atualizações de status de tramitação devem sobrescrever ou versionar o registro existente, nunca criar propostas duplicadas no banco de dados.

### Transparência e Usabilidade
4. **Filtros resilientes:** A interface de busca deve permitir múltiplas combinações de filtros (UF, período, status) sem quebrar. Se não houver resultados, exiba uma mensagem clara em vez de uma tela vazia.
5. **Navegação fluida:** A Landing Page deve atuar estritamente como um funil para as visões detalhadas (indicadores, mapa, lista de projetos).
6. **Clareza nos indicadores:** Gráficos e indicadores de produtividade legislativa ou de equipe devem apresentar as métricas com rótulos autoexplicativos.

### Arquitetura e Manutenibilidade
7. **Isolamento de Domínios:** Mantenha a lógica de coleta de APIs separada da lógica de roteamento do FastAPI e da interface de usuário.
8. **Automação passiva:** O monitoramento da equipe SCRUM não deve interferir no código de produção do Mapa L.I.L.A.S; deve rodar estritamente via GitHub Actions gerando artefatos estáticos.

---

## Convenções técnicas

- **Linguagem Backend:** Python 3.10+
- **Framework Backend:** FastAPI
- **Frontend:** React (para componentização de dashboards, mapas de calor e landing page)
- **Persistência:** PostgreSQL (via SQLAlchemy ou SQLModel)
- **Integração / Automação (SCRUM):** GitHub Actions com deploy estático via GitHub Pages.
- **Estrutura de pastas:**
  - `backend/` — rotas FastAPI, modelos Pydantic, serviços de coleta e banco de dados.
  - `frontend/` — código React, componentes de UI, páginas.
  - `scripts/` — scripts analíticos (ex: extração de métricas do GitHub).
  - `.github/workflows/` — pipelines de CI/CD e monitoramento SCRUM.
- **Convenções de nomenclatura:**
  - Endpoints FastAPI em `snake_case` (ex: `/api/v1/proposicoes_feminicidio`).
  - Componentes React em `PascalCase`.
  - Commits semânticos (ex: `feat: normaliza API do Senado`, `fix: filtro de mapa de calor`).

---

## Como me ajudar

- **Sempre proponha a mudança mínima** que realiza a tarefa solicitada. Não refatore código não relacionado "de passagem".
- **Se uma mudança que você fosse gerar viola a Constituição, pare e avise** antes de escrever código.
- **Prefira escrever testes antes (ou junto) do código** quando a tarefa tem critérios de aceitação objetivos.
- **Uma tarefa por vez.** Não implemente duas tarefas no mesmo diff, mesmo que pareçam relacionadas.
- **Respeite o que já existe.** Antes de criar um novo arquivo/estrutura, verifique se a solução pode viver em código existente.
- **Ao lidar com as APIs Legislativas,** sempre verifique o schema de resposta atualizado nas documentações oficiais antes de construir os modelos Pydantic.

---

## Fora de escopo padrão

A menos que o pedido diga o contrário, **não faça**:

- Adicionar dependências externas novas.
- Reformatar código existente.
- Alterar a estrutura de pastas.
- Tocar em testes de outras funcionalidades.
- Criar documentação não solicitada (README, comentários "de cortesia", etc).
- Fazer commits sem revisão explícita.

---

## Funcionalidades

### 1. Coleta, Normalização e Classificação de Dados Legislativos (RF02, RF03)

**Status:** spec

#### Spec

Sistema de background que consulta periodicamente as APIs da Câmara e do Senado para coletar projetos de lei relacionados aos direitos das mulheres, feminicídio e violência doméstica. O sistema padroniza os retornos discrepantes em um modelo único e os classifica por tema, tipo e estágio.

**Comportamento Observável:**
- O sistema executa rotinas de coleta automática em uma frequência fixa de 2 em 2 horas, utilizando `BackgroundTasks` do FastAPI para o gerenciamento da tarefa no ciclo de vida da aplicação.
- A primeira inicialização do sistema (ou via endpoint administrativo) realiza uma carga histórica retroativa, buscando todos os projetos de lei aplicáveis desde um ano-base configurável.
- As requisições filtram proposições (com foco nas siglas PL e PLP) iterando estritamente pelas palavras-chave "feminicídio", "violência doméstica", "direitos da mulher" e "mulher".
- Nas consultas à API do Senado, a pesquisa é afunilada cruzando as palavras-chave com os códigos de assunto geral `130` (Direito Penal) e `143` (Direitos Humanos/Minorias).
- Os dados profundamente aninhados recebidos das APIs governamentais são "achatados" (flatten) em uma estrutura de dicionário simples e unificada antes da persistência no banco de dados.

**Critérios de aceitação:**
1. O agendador interno utilizando o FastAPI aciona corretamente os jobs de coleta a cada 2 horas, aproveitando parâmetros como `numdias=1` para garantir coletas incrementais leves no Senado.
2. A coleta histórica varre a paginação retroativamente a partir do ano-base sem sobrecarregar a memória do servidor.
3. **Validação Rigorosa de Schema:** Como os endpoints e estruturas de resposta do governo mudam com frequência, o sistema valida obrigatoriamente a assinatura do payload de resposta usando Pydantic antes de instanciar os modelos do banco.
4. Campos em locais divergentes das duas APIs (como extrair a autoria que, no Senado, demanda navegar por `documento > resumoAutoria` e extrair ementas de `conteudo > ementa`) são mapeados e salvos num formato único.
5. Registros da API que sejam inválidos ou cujos layouts tenham sido descontinuados silenciosamente não paralisam todo o job, mas são ignorados e geram logs de alerta.

**Casos de borda:**
- **Indisponibilidade das APIs do governo:** O sistema não deve falhar criticamente; deve apenas registrar um log de aviso (`warning`), abortar a coleta do ciclo atual e tentar novamente na próxima janela de 2 horas.
- **Mudança de contrato (Schema):** Se a estrutura JSON das APIs mudar estruturalmente adicionando novas chaves ou mudando os níveis de resposta, o modelo Pydantic deve lançar uma exceção clara interrompendo apenas a persistência do dado malformado para evitar poluição do banco.

#### Plano

**Decisões técnicas:**

- **Coleta e Agendamento:**
  - **Escolha:** Implementação via `BackgroundTasks` nativo do FastAPI executando funções em loop assíncrono (ex: via `asyncio.sleep` atrelado aos eventos de *startup* da aplicação).
  - **Rationale:** Atende a exigência de ser de 2 em 2 horas mantendo a stack restrita ao Python, dispensando temporariamente a necessidade de gerenciar filas complexas como Celery.
- **Isolamento e Tratamento das Respostas:**
  - **Escolha:** Construção de adaptadores isolados no `backend/services` responsáveis exclusivamente por transformar o JSON aninhado do Senado (onde as situações legislativas ficam escondidas dentro de `autuacoes > situacoes`) em objetos planos (DTOs).
  - **Rationale:** Reduz o acoplamento. As APIs do Senado retornam respostas extensas com muitos níveis pouco padronizados, e essa camada intermediária facilita a manutenção se o governo atualizar a versão do endpoint.
- **Segurança de Tipagem (Validação Pydantic):**
  - **Escolha:** Configurar as models Pydantic de Ingestão (`CamaraResponse`, `SenadoResponse`) para não aceitarem extração de dados cegamente caso os nós vitais tenham mudado de lugar.
  - **Rationale:** A verificação estrita do schema cumpre a regra de Confiabilidade da Constituição do projeto, mitigando o risco das frequentes instabilidades de endpoints governamentais.

#### Tarefas

1. **Definição de Schemas de Ingestão (Pydantic):**
   - **Depende de:** —
   - **Pronto quando:** Modelos Pydantic para `CamaraResponse` e `SenadoResponse` estiverem implementados e validados contra os payloads reais das APIs, garantindo o mapeamento de campos aninhados como `documento > resumoAutoria` e `conteudo > ementa`.

2. **Infraestrutura de Persistência (SQLAlchemy/SQLModel):**
   - **Depende de:** —
   - **Pronto quando:** As tabelas `pls_senado`, `pls_camara`, `parlamentares` e as tabelas de autoria estiverem mapeadas no banco PostgreSQL conforme a modelagem definida.

3. **Desenvolvimento do Serviço de Normalização:**
   - **Depende de:** 1, 2.
   - **Pronto quando:** Existir uma lógica de "achatamento" (flatten) que converta os objetos complexos das APIs em registros planos prontos para o banco de dados, tratando duplicatas e limpando strings de ementas.

4. **Implementação do Entrypoint de Carga Histórica:**
   - **Depende de:** 3.
   - **Pronto quando:** Um endpoint administrativo (ex: `/admin/coleta/historica`) for capaz de receber um ano-base e realizar a varredura retroativa completa de PLs, PLPs e PECs usando as palavras-chave e códigos de assunto (`130`, `143`).

5. **Configuração do Agendador de Coleta Incremental:**
   - **Depende de:** 3.
   - **Pronto quando:** A lógica de `BackgroundTasks` do FastAPI estiver configurada para rodar a cada 2 horas, utilizando o parâmetro `numdias=1` para buscar apenas atualizações recentes e otimizar a performance.

6. **Sistema de Logs e Resiliência:**
   - **Depende de:** 4, 5.
   - **Pronto quando:** Falhas de conexão ou mudanças repentinas nos schemas das APIs governamentais forem capturadas por blocos try/except, gerando logs de alerta sem interromper a execução do servidor FastAPI.

### 2. Portal Público L.I.L.A.S: Dashboards, Mapa e Listagem (RF01, RF04, RF05, RF06, RF07, RF08)

**Status:** spec

#### Spec

Interface voltada ao cidadão/pesquisador. Inclui uma landing page responsiva que guia aos painéis interativos. Os painéis exibem mapa de calor de atuação por estado, detalhamento por projeto de lei e permitem buscas complexas cruzando variáveis.

**Critérios de aceitação:**

1. A landing page carrega corretamente em dispositivos móveis e desktops.
2. O Painel exibe os indicadores agregados (qtd por ano, status, tempo médio, parlamentares ativos).
3. O Mapa de Calor Nacional destaca visualmente as UF com maior número de representantes/leis.
4. É possível filtrar as proposições cruzando os critérios (UF + período + categoria [PL, PLC, PEC] + status).
5. Cada proposição tem uma rota de detalhe (ex: `/proposicao/123`) exibindo todo seu histórico de tramitação.

**Casos de borda:**

- Pesquisa sem resultados para filtros extremamente específicos não deve quebrar os gráficos, mas exibir estado vazio (empty state) amigável.

### 3. Análise de Produtividade da Equipe SCRUM

**Status:** spec

#### Spec

Esta funcionalidade visa fornecer uma visão analítica sobre a saúde do desenvolvimento do Mapa L.I.L.A.S, permitindo que a equipe identifique gargalos e visualize o ritmo de entrega através de um dashboard puramente estático e automatizado.

**Comportamento Observável:**
O sistema gera um arquivo `index.html` hospedado no GitHub Pages que apresenta:
- **Gráfico de Commits:** Frequência temporal de envios para o repositório.
- **Fluxo de Issues:** Quantidade de issues abertas vs. fechadas por período.
- **Métrica de Volume por Tarefa:** Gráfico relacionando a quantidade de caracteres do corpo (body) de cada Issue com a complexidade percebida (proxy de esforço).
- **Métrica de Pull Requests:** Quantidade de PRs abertos (em revisão/aguardando) e fechados (mergeados ou rejeitados) por período.
- **Timestamp de Atualização:** Horário da última execução da análise via GitHub Actions.

**Critérios de aceitação:**
1. A página deve ser acessível via URL do GitHub Pages do projeto.
2. **Independência de API no Frontend:** O HTML gerado deve ser 100% estático. A página não deve realizar nenhuma requisição (fetch/XHR) à API do GitHub no momento em que o usuário a acessa.
3. Toda a mineração de dados (commits, issues, PRs) ocorre estritamente nos bastidores, durante a execução do script Python na GitHub Action. Os resultados são consolidados e "injetados" (baked-in) dentro do HTML gerado.
4. A interface deve utilizar Chart.js (ou similar via CDN) para renderização dos gráficos, consumindo apenas o objeto JSON estático que foi embutido no arquivo pelo script gerador.

**Casos de borda:**
- **Repositório sem atividades na semana:** O dashboard deve exibir "Sem atividades recentes" nos gráficos em vez de quebrar a renderização.
- **Falha no Token do GitHub:** A Action deve falhar com um log claro, sem deletar a versão anterior funcional do GitHub Pages.

**Fora de escopo:**
- Integração com o banco de dados PostgreSQL do projeto principal.
- Avaliação qualitativa de código (code review automatizado). Apenas métricas de volume e tempo.
- Consultas dinâmicas em tempo real (runtime) a APIs externas pelo navegador.

#### Plano

**Decisões técnicas:**

- **Arquitetura de Dados:**
  - **Escolha:** Build-time data fetching (Geração estática).
  - **Rationale:** Evita problemas de limite de requisições (rate limit) da API do GitHub ao acessar a página. A visualização reflete o último "retrato" tirado pela pipeline.
- **Script de Extração:** - Python usando `PyGithub` rodando em `.github/workflows/`. O script (`metrics/analyzer.py`) irá gerar o arquivo final `index.html` (inserindo os dados calculados diretamente no corpo do documento) na pasta `metrics/output/`.
- **Pipeline de CI/CD (GitHub Actions):**
  - **Escolha:** Workflow agendado (cron) e acionável manualmente (workflow_dispatch).
  - **Permissões:** Necessita de `contents: write` para publicar no branch `gh-pages`.
  - **Implementação Base (`.github/workflows/scrum-metrics.yml`):**
    ```yaml
    name: Atualiza Métricas SCRUM

    on:
      schedule:
        - cron: '0 2 * * 0' # Executa todo domingo às 02:00
      workflow_dispatch: # Permite execução manual

    permissions:
      contents: write
      pages: write
      id-token: write

    jobs:
      build-and-deploy:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout repository
            uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.10'

          - name: Install dependencies
            run: pip install PyGithub

          - name: Run metrics analyzer
            env:
              GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            run: python metrics/analyzer.py # Este script gera o HTML com os dados já injetados

          - name: Deploy to GitHub Pages
            uses: peaceiris/actions-gh-pages@v4
            with:
              github_token: ${{ secrets.GITHUB_TOKEN }}
              publish_dir: ./metrics/output
              force_orphan: true
    ```

#### Tarefas
1. **Configurar Script Python (`metrics/analyzer.py`):** Criar lógica de conexão com API do GitHub para minerar commits, issues e PRs e consolidar os dados em estruturas simples (dicionários/listas).
2. **Desenvolver Template (`metrics/template.html`):** Estrutura base com placeholders (ex: `{{ DATA_PAYLOAD }}`) onde o script Python injetará os dados consolidados para consumo do Chart.js.
3. **Gerador Estático:** Atualizar o script Python para ler o `template.html`, substituir o placeholder pelos dados reais minados e salvar o `index.html` final em `metrics/output/`.
4. **Pipeline de Automação:** Adicionar o arquivo `.github/workflows/scrum-metrics.yml` para rodar o processo e atualizar silenciosamente a página no GitHub Pages.

### 4. Desenvolvimento do Banco de Dados (PostgreSQL)

**Status:** spec

#### Spec

Esta funcionalidade estabelece a espinha dorsal de dados do Mapa L.I.L.A.S, garantindo que as informações coletadas das APIs governamentais sejam armazenadas de forma estruturada, permitindo consultas complexas, análises de gênero e monitoramento de tramitação em tempo real.

**Comportamento Observável:**
- O banco de dados centraliza as proposições da Câmara e do Senado em um esquema que permite a filtragem unificada por UF, partido, ano e estágio de tramitação.
- O sistema mantém um registro histórico de parlamentares, incluindo dados vitais para o projeto como o sexo (para análise de autoria feminina em leis de combate ao feminicídio).
- A estrutura de tabelas de autoria (`autoria_camara`, `autoria_senado`) permite identificar quem são os autores principais e coautores de cada projeto, alimentando o indicador de "parlamentares mais ativos".
- **Histórico Linear:** O sistema armazena a linha do tempo completa de tramitação de cada projeto em tabelas dedicadas, permitindo a exibição do passo a passo do status (RF06).
- **Cofre de Dados (Raw Data):** O banco salva o payload JSON original das APIs governamentais junto aos dados estruturados, servindo como backup caso o parser precise ser reprocessado no futuro.

**Critérios de aceitação:**
1. **Unicidade de Registros:** O banco deve utilizar chaves primárias que evitem a duplicidade de proposições ao rodar coletas repetitivas (2 em 2h). Para parlamentares, deve ser aplicado o padrão de prefixo (ex: `cam_141492`) para evitar conflitos de IDs.
2. **Normalização e Restrições (Constraints):** O campo `sexo` na tabela `parlamentares` deve ser restrito a "F" ou "M" (`ck_parlamentares_sexo`), e a casa legislativa restrita a "Câmara" ou "Senado" (`ck_parlamentares_casa`).
3. **Integridade Referencial e Cascatas:** Exclusões de projetos ou parlamentares devem refletir em `CASCADE` nas tabelas de autoria e tramitações para evitar dados órfãos no banco.
4. **Auditoria:** Todas as tabelas mutáveis devem conter campos `created_at` e `updated_at` gerenciados pelo servidor de banco de dados (`func.now()`).
5. **Tipagem Híbrida:** O armazenamento dos dados originais das APIs deve utilizar o tipo `JSONB` nativo do PostgreSQL nas tabelas de proposições e tramitações.

**Casos de borda:**
- **Parlamentares sem partido:** O banco deve aceitar valores nulos ou "Sem Partido" (S/Part) para parlamentares em transição, sem quebrar as rotas de filtragem.
- **Ementas Longas:** O campo `ementa` deve ser do tipo `TEXT` para suportar descrições legislativas extensas.

#### Plano

**Decisões técnicas:**

- **ORM e Modelagem:**
  - **Escolha:** SQLAlchemy (com DeclarativeBase e tipagem nativa).
  - **Rationale:** Permite mapeamento robusto, uso nativo de dialectos do Postgres (como JSONB) e configuração granular de constraints de banco e ondelete (CASCADE).
- **Gerenciamento de Migrações:**
  - **Escolha:** Alembic.
  - **Rationale:** Essencial para evoluir o schema do banco à medida que novos campos das APIs governamentais forem mapeados, sem perda de dados históricos já coletados.
- **Estratégia de Inserção e Atualização:**
  - **Escolha:** "Upsert" (Update or Insert) baseado no ID único da proposição, atualizando as linhas do tempo de tramitação incrementalmente.
  - **Rationale:** Cumpre o princípio da Constituição de "evitar duplicidade", garantindo que novos status simplesmente adicionem novas linhas na tabela de tramitação respectiva.

#### Tarefas

1. **Configuração do Ambiente Database:**
   - **Depende de:** —
   - **Pronto quando:** Instância PostgreSQL configurada e acessível via string de conexão no arquivo `.env`.

2. **Implementação das Models (SQLAlchemy):**
   - **Depende de:** 1.
   - **Pronto quando:** Arquivos de modelos criados com os relacionamentos Bidirecionais (`relationship` e `back_populates`) para Proposições, Tramitações, Parlamentares e Autoria.

3. **Criação dos Scripts de Migração Inicial:**
   - **Depende de:** 2.
   - **Pronto quando:** Comando `alembic upgrade head` executado com sucesso, criando todas as tabelas no banco de dados.

4. **Desenvolvimento dos Entrypoints de Persistência:**
   - **Depende de:** 2.
   - **Pronto quando:** Funções de serviço estiverem implementadas processando e preenchendo as chaves estrangeiras corretamente (garantindo que o Parlamentar exista antes da Autoria, e o PL exista antes da Tramitação).

5. **Otimização e Índices:**
   - **Depende de:** 3.
   - **Pronto quando:** Índices de banco de dados aplicados nas colunas de busca (UF, Partido, Tipo de Proposição) para suportar os filtros do Portal (RF08).

#### Tabelas de Referência (Esquema Central)

```sql
  -- Proposições
  pls_senado (id PK, codigo_materia, identificacao, ementa, dados_raw JSONB, updated_at)
  pls_camara (id PK, numero, ano, sigla_tipo, ementa, dados_raw JSONB, updated_at)

  -- Histórico (1:N)
  tramitacao_senado (id PK, id_pl FK, situacao, local, sequencia, dados_raw JSONB)
  tramitacao_camara (id PK, id_pl FK, situacao, local, sequencia, dados_raw JSONB)

  -- Parlamentares e Autoria (N:M)
  parlamentares (id PK, casa, nome_eleitoral, sigla_partido, sigla_uf, sexo)
  autoria_camara (id_pl FK, id_parlamentar FK, tipo_autoria) -- PK Composta
  autoria_senado (id_pl FK, id_parlamentar FK, tipo_autoria) -- PK Composta
```
