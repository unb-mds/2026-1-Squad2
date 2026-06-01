# O que são as Skills?

As skills são arquivos que contêm instruções para o Claude Code ou Cursor.

Abaixo estão as skills que utilizamos no projeto:

- context-handoff: 
Como utilizar na prática:
Se você estiver usando o Claude Code ou Cursor: Adicione o arquivo ao diretório de skills ou regras do projeto. Basta digitar /context-handoff no terminal ou chat.

Se estiver usando ChatGPT ou Gemini: Copie a skill e envie a seguinte mensagem: "Incorpore esta skill. A partir de agora, quando eu disser /context-handoff, você deve gerar a saída conforme as instruções."

Na nova sessão: Basta colar o output gerado pela skill e dizer: "Este é o nosso contexto inicial. Retome o trabalho a partir do [PRÓXIMO PASSO IMEDIATO]."