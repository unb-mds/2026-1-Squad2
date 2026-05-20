export const mockProjetos = {
  total: 6,
  page: 1,
  per_page: 6,
  total_pages: 1,
  projetos: [
    {
      id: "pl-123-2023",
      numero: "123",
      ano: 2023,
      casa: "SENADO FEDERAL",
      status: "em_tramitacao",
      autor_nome: "Sen. Ana Soares",
      autor_partido: "MDB",
      autor_uf: "MG",
      ementa:
        "Altera a Lei Maria da Penha para tipificar o monitoramento eletrônico do agressor em casos de risco de feminicídio.",
      ultima_atualizacao: "2023-10-15",
    },
    {
      id: "pl-1234-2022",
      numero: "1234",
      ano: 2022,
      casa: "SENADO FEDERAL",
      status: "aprovado",
      autor_nome: "Sen. Carlos Mendes",
      autor_partido: "PL",
      autor_uf: "RJ",
      ementa:
        "Altera a Lei nº 11.340/2006 (Lei Maria da Penha) para determinar o uso obrigatório de tornozeleira eletrônica para agressores submetidos a medidas protetivas de urgência.",
      ultima_atualizacao: "2023-09-02",
    },
    {
      id: "pl-987-2021",
      numero: "987",
      ano: 2021,
      casa: "CÂMARA DOS DEPUTADOS",
      status: "arquivado",
      autor_nome: "Dep. Ana Costa",
      autor_partido: "MDB",
      autor_uf: "MG",
      ementa:
        "Institui o benefício de pensão especial aos filhos e dependentes menores de dezoito anos de mulheres vítimas do crime de feminicídio no Brasil.",
      ultima_atualizacao: "2023-01-10",
    },
    {
      id: "pl-555-2023",
      numero: "555",
      ano: 2023,
      casa: "SENADO FEDERAL",
      status: "em_tramitacao",
      autor_nome: "Sen. João Lima",
      autor_partido: "PSDB",
      autor_uf: "PR",
      ementa:
        "Cria o Banco Nacional de Dados sobre Feminicídio, com o objetivo de centralizar as informações sobre os casos ocorridos e auxiliar na formulação de políticas públicas.",
      ultima_atualizacao: "2023-11-05",
    },
    {
      id: "pl-302-2022",
      numero: "302",
      ano: 2022,
      casa: "CÂMARA DOS DEPUTADOS",
      status: "aprovado",
      autor_nome: "Dep. Mariana Ferreira",
      autor_partido: "PT",
      autor_uf: "SP",
      ementa:
        "Dispõe sobre a criação de centros de acolhimento para mulheres em situação de violência doméstica e suas crianças dependentes.",
      ultima_atualizacao: "2023-06-20",
    },
    {
      id: "pl-88-2023",
      numero: "88",
      ano: 2023,
      casa: "CÂMARA DOS DEPUTADOS",
      status: "em_tramitacao",
      autor_nome: "Dep. Roberto Nunes",
      autor_partido: "PDT",
      autor_uf: "BA",
      ementa:
        "Estabelece protocolo obrigatório de atendimento às vítimas de violência doméstica nas unidades de pronto atendimento do Sistema Único de Saúde.",
      ultima_atualizacao: "2023-12-01",
    },
  ],
};

export const mockFiltros = {
  partidos: ["MDB", "PL", "PSDB", "PT", "PDT"],
  ufs: ["MG", "RJ", "PR", "SP", "BA"],
  anos: [2021, 2022, 2023],
};