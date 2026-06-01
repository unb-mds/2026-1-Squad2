# 🐳 Docker e Containerização

Para garantir que o **Mapa L.I.L.A.S.** tenha um ambiente de desenvolvimento e produção padronizado, confiável e fácil de ser executado, utilizamos o **Docker** e o **Docker Compose**. 

Isso resolve problemas clássicos como *"na minha máquina funciona"*, empacotando as aplicações e suas dependências (banco de dados, bibliotecas, ferramentas de sistema) em containers isolados.

---

## Estrutura do Docker Compose

O projeto é orquestrado através do arquivo `docker-compose.yml` localizado na raiz do repositório. Ele gerencia três serviços principais que se comunicam em uma rede interna:

### 1. `db` (PostgreSQL)
- **Imagem:** `postgres:15`
- **Função:** Banco de dados relacional principal da aplicação.
- **Armazenamento:** Utiliza um *volume* chamado `postgres_data` mapeado para `/var/lib/postgresql/data` para garantir que os dados persistam mesmo se o container for desligado.
- **Healthcheck:** Configurado para verificar a disponibilidade do banco (`pg_isready`) antes de liberar outros serviços que dependem dele.

### 2. `backend` (FastAPI / Python)
- **Build:** Construído a partir do diretório `./backend`.
- **Função:** API REST que fornece os dados legislativos, interage com o banco e serve a aplicação React.
- **Porta:** Exposta na porta `8000` (acessível via `http://localhost:8000`).
- **Dependências:** O backend só inicia após o container do banco de dados (`db`) estar saudável (*service_healthy*).
- **Variáveis de Ambiente:** Carregadas a partir do arquivo `./backend/.env`.
- **Volumes:** O código local em `./backend` é mapeado para `/app` no container, permitindo o *hot-reload* (atualização automática ao salvar arquivos).

### 3. `frontend` (React / Vite)
- **Build:** Construído a partir do diretório `./frontend`.
- **Função:** Interface web para interação do usuário com os dados e dashboards.
- **Porta:** Exposta na porta `5173` (acessível via `http://localhost:5173`).
- **Dependências:** O frontend depende do `backend` estar rodando para ser iniciado.
- **Volumes:** O código fonte em `./frontend` é mapeado para `/app`, com exceção de `node_modules` que roda encapsulado no container para não misturar dependências da máquina host.

---

## Como Rodar o Projeto

Com o Docker e Docker Compose instalados na sua máquina, basta executar o seguinte comando na raiz do repositório:

```bash
docker-compose up --build
```

O argumento `--build` força a criação ou recriação das imagens das aplicações. Após o processo de build, os três containers subirão na seguinte ordem: `db` ➔ `backend` ➔ `frontend`.

Para parar a execução, utilize o atalho `Ctrl + C` no terminal ou rode:

```bash
docker-compose down
```

*(Adicione a flag `-v` ao comando `down` se você também quiser excluir permanentemente os dados gravados no banco de dados local).*
