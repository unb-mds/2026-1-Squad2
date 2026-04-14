# Conceitos Importantes + Introdução ao PostgreSQL
## O que é PostgreSQL?
PostgreSQL é um sistema de gerenciamento de banco de dados relacional open source, conhecido por sua robustez, confiabilidade e suporte a funcionalidades avançadas.

Ele também suporta dados em formato JSON, sendo bastante flexível para diferentes tipos de aplicações.

## Conceitos importantes
1. Banco de Dados Relacional
Organiza os dados em tabelas (linhas e colunas) e utiliza chaves para criar relações entre elas.

2. SQL (Structured Query Language)
Linguagem usada para manipular dados:

- ``SELECT`` → consultar
- ``INSERT`` → inserir
- ``UPDATE`` → atualizar
- ``DELETE`` → remover
3. Normalização
Ajuda a evitar redundância e manter consistência nos dados.

4. Índices
Melhoram a performance de leitura, mas podem impactar operações de escrita.

5. Transações (ACID)
Garantem confiabilidade nas operações:

- Atomicidade
- Consistência
- Isolamento
- Durabilidade
### Vantagens
- Open source e gratuito
- Alta confiabilidade
- Suporte completo a transações (ACID)
- Extensível (funções, tipos e extensões)
- Suporte a JSON/JSONB
- Comunidade ativa
- Excelente para consultas complexas
### Desvantagens
- Configuração inicial mais complexa
- Maior consumo de recursos
- Curva de aprendizado mais alta
- Escalabilidade horizontal mais difícil
- Pode ser excessivo para projetos pequenos
## Quando usar?
*Indicado para:*

Projetos com dados relacionais complexos
Necessidade de consistência e integridade
Aplicações robustas
*Evitar ou avaliar melhor quando:*

Projetos muito simples
Necessidade de escalabilidade horizontal extrema
Casos onde baixa latência é prioridade absoluta


# 📌 Conteúdos a serem estudados

## 🟢 SQL (Essencial)
SELECT, INSERT, UPDATE, DELETE
WHERE, ORDER BY, GROUP BY
JOIN (INNER, LEFT, RIGHT)
## 🟢 Modelagem de Dados
Normalização (1FN, 2FN, 3FN)
Tipos de relacionamento (1:1, 1:N, N:N)
Tabela associativa (tabela ponte)
# 🟢 Performance
Índices (INDEX)
EXPLAIN
Boas práticas de consultas

# 🔗 Link de estudo
https://youtu.be/9cAKQWodpvM?si=05CHR1vfH3fLBak0 