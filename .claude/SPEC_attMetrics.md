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

### 3. Análise de Produtividade da Equipe SCRUM

**Status:** spec
#### Spec

Esta funcionalidade visa fornecer uma visão analítica sobre a saúde do desenvolvimento do Mapa L.I.L.A.S, permitindo que a equipe identifique gargalos e visualize o ritmo de entrega através de um dashboard puramente estático e automatizado.

**Comportamento Observável:**

O sistema gera um arquivo `index.html` hospedado no GitHub Pages que apresenta:

- 1. **Gráfico de linhas — Issues abertas vs. fechadas por semana**  
   - Eixo X: semanas (formato `YYYY-WXX`).  
   - Eixo Y: quantidade.  
   - Duas séries: "Abertas" e "Fechadas".  
  
2. **Histograma — Quantidade de caracteres na mensagem de commit**  
   - Eixo X: faixas de caracteres (0–20, 21–50, 51–100, 101–200, 200+).  
   - Eixo Y: número de commits naquela faixa.  
  
3. **Gráfico de barras — Quantidade de co-autores por semana**  
   - Eixo X: semanas.  
   - Eixo Y: total de linhas `Co-authored-by` encontradas nos commits daquela semana.  
  
4. **Mapa de calor — Horário dos commits por dia da semana**  
   - Eixo X: horas do dia (0h–23h).  
   - Eixo Y: dias da semana (Seg–Dom).  
   - Cor: gradiente de `#e8f4f8` (zero commits) a `#003366` (máximo).  
   - Tooltip mostra dia, hora e quantidade de commits.  
  
5. **Gráfico de barras empilhadas — Issues abertas/fechadas por semana**  
   - Mesmo dado do item 1, mas em formato de barras empilhadas para visualização alternativa.  
  
6. **Ranking — Top committers**  
   - Tabela ordenada por número de commits (desc).  
   - Colunas: posição, nome/username, total de commits.

7. **Ranking — Top autores de PRs**  
   - Tabela ordenada por número de PRs abertas (desc).  
   - Colunas: posição, nome/username, total de PRs abertas.  
  
8. **Ranking — Top em Issues (abertas + fechadas)**  
   - Tabela ordenada pela soma de issues abertas + issues fechadas pelo usuário (desc).  
   - Colunas: posição, nome/username, issues abertas, issues fechadas, total.

**Critérios de aceitação:**

1. 1. O arquivo `docs/scrum/index.html` abre corretamente no navegador sem servidor local (protocolo `file://` ou via GitHub Pages).  
2. O arquivo `docs/scrum/metrics.json` é gerado pelo workflow e contém todas as seções: `issues_per_week`, `commit_message_histogram`, `coauthors_per_week`, `commit_heatmap`, `top_committers`, `top_pr_authors`, `top_issue_contributors`.  
3. O workflow `.github/workflows/scrum metrics.yml` executa com sucesso no GitHub Actions usando apenas `GITHUB_TOKEN`.  
4. O workflow roda automaticamente todo domingo às 03:00 UTC e pode ser disparado manualmente via `workflow_dispatch`.  
5. Após a execução, o workflow faz commit do `metrics.json` atualizado no branch `main`.  
6. Os gráficos renderizam corretamente com os dados do JSON (sem erros no console).  
7. A página é responsiva (funciona em mobile e desktop).  
8. O ranking exibe pelo menos os 10 primeiros ou todos os contribuidores (o que for menor).

**Casos de borda:**

- **Semana sem atividade:** a semana aparece no eixo X com valor 0; não é omitida.  
- **Commit sem mensagem (squash vazio):** conta como 0 caracteres na faixa 0–20.  
- **Usuário deletado (ghost):** aparece como `ghost` nos rankings.  
- **Co-authored-by com formato inválido:** é ignorado silenciosamente.  
- **Repositório com < 1 semana de histórico:** exibe os dados disponíveis sem erro.

**Fora de escopo:**

- Métricas de code review (comments em PRs).  
- Métricas de CI (tempo de build, falhas).  
- Filtro interativo por período.  
- Autenticação ou área restrita.  
- Armazenamento histórico (o JSON é sempre reescrito por completo).
#### Plano

**Decisões técnicas:**

- **Coleta de dados:**  
  - **Escolha:** Script Python usando `PyGithub` para acessar a API REST do GitHub.  
  - **Alternativas consideradas:** GitHub GraphQL API; `gh` CLI direto no workflow.  
  - **Rationale:** `PyGithub` é bem documentada, suporta paginação automática e o projeto já usa Python. A GraphQL seria mais eficiente mas adiciona complexidade de queries. O `gh` CLI limitaria a lógica a shell scripts.  
  
- **Visualização:**  
  - **Escolha:** Chart.js + tabelas HTML puras com estilo Tailwind CDN.  
  - **Alternativas consideradas:** D3.js; Mermaid; imagens estáticas geradas por matplotlib.  
  - **Rationale:** D3.js oferece controle total sobre SVG, permite customização avançada dos gráficos e escalas bem para visualizações futuras. Chart.js é mais simples mas menos flexível. Imagens estáticas perdem interatividade.  
  
- **Persistência dos dados:**  
  - **Escolha:** Arquivo JSON único commitado no repo pelo próprio workflow.  
  - **Alternativas consideradas:** GitHub Pages artifact; branch separado `gh-pages`.  
  - **Rationale:** JSON no mesmo branch mantém histórico via git, é simples de debugar, e GitHub Pages pode servir de qualquer pasta configurada.  
  
- **Agendamento:**  
  - **Escolha:** `cron: '0 2 * * 0'` (domingo 03:00 UTC) + `workflow_dispatch`.  
  - **Rationale:** Frequência semanal alinha com as sprints da disciplina; horário de madrugada evita conflitos com trabalho ativo.
 
- **Pipeline de CI/CD (GitHub Actions):**

  - **Escolha:** Workflow agendado (cron) e acionável manualmente (workflow_dispatch).

  - **Permissões:** Necessita de `contents: write` para publicar no branch `gh-pages`.

  - **Implementação Base (`.github/workflows/scrum-metrics.yml`):**

 ```yaml
name: Atualiza Métricas SCRUM

on:

  schedule:

    - cron: '0 2 * * 0'   # Toda domingo às 02:00 UTC

  workflow_dispatch:        # Permite execução manual pela UI do GitHub

  

permissions:

  contents: write

  

jobs:

  build-and-deploy:

    runs-on: ubuntu-latest

  

    steps:

      - name: Checkout repositório

        uses: actions/checkout@v4

  

      - name: Configurar Python 3.10

        uses: actions/setup-python@v5

        with:

          python-version: '3.10'

  

      - name: Instalar dependências

        run: pip install PyGithub

  

      - name: Executar analyzer

        env:

          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

          # GITHUB_REPOSITORY já é injetado automaticamente pelo Actions

        run: python metrics/analyzer.py

  

      - name: Salvar métricas na pasta docs

        run: |

          mkdir -p docs/scrum

          cp -r metrics/output/* docs/scrum/

      - name: Commit e Push das métricas atualizadas

        run: |

          git config --global user.name "github-actions[bot]"

          git config --global user.email "github-actions[bot]@users.noreply.github.com"

          git add docs/scrum/

          git commit -m "chore: atualiza métricas scrum [skip ci]" || echo "Sem mudanças para commitar"

          git push
 ```

#### Tarefas

1. **Criar script coletor (`metrics/analizer.py`)**  
   - **Depende de:** —  
   - **Pronto quando:**  
     - O script aceita variáveis de ambiente `GITHUB_TOKEN` e `GITHUB_REPOSITORY`.  
     - Gera `docs/scrum/metrics.json` com schema correto.  
     - Roda localmente com `python analizer.py` (dado token válido).  
   - **Fora de escopo:** renderização HTML, workflow.  
  
2. **Criar workflow (`.github/workflows/metrics.yml`)**  
   - **Depende de:** Tarefa 1.  
   - **Pronto quando:**  
     - Instala dependências, executa o script, e commita o JSON atualizado.  
     - Roda no cron semanal e via dispatch manual.  
     - Usa apenas `GITHUB_TOKEN` (permissões `contents: write`).  
   - **Fora de escopo:** a página HTML.  
  
1. **Criar página HTML (`docs/scrum/index.html`)**  
   - **Depende de:** Tarefa 1 (precisa do schema do JSON para bindar os gráficos).  
   - **Pronto quando:**  
     - Carrega `metrics.json` via `fetch` relativo.  
     - Renderiza todos os 7 componentes visuais descritos na spec.  
     - Responsivo (mobile-first com Tailwind).  
     - Sem erros no console do navegador.  
   - **Fora de escopo:** coleta de dados, CI.  
  
4. **Configurar GitHub Pages**  
   - **Depende de:** Tarefas 2 e 3.  
   - **Pronto quando:**  
     - A página é acessível via URL pública do GitHub Pages.  
     - O JSON é servido corretamente (sem CORS issues em mesmo domínio).  
   - **Fora de escopo:** DNS customizado.

### Schema do `metrics.json`  


```JSON

{
  "generated_at": "2025-05-11T03:00:00Z",
  "repository": "unb-mds/2026.1-ContraDito",
  "issues_per_week": [
    { "week": "2025-W01", "opened": 5, "closed": 3 }
  ],
  "commit_message_histogram": [
    { "range": "0-20", "count": 12 },
    { "range": "21-50", "count": 30 },
    { "range": "51-100", "count": 45 },
    { "range": "101-200", "count": 20 },
    { "range": "200+", "count": 5 }
  ],
  "coauthors_per_week": [
    { "week": "2025-W01", "count": 4 }
  ],
  "commit_heatmap": [
    { "day": 0, "hour": 10, "count": 8 },
    { "day": 6, "hour": 22, "count": 2 }
  ],
  "top_committers": [
    { "username": "fulano", "name": "Fulano Silva", "commits": 42 }
  ],
  "top_pr_authors": [
    { "username": "fulano", "name": "Fulano Silva", "prs_opened": 15 }
  ],
  "top_issue_contributors": [
    { "username": "fulano", "name": "Fulano Silva", "opened": 10, "closed": 8, "total": 18 }
  ]
}
```
