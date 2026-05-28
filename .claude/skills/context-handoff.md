# context-handoff

## Descrição
Comprime a sessão atual de chat em um documento de estado de formato rígido e ultra-denso. O objetivo é transferir o contexto para uma nova sessão ou agente, economizando o máximo de tokens possível sem perder histórico de decisões, estado da arquitetura ou os próximos passos imediatos.

## Instruções
Quando o usuário solicitar `/context-handoff` ou pedir para resumir a sessão para transferência, você DEVE analisar todo o histórico desta conversa e gerar uma resposta em formato Markdown seguindo estritamente as regras abaixo.

### 1. Mentalidade "Caveman" (Modo Ultra-Denso)
- Você está proibido de usar saudações, preâmbulos, transições ou conclusões (ex: "Aqui está o seu resumo...", "Espero que ajude!").
- Remova adjetivos e advérbios desnecessários. Use frases curtas, listas e linguagem pragmática.
- Otimize implacavelmente para redução de tokens.
- Comunique-se como um engenheiro sênior passando o bastão em 30 segundos.

### 2. Estrutura Obrigatória
A sua saída deve conter EXATAMENTE estas quatro seções, e nada mais:

#### [OBJETIVO DA SESSÃO]
- 1 a 2 frases curtas definindo a meta principal que estávamos perseguindo.

#### [DECISÕES & LINGUAGEM]
- Padrões arquiteturais definidos.
- Ferramentas, bibliotecas ou frameworks escolhidos/alterados.
- "Linguagem Ubíqua": termos de domínio ou nomenclaturas específicas que concordamos em usar (ex: "Usar 'Client' ao invés de 'User'").

#### [ESTADO ATUAL (O QUE ESTÁ FEITO)]
- Lista do que já foi resolvido, implementado ou refatorado.
- Mencione os nomes exatos dos arquivos (`src/caminho/arquivo.ext`) e as rotas/funções cruciais modificadas.
- Se houver um bloco de código vital de até 15 linhas que encapsule a essência do estado atual, inclua-o.

#### [PRÓXIMO PASSO IMEDIATO (O GARGALO)]
- Onde paramos exatamente.
- O erro de compilação atual (inclua a stack trace curta se houver), o teste que está falhando, ou a próxima feature a ser construída.
- Seja cirúrgico: o que o próximo agente deve fazer na linha 1?

### 3. Exemplo de Saída Esperada

## [OBJETIVO DA SESSÃO]
Migrar API de Express para FastAPI e implementar autenticação JWT.

## [DECISÕES & LINGUAGEM]
- Framework: FastAPI (Python).
- DB: PostgreSQL via SQLAlchemy 2.0 (async).
- Nomenclatura: 'Tenant' será usado para isolamento de empresas.

## [ESTADO ATUAL]
- `main.py`: Setup base concluído.
- `database.py`: Pool de conexões async testado e funcional.
- `routes/auth.py`: Rota POST `/login` criada.

## [PRÓXIMO PASSO IMEDIATO]
- A rota `/login` está retornando HTTP 500.
- Falha no Pydantic ao validar a model `TenantLogin`.
- Tarefa: Corrigir erro de tipagem no schema `schemas/tenant.py` e criar o primeiro teste de integração (TDD).