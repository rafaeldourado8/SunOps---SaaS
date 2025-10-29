# 1. Use uma imagem base slim oficial do Python
FROM python:3.10-slim

# 2. Defina o diretório de trabalho dentro do container
WORKDIR /app

# 3. Instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copie o arquivo de requisitos PRIMEIRO
COPY requirements.txt .

# 5. Instale as bibliotecas Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
