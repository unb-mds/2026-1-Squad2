---
name: "Nova Tarefa / Funcionalidade"
about: "Template padrão para abertura de issues fullstack, backend ou frontend do Mapa L.I.L.A.S"
title: "[FEAT/FIX/CHORE]: <título curto e descritivo>"
labels: ''
assignees: ''
---

## Contexto e Motivação
**Descrição:** ## Relação com o SDD (CLAUDE.md)
- **Funcionalidade:** [ex: 1. Coleta e Normalização / 2. Portal Público / 3. Análise SCRUM]
- **Depende de outra issue?** [ex: #12, ou Nenhuma]

## Critérios de Aceitação
- [ ] Critério 1 verificável e observável.
- [ ] Critério 2...

---

## Checklist da Constituição L.I.L.A.S
### Backend / Dados (Se aplicável)
- [ ] **Normalização estrita:** Os dados estão sendo convertidos para o modelo único unificado?
- [ ] **Rastreabilidade:** A fonte (Câmara/Senado) e link original estão sendo preservados?
- [ ] **Não duplicidade:** A lógica atualiza/sobrescreve registros existentes em vez de duplicá-los?
- [ ] **Validação Pydantic:** O schema de resposta das APIs externas foi validado antes da ingestão?

### Frontend / UI (Se aplicável)
- [ ] **Filtros Resilientes:** A interface lida bem com a combinação de múltiplos filtros e não quebra se não houver resultados (exibe empty state)?
- [ ] **Clareza nos Indicadores:** Os gráficos, mapas ou métricas possuem rótulos autoexplicativos?
- [ ] **Responsividade:** A interface carrega e funciona corretamente tanto em desktop quanto em mobile?
- [ ] **Padrão React:** Os componentes seguem a nomenclatura `PascalCase` e mantêm o isolamento de domínio (não misturam lógica de request com UI)?

---

## Plano de Ação / Subtarefas (Opcional)
- [ ] Subtarefa de Backend (ex: Criar rota FastAPI `GET /api/v1/indicadores`)
- [ ] Subtarefa de Frontend (ex: Criar componente React `PainelIndicadores.tsx`)
- [ ] Subtarefa de Integração (ex: Conectar o componente de filtros ao endpoint via Axios/Fetch)
- [ ] Testes unitários / Validação visual

## Informações Adicionais