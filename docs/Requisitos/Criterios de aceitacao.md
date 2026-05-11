# Critérios de Aceitação - Mapa L.I.L.A.S

Este documento detalha os critérios de aceitação técnicos para as funcionalidades de front-end e back-end mapeadas nos épicos do sistema de monitoramento legislativo.

---

## Épico 1: Visualização de Dashboards
**Funcionalidades:** Geração de gráficos, filtros cruzados de dados e alternância de tipos de visualização.

### 1. Carregamento e Estado Inicial
* A página deve realizar uma requisição (fetch) à API no momento da montagem do componente para buscar um dataset padrão.
* O sistema deve renderizar um componente de gráfico padrão alimentado por esses dados iniciais.
* O front-end deve exibir um indicador de carregamento (spinner ou skeleton) enquanto aguarda a resposta da API.

### 2. Implementação dos Filtros de Dados
* A interface deve conter componentes de seleção (dropdowns, datepickers, etc.) mapeados para: Estado, Partido, Gênero dos Autores, Data, Status e Tema (Feminicídio, Mulher, Violência doméstica).
* O front-end deve gerenciar o estado dos filtros e formatar os parâmetros (query strings) para o envio à API.

### 3. Validação de Seleção de Dados (Bloqueio de UI)
* Se o estado de todos os filtros de dados for nulo ou vazio, o gráfico não deve ser renderizado.
* A interface deve bloquear novas buscas e exibir um helper text exigindo que pelo menos um filtro de dado seja selecionado.

### 4. Alternância do Tipo de Gráfico
* A página deve incluir um seletor visual para: Rosca, Pizza, Barra, Coluna e Mapa do Brasil por estado.
* A alteração neste seletor **não deve** disparar uma nova requisição ao back-end.
* O sistema deve re-renderizar o gráfico dinamicamente com o novo formato, reaproveitando o payload já armazenado no estado local.

### 5. Tratamento de Retorno Singular (Fallback Numérico)
* Se a busca resultar em um dado absoluto único (sem subcategorias para comparação cruzada), o gráfico deve ser ocultado.
* O front-end deve renderizar um componente de Card/Badge destacando apenas o número absoluto e sua respectiva legenda.

### 6. Tratamento de Retorno Vazio (Empty State)
* Se a API retornar um array vazio `[]`, o sistema deve ocultar a área do gráfico.
* Deve ser renderizado um *Empty State* informando que nenhuma proposta corresponde aos filtros.

---

## Épico 2: Home (Landing Page)
**Funcionalidades:** Painel inicial com indicadores, estatísticas resumidas e navegação.

### 1. Painel de Indicadores Gerais (KPIs)
* O sistema deve realizar uma requisição para buscar as métricas globais e exibir em Cards os totais de:
  * Projetos gerais.
  * Projetos recém-cadastrados.
  * Projetos em tramitação.
  * Projetos aprovados e arquivados.

### 2. Exibição de Gráficos de Overview
* A página deve renderizar componentes gráficos simplificados com dados estatísticos pré-selecionados, sem exigir aplicação de filtros pelo usuário nesta tela.

### 3. Rankings e Métricas Específicas
* A interface deve exibir uma lista categorizada dos "Top 5 Estados" com maior volume de propostas.
* A interface deve exibir a lista dos "Parlamentares mais ativos", ordenada de forma decrescente.
* O sistema deve calcular e exibir o "Tempo Médio de Tramitação" global.

### 4. Timeline de Movimentações
* O front-end deve renderizar um componente de feed consumindo uma listagem limitada das movimentações legislativas mais recentes, ordenadas por data decrescente.

### 5. Navegação (Calls to Action)
* A interface deve conter CTAs (botões/links) de destaque direcionando para:
  * A rota da página de Pesquisa de Projetos de Lei (PLs).
  * A rota da página de Geração de Dashboards.

### 6. Informações Institucionais (Footer)
* O final da página deve renderizar um rodapé contendo informações explicativas sobre o projeto e dados de contato.

### 7. Resiliência e Tratamento de Falhas
* Em caso de falha crítica nas APIs (500, timeout), a página não deve quebrar silenciosamente.
* O sistema deve exibir uma tela de falha ou disparar um recarregamento automático (`window.location.reload()`).

---

## Épico 3: Consulta de Proposições
**Funcionalidades:** Busca textual, aplicação de filtros e listagem paginada de projetos de lei.

### 1. Campos de Busca e Filtros Avançados
* A interface deve disponibilizar um campo de input para "Busca Livre" (texto).
* O sistema deve renderizar componentes de seleção para: Ano/Período, Partido, Estado e Status (Apresentação, Comissão, Votação e Sanção).

### 2. Processamento da Busca
* O front-end deve concatenar a busca livre com os filtros avançados e enviá-los como query params à API.
* A API deve aplicar o operador lógico AND entre os filtros para refinar o resultado.

### 3. Listagem e Paginação Restrita
* O sistema deve implementar paginação estrita, exibindo **exatamente o máximo de 5 PLs por página**.
* O front-end deve disponibilizar controles de navegação (Próximo, Anterior e Página Atual).

### 4. Navegação de Detalhamento
* Cada card/item da lista de resultados deve ser clicável.
* Ao clicar, o sistema deve realizar o roteamento do usuário para a página de detalhes da proposição usando seu respectivo ID (ex: `/pl/:id`).

### 5. Tratamento de Ausência de Resultados
* Se a API retornar um conjunto vazio, a lista de PLs não deve ser renderizada.
* O sistema deve exibir um *Empty State* solicitando alteração dos filtros e disponibilizar um botão de "Limpar Filtros" (reset de estado).

---

## Épico 4: Detalhamento Legislativo
**Funcionalidades:** Exibição completa de dados de uma PL, histórico, download e compartilhamento.

### 1. Roteamento e Carregamento de Dados
* A página deve ser acessada via rota dinâmica (`/pl/:id`).
* O front-end deve extrair o ID da URL e disparar uma requisição GET para buscar os dados agregados da proposição.

### 2. Exibição de Metadados
* A interface deve renderizar os textos da "Ementa Completa" e "Explicação da Ementa".
* Deve identificar claramente o Autor e o Relator.
* O status atual da tramitação deve ser exibido em destaque (badge visual).

### 3. Linha do Tempo do Histórico
* O front-end deve renderizar uma *Timeline* mapeando o array de tramitação retornado pela API, ordenado de forma cronológica.

### 4. Download do PDF
* A página deve conter um botão "Baixar Documento Inicial" ou "Ver PDF".
* O clique deve acionar o download ou abrir o PDF em nova aba via URL fornecida pela API.

### 5. Compartilhamento
* A interface deve incluir um botão "Compartilhar".
* O sistema deve copiar o link atual para a área de transferência (Clipboard API) ou acionar o compartilhamento nativo do dispositivo (Web Share API) com feedback de sucesso.

### 6. Navegação Contextual
* A página deve incluir um link rápido para a tela de Dashboards, mantendo o fluxo analítico do usuário.

### 7. Tratamento de Falha Crítica
* Se a API não responder (timeout) ou retornar erro 500, a interface não deve ficar em loop de carregamento.
* O front-end deve exibir um *Error State* em tela cheia informando a indisponibilidade e oferecendo um botão "Tentar Novamente".