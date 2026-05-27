# Estudo Técnico: Adoção do FastAPI e possível Integração com PostgreSQL

## 1. Nivelamento de Conceitos

- **O que é uma API (Application Programming Interface)?**
  Em termos simples, uma API é uma ponte de comunicação. No contexto web (RESTful APIs), ela atua como o "garçom" do nosso sistema: ela recebe os pedidos do front-end (como uma interface construída em React), processa as regras de negócio, busca ou salva os dados no banco de dados e entrega a resposta formatada (geralmente em JSON) de volta ao cliente.

- **O que é um Framework?**
  É uma estrutura base, um conjunto de ferramentas e bibliotecas pré-configuradas que resolve problemas comuns de desenvolvimento (como roteamento de URLs, segurança e conexão com banco de dados). Em vez de escrever todo o código do zero para interpretar requisições HTTP, o framework nos fornece os blocos de montar, permitindo que a equipe foque apenas nas regras de negócio do projeto.

## 2. Vantagens do FastAPI

1. **Alta Performance:** É um dos frameworks Python mais rápidos disponíveis, comparável a NodeJS e Go. Ele suporta programação assíncrona (`async`/`await`) nativamente, o que é excelente para lidar com múltiplas requisições ao banco de dados sem travar o servidor.
2. **Validação Automática de Dados:** Utiliza a biblioteca Pydantic. Se a nossa rota espera receber um número inteiro e o usuário enviar uma string, o FastAPI bloqueia a requisição automaticamente e retorna uma mensagem de erro clara, sem que precisemos escrever código extra para isso.
3. **Documentação Automática (Swagger e ReDoc):** Assim que você cria uma rota, o FastAPI gera automaticamente uma página web interativa onde é possível ler a documentação da API e testar os endpoints diretamente do navegador.
4. **Curva de Aprendizado e Produtividade:** O código é extremamente enxuto e legível. Requer muito menos "código boilerplate" (código repetitivo de configuração) do que frameworks maiores.

## 3. Por que deveríamos usar no Projeto?

A adoção do FastAPI traz benefícios diretos para o fluxo de trabalho da disciplina:

- **Integração Front e Back:** A documentação automática (Swagger) permite que o time de front-end veja exatamente quais dados enviar e o que vão receber, sem precisar perguntar ao time de back-end o tempo todo.
- **Agilidade nas Sprints:** Como ele reduz a quantidade de código necessário para criar um endpoint (CRUD), a equipe consegue entregar histórias de usuário mais rapidamente a cada iteração.
- **Facilidade de Testes:** O framework foi desenhado para ser facilmente testável (usando `pytest`).

## 4. Integração com PostgreSQL (Funcionalidades Básicas)

Para conectar o FastAPI (que "fala" Python) ao PostgreSQL (que "fala" SQL), nós não escrevemos comandos SQL crus diretamente dentro das nossas rotas. Em vez disso, utilizamos uma arquitetura baseada em um **ORM (Object-Relational Mapper)**, sendo o **SQLAlchemy** a escolha mais comum.

O fluxo de funcionamento teórico ocorre nas seguintes etapas:

1. **O "Tradutor" (ORM):** O ORM funciona como uma ponte. Ele nos permite representar as tabelas do PostgreSQL como simples "Classes" em Python. Assim, manipular um dado no banco torna-se tão fácil quanto modificar um objeto no código.
2. **A Requisição (Entrada):** O front-end envia uma requisição para a API (ex: `POST /usuarios/` com os dados de um novo cadastro). O FastAPI intercepta essa chamada e valida se os dados estão no formato correto.
3. **A Transação Segura:** O FastAPI repassa esses dados para o ORM. O ORM, de forma invisível e segura (protegendo contra ataques como SQL Injection), traduz nosso objeto Python para um comando `INSERT` em SQL puro.
4. **A Execução:** Esse comando chega ao PostgreSQL, que valida suas próprias regras de integridade (ex: "esse e-mail já existe?"), grava a informação no disco de forma permanente e retorna uma confirmação de sucesso.
5. **A Resposta (Saída):** O ORM recebe a resposta do banco de dados, converte de volta para o contexto do Python e o FastAPI finaliza o ciclo, transformando o resultado em um formato JSON amigável para devolver ao front-end.

## 5. Sites para estudos

- <https://fastapidozero.dunossauro.com/estavel/>
- <https://fastapi.tiangolo.com/learn/>
- <https://www.youtube.com/watch?v=BtIy2aD8k_w&list=PLpdAy0tYrnKy3TvpCT-x7kGqMQ5grk1Xq>
