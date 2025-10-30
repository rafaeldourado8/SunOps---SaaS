# Estágio 1: Instalar dependências e rodar o dev server

# Use uma imagem Node.js Alpine (leve)
FROM node:20-alpine AS development

# Defina o diretório de trabalho
WORKDIR /app

# Instale pnpm globalmente
RUN npm install -g pnpm

# Copie os arquivos de definição de dependências
COPY package.json pnpm-lock.yaml ./

# Instale as dependências usando pnpm
# O --frozen-lockfile garante que as versões exatas do lockfile serão usadas
RUN pnpm install --frozen-lockfile

# Copie o restante do código da aplicação
# (Alternativamente, pode usar volumes no docker-compose.yml para hot-reload)
COPY . .

# Exponha a porta padrão do Vite (5173)
EXPOSE 5173

# Comando para iniciar o servidor de desenvolvimento Vite
# O '--host' faz o Vite escutar em todas as interfaces de rede dentro do container
CMD ["pnpm", "run", "dev", "--host"]
