git add .
git commit -m "docs: substituir arquivos PDF por documentação MkDocs"
git push# Implementação Dashboard

## 1. Resumo

A arquitetura de software será baseada em extração de dados e APIs próprias, criada para gerar os dashboards interativos do portal de Monitoramento Legislativo de Feminicídio.

Em vez de o site (Frontend) buscar as informações de leis diretamente nas APIs da Câmara e do Senado toda vez que o usuário clica em um botão, nosso sistema fará o "download" desses dados antes, organizará tudo no nosso próprio banco de dados, e o nosso site consumirá apenas os dados já mastigados da nossa própria API.

## 2. Importância da Arquitetura

Essa separação é indispensável para garantir que o projeto funcione sem travar. APIs governamentais costumam ter limites de requisição (*rate limits*), formatos de resposta diferentes e, muitas vezes, são lentas.

Se não tivermos essa arquitetura:

- O dashboard demoraria muitos segundos (ou minutos) para carregar.
- O sistema não conseguiria unificar leis do Senado e da Câmara no mesmo gráfico facilmente.
- O site poderia cair se muitos usuários acessassem ao mesmo tempo.

## 3. Como o Sistema Funciona

O fluxo de funcionamento do nosso sistema é dividido em 3 grandes etapas:

### A) ETL (Extração, Transformação e Carga) no Backend

- **Extração:** Um script em Python (FastAPI) bate nas APIs do Senado e Câmara de madrugada.
- **Transformação:** Limpa os dados, remove duplicatas e padroniza tudo (ex: converte siglas de partidos para um formato único).
- **Carga:** Salva tudo no nosso **PostgreSQL**.

### B) A nossa API Interna

- O **FastAPI** disponibiliza rotas (URLs) exclusivas para o nosso site.
- Exemplo: O site pede `GET /api/proposicoes?estado=SP` e o FastAPI responde rapidamente apenas com os números consolidados: `{"2023": 15, "2024": 32}`.

### C) O Frontend (React + Tailwind + Gráficos)

- O **React** constrói a interface e gerencia as escolhas do usuário.
- Quando o usuário muda um filtro (ex: clica na aba "PIZZA"), o React solicita os novos dados para a nossa API e a biblioteca de gráficos redesenha a tela na hora.

## 4. Exemplo da Estrutura de um projeto

Nesse exemplo usa-se duas pastas principais (repositórios) na divisão do projeto:

```
meu-projeto/
│
├── backend/              # Onde fica o FastAPI e o banco de dados
│   ├── main.py           # Arquivo principal da API
│   ├── models.py         # Estrutura das tabelas do Banco
│   ├── database.py       # Conexão com o PostgreSQL
│   └── rotas_graficos.py # Endpoints que devolvem os JSONs
│
└── frontend/             # Onde fica o React
    ├── src/
    │   ├── components/   # NavBar, Filtros, Cards
    │   ├── pages/        # Dashboard.jsx, Home.jsx
    │   └── services/     # Arquivos para chamar a nossa API (Axios/Fetch)
    ├── package.json
    └── tailwind.config.js # Configurações de estilo
```

## 5. Tecnologias e Pré-requisitos

- **PostgreSQL:** Nosso banco de dados relacional. Excelente para fazer contagens e médias rápidas (queries de agregação).
- **FastAPI (Python):** Framework moderno e de altíssima performance para criar nossa API e os scripts de extração.
- **React.js:** Biblioteca JavaScript para criar as interfaces e gerenciar as mudanças de filtros em tempo real.
- **Tailwind CSS:** Framework de CSS para estilizar os botões, cards e layout de forma rápida e responsiva.
- **Recharts ou Chart.js:** Bibliotecas para o React que pegam os nossos dados e desenham os gráficos (barras, rosca, linha) sozinhos.

## 6. Vantagens e desvantagens

**Vantagens:**

- Altíssima velocidade para o usuário final.
- Controle total sobre os dados (se a API do governo cair, nosso site continua no ar com os dados do dia anterior).
- Separação clara de tarefas na equipe (quem manja de Python fica no Back, quem manja de layout fica no Front).
- Layout super profissional e navegação fluida.

**Desvantagens:**

- Exige modelar um banco de dados próprio.
- Precisamos criar scripts que rodam em segundo plano (*background jobs*) para manter o banco atualizado.

## Links úteis

- **Recharts (Gráficos para React):** <https://recharts.org/>
