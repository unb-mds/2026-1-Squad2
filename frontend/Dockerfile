# Usa uma imagem leve do Node
FROM node:22-alpine

WORKDIR /app

# Copia os arquivos de dependências primeiro (otimiza o cache)
COPY package*.json ./

# Instala as dependências (incluindo React e Tailwind)
RUN npm install

# Copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta padrão do Vite/React
EXPOSE 5173

# Comando para rodar o projeto em modo desenvolvimento
CMD ["npm", "run", "dev", "--", "--host"]