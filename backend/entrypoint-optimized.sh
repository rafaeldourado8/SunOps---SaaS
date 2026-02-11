#!/bin/bash
set -e

echo "🚀 Iniciando CRM Solar com RabbitMQ + Celery"

# Aguardar serviços
echo "⏳ Aguardando PostgreSQL..."
while ! nc -z db 5432; do sleep 1; done

echo "⏳ Aguardando Redis..."
while ! nc -z redis 6379; do sleep 1; done

echo "⏳ Aguardando RabbitMQ..."
while ! nc -z rabbitmq 5672; do sleep 1; done

# Migrações
echo "📦 Executando migrações..."
python manage.py migrate --noinput

# Coletar estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar aplicação
echo "✅ Iniciando Gunicorn..."
exec "$@"
