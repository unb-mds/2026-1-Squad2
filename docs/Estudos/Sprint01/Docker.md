# Guia de Estudos: Conceitos Básicos de Docker \
## 1. O que é o Docker?
O Docker é um serviço de virtualização que permite criar e rodar a sua aplicação independentemente do ambiente hospedeiro onde ela está sendo desenvolvida . A sua principal finalidade é resolver o famoso problema do "na minha máquina funciona" . Ele garante que todo o ambiente — bibliotecas, pacotes e configurações do sistema operacional — seja virtualizado de forma coesa, assegurando que o seu código se comporte de maneira exatamente igual em qualquer outro lugar.

Diferença para Máquinas Virtuais (VMs): Diferentemente de uma máquina virtual que exige a instalação de um sistema operacional (OS) completo e isolado para cada aplicação, o container do Docker não possui um sistema operacional interno. Ele reutiliza o kernel do sistema operacional do computador hospedeiro e isola os processos da aplicação . Isso torna a abordagem de containers absurdamente mais ágil e leve do que gerenciar VMs tradicionais.

## 2. Conceitos Fundamentais
Dockerfile: É essencialmente a arquitetura da sua aplicação descrita como código. Um arquivo de texto com as instruções precisas para gerar a imagem Docker .
Imagens: São as plantas ou os pacotes imutáveis gerados a partir do Dockerfile. Elas contêm absolutamente tudo que é necessário para executar a aplicação no sistema .
Containers: É a imagem ganhando vida, isto é, uma instância em execução de uma imagem. Múltiplos containers podem rodar simultaneamente na mesma máquina hospedeira sem interferirem uns nos outros. Como as interfaces de rede do container e da máquina são separadas, você frequentemente precisa realizar o mapeamento de portas (ex: espelhar o que roda na porta interna 8080 do container para a porta 8080 da sua máquina pessoal).
Docker Compose: É uma ferramenta para definir e rodar aplicações Docker de múltiplos contêineres separando as aplicações(Back-end, Front-end, Banco de dados).
## 3. Tutorial: Dockerfile na Prática
Baseado na necessidade do nosso projeto, criaremos o Dockerfile que fará as cópias dos nossos scripts para dentro do container e fará a instalação das bibliotecas de dados. Aqui está um exemplo.

```
# 1. Utiliza uma Imagem base do Python
FROM python:3.11-slim

# Determina onde as coisas acontecerão lá dentro
WORKDIR /app

# 2. Instalação das bibliotecas necessárias via arquivo de requisitos
# (Assegure-se que pandas, scikit-learn, nltk, spacy e hdbscan estejam no requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Cópia de todos os scripts do projeto para dentro do diretório /app do container
COPY . .

# 4. Comando de entrada (Entrypoint) estipulando a execução dos scripts principais
CMD ["python", "script_principal.py"]

```

## 4. Bônus: Orquestrando com Docker Compose
O Dockerfile ensina como construir a caixa de um serviço isolado, mas quando se tem muitas aplicações juntas é preciso de vários contêineres um para Backend, Frontend e Banco de dados.

É aí que o Docker Compose entra. Ele é configurado através de um arquivo chamado docker-compose.yml, que documenta e sobe múltiplos containers de uma vez com uma única instrução:

```
version: '3.8'

services:
  # Serviço 1: O nosso script atual
  app-dados:
    build: . 
    image: cluster-propostas
    volumes:
      - .:/app
    ports:
      - "8080:8080"
  
  # Serviço 2: Um Banco de Dados separado
  database:
    image: postgres:15
    environment:
      POSTGRES_USER: usuario_db
      POSTGRES_PASSWORD: senha123
```
Com esse arquivo estruturado, basta rodar o comando ``docker compose up -d`` no terminal, e a ferramenta fará o download das imagens, criará as redes para que a sua aplicação comunique com o banco e inicializará tudo simultaneamente e em segundo plano (graças a flag ``-d``).

Ao padronizar seus projetos dessa maneira, não haverá mais estresse com configuração. A reprodutibilidade dos resultados alcançados pelo time será impecável.