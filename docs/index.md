# 🗺️ Mapa L.I.L.A.S - MDS 2026.1

Bem-vindo à documentação oficial do projeto **Mapa L.I.L.A.S**, desenvolvido no âmbito da disciplina de **Métodos de Desenvolvimento de Software (MDS)** da Universidade de Brasília (UnB).

---

!!! info "Visão do Produto"
    O **Mapa LILAS** (*Mapa Legislativo Informativo de Leis de Acompanhamento Social*) é uma plataforma concebida para o monitoramento de dados legislativos com relação à Pauta do Feminicídio e Direitos da Mulher. O nosso foco é fornecer uma solução de software transparente, fiável e analítica.

## 🧭 Mapa da Documentação

Navegue rapidamente pelas seções atualizadas do nosso projeto:

<div class="grid cards" markdown>

-   📋 **Requisitos e UX**
    ---
    Conheça as bases do nosso produto, nosso público-alvo e protótipos.
    * [Visão do Produto](Requisitos/Visão de produto.md)
    * [Critérios de Aceitação](Requisitos/Criterios de aceitacao.md)
    * [Persona (Marina)](Requisitos/Persona.md)
    * [Story Map & Wireframes](Requisitos/Wireframe.md)

-   🏗️ **Arquitetura de Software**
    ---
    Detalhes técnicos, decisões e fluxos do nosso Backend de ETL.
    * [Visão Geral (Sistema)](Arquitetura/Visao_Geral.md)
    * [Modelagem C4](Arquitetura/C4_Model.md)
    * [Decisões (ADRs)](Arquitetura/ADRs.md)
    * [Qualidade e Isolamento DB](Arquitetura/Seguranca_Escalabilidade.md)

-   🗄️ **Banco de Dados & Estudos**
    ---
    Pesquisas e modelagem de persistência.
    * [PostgreSQL (Sprint 02)](Estudos/Sprint02/postgreSQL.md)
    * [API Senado / Câmara](<Estudos/Sprint04/Estudo API da Câmara do Senado.md>)

</div>

---

## 🎯 Funcionalidades Principais (Épicos)

1. **Visualização de Dashboards:** Geração de gráficos interativos e alternância de tipos de visualização.
2. **Home (Landing Page):** Painel inicial com indicadores globais e ranking de estados.
3. **Consulta de Proposições:** Busca textual com filtros avançados.
4. **Detalhamento Legislativo:** Exibição da ementa e linha do tempo de tramitação.

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologias |
| :--- | :--- |
| **Frontend** | React, TailwindCSS |
| **Backend API & ETL** | Python, FastAPI |
| **Base de Dados** | PostgreSQL |
| **Documentação** | Material for MkDocs |

---

## 🚀 Como Executar Localmente

Para configurar o ambiente de desenvolvimento na sua máquina:

=== "Comandos (Linux / macOS)"

    ```bash
    git clone https://github.com/unb-mds/2026-1-Mapa_L.I.L.A.S.git
    cd 2026-1-Mapa_L.I.L.A.S
    docker-compose up --build -d
    ```

=== "Comandos (Windows)"

    ```powershell
    git clone https://github.com/unb-mds/2026-1-Mapa_L.I.L.A.S.git
    cd 2026-1-Mapa_L.I.L.A.S
    docker-compose up --build -d
    ```

> Após os containers subirem, o frontend estará disponível em `http://localhost:3000` e a API em `http://localhost:8000`.