# SPEC — Página de Projetos de Lei (L.I.L.A.S.)

> **Versão:** 1.0  
> **Release:** Release 1  
> **Responsável:** Equipe MDS 2026.1  
> **Status:** Pronto para implementação

---

## 1. Objetivo da Página

A página **Projetos de Lei** é o núcleo de consulta da plataforma L.I.L.A.S. Ela exibe uma listagem paginada de proposições legislativas relacionadas ao combate ao feminicídio e aos direitos da mulher. O usuário deve ser capaz de buscar, filtrar, ordenar e navegar pelos projetos, chegando a um card com informações suficientes para decidir se quer ver os detalhes completos.

---

## 2. Stack e Restrições

| Item | Decisão |
|---|---|
| Framework | React (JSX) |
| Estilização | TailwindCSS |
| Gerenciamento de estado | `useState` + `useEffect` (sem Redux por enquanto) |
| Requisições HTTP | `fetch` nativo ou `axios` |
| Roteamento | React Router (já configurado no projeto) |
| Backend | FastAPI — endpoints descritos na Seção 6 |
| Autenticação | Não requerida nesta página |
| Responsividade | Obrigatória (mobile-first) |

---

## 3. Estrutura Visual da Página

A página é composta por **4 regiões principais**:

```
┌─────────────────────────────────────────────────────┐
│  [NavBar]  INICIO | GRÁFICOS | PROJETOS DE LEI      │
├─────────────────────────────────────────────────────┤
│  [Header da Página]                                  │
│  Título: "Projetos de Lei"                           │
│  Subtítulo descritivo                                │
├─────────────────────────────────────────────────────┤
│  [Barra de Filtros]                                  │
│  Busca por texto | Autor | Partido | UF | Status | Ano │
│  Botões: LIMPAR / APLICAR FILTROS                    │
├─────────────────────────────────────────────────────┤
│  [Barra de Resultados]                               │
│  "X Projetos Encontrados"  |  Ordenar por: [select] │
├─────────────────────────────────────────────────────┤
│  [Grid de Cards]                                     │
│  Layout: 3 colunas (desktop) / 2 (tablet) / 1 (mobile) │
├─────────────────────────────────────────────────────┤
│  [Paginação]                                         │
│  ← 1 2 3 ... 15 →                                   │
├─────────────────────────────────────────────────────┤
│  [Footer]                                            │
└─────────────────────────────────────────────────────┘
```

---

## 4. Componentes Detalhados

### 4.1 NavBar

- Logo `L.I.L.A.S.` à esquerda (roxo, bold).
- Links de navegação: `INICIO`, `GRÁFICOS`, `PROJETOS DE LEI`.
- Link ativo sublinhado e em roxo (`#5B4FCF` ou similar).
- Sticky no topo ao rolar.

---

### 4.2 Header da Página

- **Título H1:** "Projetos de Lei" — fonte grande, cor roxa.
- **Subtítulo:** "Explore a base de dados legislativa. Utilize os filtros avançados para encontrar proposições específicas por autoria, tema ou status atual."

---

### 4.3 Barra de Filtros

Campos disponíveis:

| Campo | Tipo | Placeholder / Opções |
|---|---|---|
| Palavra-chave ou número | `<input type="text">` | Ícone de lupa + placeholder vazio |
| Autor | `<select>` | Lista dinâmica vinda da API |
| Partido | `<select>` | Lista dinâmica vinda da API |
| UF | `<select>` | Lista estática dos 27 estados |
| Status | `<select>` | `Em Tramitação`, `Aprovado`, `Arquivado` |
| Ano | `<select>` | Anos disponíveis (ex.: 2020–2026) |

**Botões:**
- `LIMPAR` — outline, limpa todos os filtros e recarrega a listagem padrão.
- `APLICAR FILTROS` — preenchido roxo, dispara nova requisição à API com os filtros ativos.

**Comportamento:**
- Os filtros **não disparam requisição automaticamente** ao mudar — somente ao clicar em `APLICAR FILTROS`.
- `LIMPAR` reseta todos os campos para o estado inicial e recarrega os projetos sem filtro.

---

### 4.4 Card de Projeto de Lei

Cada card exibe:

```
┌──────────────────────────────────────────────┐
│ [CASA LEGISLATIVA]          [BADGE DE STATUS] │
│ PL 123/2023                                  │
│ 👤 Sen. Ana Soares (MDB - MG)                │
│                                              │
│ Altera a Lei Maria da Penha para tipificar   │
│ o monitoramento eletrônico do agressor em    │
│ casos de risco de feminicídio.               │
│                                              │
│ ÚLTIMA ATUALIZAÇÃO        VER DETALHES →     │
│ 📅 15 Out 2023                               │
└──────────────────────────────────────────────┘
```

**Especificação dos campos:**

| Campo | Fonte de dados | Observação |
|---|---|---|
| Casa Legislativa | `casa` | `"SENADO FEDERAL"` ou `"CÂMARA DOS DEPUTADOS"` |
| Número do PL | `numero` + `ano` | Ex.: `PL 123/2023` |
| Autor | `autor_nome` + `autor_partido` + `autor_uf` | Ex.: `Sen. Ana Soares (MDB - MG)` |
| Ementa | `ementa` | Texto truncado em 3 linhas com `line-clamp-3` |
| Data de atualização | `ultima_atualizacao` | Formatar como `DD Mmm YYYY` |
| Status | `status` | Ver badges abaixo |
| Link detalhes | `id` | Navega para `/projetos/:id` |

**Badges de Status:**

| Valor do campo `status` | Texto exibido | Cor |
|---|---|---|
| `em_tramitacao` | EM TRAMITAÇÃO | Amarelo (`bg-yellow-400 text-yellow-900`) |
| `aprovado` | APROVADO | Verde (`bg-green-500 text-white`) |
| `arquivado` | ARQUIVADO | Vermelho (`bg-red-500 text-white`) |

**Interação:**
- Hover no card: leve elevação com sombra (`shadow-lg`, `scale-[1.01]`).
- Clique em `VER DETALHES →` navega para a página de detalhes do PL (fora do escopo desta Release).

---

### 4.5 Barra de Resultados

- Texto à esquerda: `"X Projetos Encontrados"` — onde X é o `total` retornado pela API.
- Dropdown à direita: `Ordenar por:` com opções:
  - `Mais Recentes` (padrão)
  - `Mais Antigos`
  - `Menor para Maior (Número do PL)`

**Comportamento:** ao mudar a ordenação, dispara nova requisição imediatamente (sem precisar clicar em Aplicar).

---

### 4.6 Paginação

- Exibe: `← 1 2 3 ... [última] →`
- Página atual destacada em roxo (círculo preenchido).
- Botões `←` e `→` desabilitados quando na primeira/última página.
- Ao clicar em um número, rola o scroll para o topo da listagem.
- Controla o parâmetro `page` enviado à API.

---

### 4.7 Footer

- Logo `L.I.L.A.S.` à esquerda, fundo escuro.
- Links: `Senado Federal`, `Câmara dos Deputados`, `Sobre Nós`, `Privacidade`, `Contato`.
- Texto de direitos: `© 2026 L.I.L.A.S. - Monitoramento Legislativo. Todos os direitos reservados.`

---

## 5. Estados da Interface (UI States)

A listagem de cards deve tratar obrigatoriamente os seguintes estados:

### 5.1 Carregando (`loading`)
- Exibir **skeleton cards** (3 placeholders animados com `animate-pulse`) no lugar dos cards reais.
- A barra de resultados exibe `"Carregando..."`.

### 5.2 Resultado com dados (`success`)
- Exibe os cards normalmente.
- Exibe contagem e paginação.

### 5.3 Nenhum resultado (`empty`)
- Exibir mensagem centralizada:  
  `"Nenhum projeto encontrado com os filtros selecionados."`
- Botão secundário: `Limpar filtros`.
- Sem paginação.

### 5.4 Erro de rede (`error`)
- Exibir mensagem:  
  `"Não foi possível carregar os projetos. Tente novamente."`
- Botão: `Tentar novamente` — dispara a mesma requisição.

---

## 6. Contrato de API (FastAPI)

### Endpoint principal

```
GET /api/projetos-de-lei
```

**Query parameters:**

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `page` | `int` | Não (padrão: 1) | Número da página |
| `per_page` | `int` | Não (padrão: 10) | Itens por página |
| `keyword` | `string` | Não | Busca em número e ementa |
| `autor` | `string` | Não | Nome do autor |
| `partido` | `string` | Não | Sigla do partido |
| `uf` | `string` | Não | Sigla do estado (ex.: `MG`) |
| `status` | `string` | Não | `em_tramitacao`, `aprovado`, `arquivado` |
| `ano` | `int` | Não | Ano do PL |
| `ordenar` | `string` | Não | `recentes`, `antigos`, `numero_asc` |

**Exemplo de requisição:**
```
GET /api/projetos-de-lei?page=1&per_page=10&status=em_tramitacao&ordenar=recentes
```

**Estrutura esperada da resposta (JSON):**

```json
{
  "total": 145,
  "page": 1,
  "per_page": 10,
  "total_pages": 15,
  "projetos": [
    {
      "id": "pl-123-2023",
      "numero": "123",
      "ano": 2023,
      "casa": "SENADO FEDERAL",
      "status": "em_tramitacao",
      "autor_nome": "Sen. Ana Soares",
      "autor_partido": "MDB",
      "autor_uf": "MG",
      "ementa": "Altera a Lei Maria da Penha para tipificar o monitoramento eletrônico do agressor em casos de risco de feminicídio.",
      "ultima_atualizacao": "2023-10-15"
    }
  ]
}
```

### Endpoint de metadados para filtros (opcional mas recomendado)

```
GET /api/projetos-de-lei/filtros
```

**Resposta:**
```json
{
  "autores": ["Sen. Ana Soares", "Dep. Carlos Mendes"],
  "partidos": ["MDB", "PL", "PSDB"],
  "ufs": ["MG", "RJ", "SP"],
  "anos": [2020, 2021, 2022, 2023, 2024, 2025, 2026]
}
```

---

## 7. Estrutura de Componentes React

```
src/
├── pages/
│   └── ProjetosLei/
│       └── index.jsx          ← página principal (orquestra tudo)
├── components/
│   ├── NavBar/
│   │   └── index.jsx
│   ├── ProjetosLei/
│   │   ├── FiltrosBar.jsx     ← barra de filtros completa
│   │   ├── CardPL.jsx         ← card individual de um PL
│   │   ├── CardPLSkeleton.jsx ← versão loading do card
│   │   ├── ListagemPL.jsx     ← grid de cards + estados
│   │   └── Paginacao.jsx      ← controle de páginas
│   └── Footer/
│       └── index.jsx
├── hooks/
│   └── useProjetosLei.js      ← lógica de fetch + estado
└── services/
    └── api.js                 ← configuração base do axios/fetch
```

---

## 8. Critérios de Aceite (Release 1)

Para que a página seja considerada **pronta** na Release 1, ela deve:

- [ ] Renderizar a listagem de PLs consumindo o endpoint real da API
- [ ] Exibir corretamente os 3 badges de status com as cores certas
- [ ] Filtros funcionando: palavra-chave, partido, UF, status e ano
- [ ] Botões `LIMPAR` e `APLICAR FILTROS` com comportamentos corretos
- [ ] Ordenação por `Mais Recentes`, `Mais Antigos` e `Menor para Maior`
- [ ] Paginação funcional com scroll para o topo ao trocar de página
- [ ] Estado de loading com skeleton cards
- [ ] Estado de lista vazia com mensagem e botão de limpar filtros
- [ ] Estado de erro com botão de retry
- [ ] Layout responsivo (mobile, tablet e desktop)
- [ ] Fiel ao protótipo de alta fidelidade (cores, tipografia, espaçamentos)

---

## 9. Paleta de Cores (extraída do protótipo)

```css
--color-primary:    #5B4FCF;  /* roxo principal — botões, badges ativos, links */
--color-primary-dark: #4338CA; /* hover dos botões roxos */
--color-bg:         #FFFFFF;
--color-surface:    #F9FAFB;  /* fundo dos cards */
--color-border:     #E5E7EB;
--color-text:       #111827;
--color-text-muted: #6B7280;
--color-footer-bg:  #1F2937;
--color-badge-green:  #22C55E;
--color-badge-yellow: #FBBF24;
--color-badge-red:    #EF4444;
```

---

*Este documento deve ser versionado junto ao repositório do projeto e atualizado sempre que houver mudanças no contrato de API ou no protótipo.*
