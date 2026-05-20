FROM python:3.11-slim
WORKDIR /app

# Dependências de sistema para o PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Cache de dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do backend
COPY . .

# Variável para o Python não criar arquivos .pyc e exibir logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# A JOGADA DE MESTRE:
# Copia o script para a raiz do contêiner (fora do /app)
COPY entrypoint.sh /entrypoint.sh

# Remove quebras de linha do Windows (CRLF para LF) e dá permissão de execução
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

# Roda o entrypoint a partir da raiz
ENTRYPOINT ["/entrypoint.sh"]