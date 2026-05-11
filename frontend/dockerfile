# parte 1: Construção do frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Parte 1: Configuração do backend
FROM python:3.11-slim
WORKDIR /app

# Dependencias do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Dependencias do python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do backend
COPY ./backend ./pasta_do_backend

# Copiar os arquivos estáticos do frontend para o backend
COPY --from=frontend-builder /aplicacao/frontend/dist ./backend/staticos

# Expor as portas necessárias para o backend e frontend
EXPOSE 8000 8080 

# Variáveis de ambiente
ENV FLASK_APP=pipipi
ENV PYTHONUNBUFFERED=1

# Serviços
CMD ["sh", "-c", "python -m uvicorn backend.api:app --host 0.0.0.0 --port 8000 & python backend/app.py"]

# Este dockerfile é feito de forma básica e ainda pode ser melhorado. 