# 🚀 Setup - SunwOps MAB

## 📋 Pré-requisitos

- Docker 24+
- Docker Compose 2.0+

## ⚡ Quick Start

```bash
# 1. Copiar .env
cp backend/.env.example backend/.env

# 2. Subir containers
docker-compose up -d

# 3. Rodar migrations
docker-compose exec api alembic upgrade head

# 4. Acessar
http://localhost:8000/docs
```

## 🐳 Containers

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| API | 8000 | FastAPI |
| PostgreSQL Master | 5432 | Write DB |
| PostgreSQL Replica | 5433 | Read DB |
| Redis | 6379 | Cache |
| RabbitMQ | 5672 | Message Broker |
| RabbitMQ UI | 15672 | Admin (guest/guest) |

## 📊 Arquitetura

```
┌─────────────────────────────────────────┐
│         Cliente (HTTP/WebSocket)        │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         FastAPI (Port 8000)             │
│  ┌──────────────────────────────────┐   │
│  │  Routers → Use Cases → Domain    │   │
│  └──────────────────────────────────┘   │
└────────┬────────────────────┬───────────┘
         │                    │
         ▼                    ▼
┌──────────────────┐  ┌──────────────────┐
│  PostgreSQL      │  │  Redis (Cache)   │
│  Master + Replica│  │                  │
└──────────────────┘  └──────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  RabbitMQ → Celery Workers               │
└──────────────────────────────────────────┘
```

## 🔧 Comandos Úteis

```bash
# Ver logs
docker-compose logs -f api

# Acessar shell
docker-compose exec api bash

# Rodar migrations
docker-compose exec api alembic upgrade head

# Criar migration
docker-compose exec api alembic revision --autogenerate -m "descricao"

# Parar tudo
docker-compose down

# Limpar volumes
docker-compose down -v
```

## 📝 Endpoints

### Kits
- `POST /api/v1/kits/` - Criar kit
- `POST /api/v1/kits/{id}/itens` - Adicionar item
- `GET /api/v1/kits/{id}/geracao` - Calcular geração
- `GET /api/v1/kits/templates` - Listar templates

### Orçamentos
- `POST /api/v1/orcamentos/` - Criar orçamento
- `POST /api/v1/orcamentos/{id}/aprovar` - Aprovar
- `POST /api/v1/orcamentos/{id}/enviar` - Enviar
- `GET /api/v1/orcamentos/{id}` - Buscar

## 🧪 Testes

```bash
# Rodar testes
docker-compose exec api pytest

# Com cobertura
docker-compose exec api pytest --cov=src
```

## 🔐 Variáveis de Ambiente

```env
# Database
POSTGRES_DB=sunwops
POSTGRES_USER=admin
POSTGRES_PASSWORD=changeme

# Redis
REDIS_URL=redis://redis:6379/0

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
```

## 📊 Monitoramento

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **RabbitMQ UI**: http://localhost:15672 (guest/guest)

## 🎯 Próximos Passos

1. ✅ Docker Compose
2. ⏳ Alembic Migrations
3. ⏳ Testes Unitários
4. ⏳ Django Admin
5. ⏳ CI/CD

---

**Desenvolvido com ☀️ por SunwOps Team**
