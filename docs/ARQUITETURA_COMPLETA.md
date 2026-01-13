# 🏗️ ARQUITETURA COMPLETA - SunwOps MAB

**Stack**: FastAPI + Django + PostgreSQL + Redis + RabbitMQ  
**Padrão**: Clean Architecture + DDD + CQRS

---

## 📐 ESTRUTURA

```
backend/
├── src/
│   ├── core/                          # DOMÍNIO (independente)
│   │   ├── domain/
│   │   │   ├── orcamentos/           ✅ Implementado
│   │   │   ├── vendas/
│   │   │   ├── suporte/
│   │   │   └── marketing/
│   │   └── application/
│   │       ├── ports/                ✅ Interfaces
│   │       ├── use_cases/            ⏳ Próximo
│   │       └── dtos/
│   │
│   ├── adapters/                      # FRAMEWORKS (detalhes)
│   │   ├── fastapi_app/              # API Assíncrona
│   │   │   ├── routers/
│   │   │   ├── dependencies.py
│   │   │   └── main.py
│   │   │
│   │   ├── django_admin/             # Admin Panel
│   │   │   ├── settings.py
│   │   │   ├── models.py
│   │   │   └── admin.py
│   │   │
│   │   └── infrastructure/
│   │       ├── database/
│   │       │   ├── postgres/         # Write DB
│   │       │   └── replicas/         # Read Replicas
│   │       ├── cache/
│   │       │   └── redis_cache.py
│   │       ├── queue/
│   │       │   └── rabbitmq.py
│   │       └── repositories/
│   │           ├── kit_repo.py
│   │           └── orcamento_repo.py
│   │
│   └── shared/
│       ├── events/
│       └── utils/
│
├── docker/
├── tests/
└── requirements/
```

---

## 🗄️ BANCO DE DADOS

### PostgreSQL (Recomendado)

**Por quê?**
- ✅ ACID completo
- ✅ JSON/JSONB nativo (eventos)
- ✅ Replicação master-slave
- ✅ Particionamento
- ✅ Full-text search
- ✅ Extensões (PostGIS, TimescaleDB)

**Alternativas:**
- MySQL/MariaDB (menos features)
- CockroachDB (distribuído)

### Estratégia de Persistência

```
┌─────────────────────────────────────────┐
│         CQRS Pattern                    │
├─────────────────────────────────────────┤
│                                         │
│  WRITE (Commands)    READ (Queries)    │
│       │                    │            │
│       ▼                    ▼            │
│  PostgreSQL          PostgreSQL         │
│   (Master)           (Replica)          │
│       │                    │            │
│       └────────┬───────────┘            │
│                │                        │
│                ▼                        │
│           Event Store                   │
│         (Domain Events)                 │
└─────────────────────────────────────────┘
```

---

## 🔄 REPLICAÇÃO

### Master-Slave (Streaming Replication)

```yaml
# docker-compose.yml
services:
  postgres-master:
    image: postgres:15
    environment:
      POSTGRES_DB: sunwops
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pg-master:/var/lib/postgresql/data
    command: >
      postgres
      -c wal_level=replica
      -c max_wal_senders=3
      -c max_replication_slots=3
  
  postgres-replica-1:
    image: postgres:15
    environment:
      PGUSER: replicator
      PGPASSWORD: ${REPLICA_PASSWORD}
    command: >
      bash -c "
      until pg_basebackup --pgdata=/var/lib/postgresql/data -R --slot=replication_slot --host=postgres-master --port=5432
      do
        sleep 1
      done
      postgres
      "
    depends_on:
      - postgres-master
```

### Configuração

**Master** (`postgresql.conf`):
```ini
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3
synchronous_commit = on
```

**Replica** (`recovery.conf`):
```ini
standby_mode = on
primary_conninfo = 'host=postgres-master port=5432 user=replicator password=xxx'
```

---

## 🏛️ CAMADAS

### 1. DOMÍNIO (Core)
```python
# Independente de frameworks
# Apenas Python puro + lógica de negócio

domain/
├── entities.py          # Entidades
├── value_objects.py     # Value Objects
├── aggregates.py        # Aggregates
├── services.py          # Domain Services
├── events.py            # Domain Events
└── exceptions.py        # Exceções
```

### 2. APLICAÇÃO (Use Cases)
```python
# Orquestra o domínio
# Usa ports (interfaces)

application/
├── use_cases/
│   ├── criar_kit.py
│   └── aprovar_orcamento.py
├── ports/
│   ├── repositories.py  # Interfaces
│   └── services.py      # Interfaces
└── dtos/
    └── orcamento_dto.py
```

### 3. INFRAESTRUTURA (Adapters)
```python
# Implementa ports
# Detalhes técnicos

infrastructure/
├── database/
│   ├── models.py        # SQLAlchemy
│   └── repositories.py  # Implementação
├── cache/
│   └── redis_cache.py
└── queue/
    └── rabbitmq.py
```

### 4. FRAMEWORKS (Delivery)

#### FastAPI (Async)
```python
# API REST assíncrona
# WebSockets
# Background tasks

fastapi_app/
├── routers/
│   ├── kits.py
│   └── orcamentos.py
├── dependencies.py
└── main.py
```

#### Django (Admin)
```python
# Painel administrativo
# ORM para queries simples
# Autenticação

django_admin/
├── settings.py
├── models.py
└── admin.py
```

---

## 🔌 INTEGRAÇÃO FastAPI + Django

### Opção 1: Bancos Separados
```
FastAPI → PostgreSQL (principal)
Django  → PostgreSQL (admin) + Read Replica
```

### Opção 2: Banco Compartilhado (Recomendado)
```python
# FastAPI usa SQLAlchemy
# Django usa Django ORM
# Mesmo banco, ORMs diferentes

# Sincronizar schemas:
# 1. Alembic (FastAPI) gera migrations
# 2. Django lê tabelas existentes
```

**Django settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sunwops',
        'USER': 'admin',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'postgres-master',
        'PORT': '5432',
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sunwops',
        'USER': 'readonly',
        'PASSWORD': os.getenv('REPLICA_PASSWORD'),
        'HOST': 'postgres-replica-1',
        'PORT': '5432',
    }
}

# Router para leitura/escrita
DATABASE_ROUTERS = ['path.to.ReplicaRouter']
```

---

## 📦 PERSISTÊNCIA

### Event Sourcing (Opcional)
```python
# Armazena eventos de domínio
# Reconstrói estado a partir de eventos

event_store/
├── events_table        # Todos os eventos
├── snapshots_table     # Estados consolidados
└── projections/        # Views materializadas
```

### Tabelas Principais
```sql
-- Kits
CREATE TABLE kits (
    id UUID PRIMARY KEY,
    nome VARCHAR(200),
    is_template BOOLEAN,
    created_at TIMESTAMP,
    -- Snapshot do estado atual
    data JSONB
);

-- Itens
CREATE TABLE itens_kit (
    id UUID PRIMARY KEY,
    kit_id UUID REFERENCES kits(id),
    categoria VARCHAR(50),
    nome VARCHAR(200),
    preco DECIMAL(10,2),
    quantidade INT,
    data JSONB
);

-- Orçamentos
CREATE TABLE orcamentos (
    id UUID PRIMARY KEY,
    kit_id UUID REFERENCES kits(id),
    cliente_nome VARCHAR(200),
    status VARCHAR(50),
    created_at TIMESTAMP,
    data JSONB
);

-- Event Store
CREATE TABLE domain_events (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id UUID,
    aggregate_type VARCHAR(100),
    event_type VARCHAR(100),
    event_data JSONB,
    occurred_at TIMESTAMP,
    version INT
);

CREATE INDEX idx_events_aggregate ON domain_events(aggregate_id, version);
```

---

## 🚀 FLUXO DE DADOS

### Write (Command)
```
Cliente → FastAPI → Use Case → Domain → Repository → PostgreSQL Master
                                    ↓
                              Domain Events → RabbitMQ → Workers
```

### Read (Query)
```
Cliente → FastAPI → Repository → PostgreSQL Replica → Cache (Redis)
```

### Background Jobs
```
RabbitMQ → Celery Worker → Use Case → Domain → Repository
```

---

## 🐳 DOCKER COMPOSE

```yaml
version: '3.8'

services:
  # API Assíncrona
  fastapi:
    build: ./fastapi_app
    ports:
      - "8000:8000"
    depends_on:
      - postgres-master
      - redis
      - rabbitmq
    environment:
      DATABASE_URL: postgresql+asyncpg://admin:${DB_PASSWORD}@postgres-master:5432/sunwops
      REDIS_URL: redis://redis:6379/0
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
  
  # Admin Panel
  django:
    build: ./django_admin
    ports:
      - "8001:8000"
    depends_on:
      - postgres-master
    environment:
      DATABASE_URL: postgresql://admin:${DB_PASSWORD}@postgres-master:5432/sunwops
  
  # Database Master
  postgres-master:
    image: postgres:15
    volumes:
      - pg-master:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: sunwops
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
  
  # Database Replica
  postgres-replica:
    image: postgres:15
    volumes:
      - pg-replica:/var/lib/postgresql/data
    depends_on:
      - postgres-master
  
  # Cache
  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
  
  # Message Broker
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "15672:15672"
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
  
  # Workers
  celery-worker:
    build: ./fastapi_app
    command: celery -A app.worker worker -l info
    depends_on:
      - rabbitmq
      - redis

volumes:
  pg-master:
  pg-replica:
  redis-data:
  rabbitmq-data:
```

---

## 📊 DECISÕES TÉCNICAS

| Decisão | Escolha | Motivo |
|---------|---------|--------|
| **Banco Principal** | PostgreSQL 15 | ACID, JSON, Replicação |
| **Replicação** | Streaming (Master-Slave) | Simples, confiável |
| **Cache** | Redis | Performance, pub/sub |
| **Fila** | RabbitMQ | Confiável, DLQ |
| **API** | FastAPI | Async, performance |
| **Admin** | Django | Produtividade |
| **ORM API** | SQLAlchemy 2.0 | Async, flexível |
| **ORM Admin** | Django ORM | Integrado |
| **Migrations** | Alembic | Controle fino |

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ Domínio (entities, aggregates, events)
2. ✅ Ports (interfaces)
3. ⏳ Use Cases
4. ⏳ Repositories (implementação)
5. ⏳ FastAPI routers
6. ⏳ Django admin
7. ⏳ Docker compose
8. ⏳ Testes

**Desenvolvido com ☀️ por SunwOps Team**
