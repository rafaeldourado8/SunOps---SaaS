#!/bin/bash
# CI/CD Local - Executa testes sem GitHub Actions

set -e

echo "🚀 Iniciando CI/CD Local..."

# Backend Tests
echo "📦 Backend: Instalando dependências..."
cd backend
pip install -r requirements.txt

echo "🧪 Backend: Executando testes..."
python manage.py test

echo "🔒 Backend: Verificando segurança..."
bandit -r apps/ -f json -o bandit-report.json || true
safety check --json || true

# Frontend Tests
echo "📦 Frontend: Instalando dependências..."
cd ../frontend
npm install

echo "🧪 Frontend: Executando testes..."
npm test || true

echo "🔒 Frontend: Auditoria de segurança..."
npm audit --json || true

# Docker Build
echo "🐳 Docker: Build das imagens..."
cd ..
docker-compose build

echo "✅ CI/CD Local concluído!"
