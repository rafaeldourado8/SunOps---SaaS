# 🏗️ ARQUITETURA DDD - SunwOps MAB

**Stack**: FastAPI + Django + PostgreSQL + Redis + RabbitMQ

---

## 📐 ESTRUTURA DE PASTAS

```
sunwops/
├── api/                          # FastAPI (Async)
│   ├── main.py
│   ├── dependencies.py
│   ├── middleware/
│   └── v1/
│       ├── endpoints/
│       │   ├── kits.py
│       │   ├── orcamentos.py
│       │   └── itens.py
│       └── schemas/              # Pydantic DTOs
│
├── admin/                        # Django Admin
│   ├── manage.py
│   ├── settings.py
│   ├── urls.py
│   └── apps/
│       ├── orcamentos/
│       │   ├── admin.py
│       │   ├── models.py         # Django ORM
│       │   └── views.py
│       └── usuarios/
│
├── core/                         # Domain Layer (DDD)
│   ├── domain/
│   │   ├── orcamentos/
│   │   │   ├── entities.py       ✅
│   │   │   ├── value_objects.py  ✅
│   │   │   ├── aggregates.py     ✅
│   │   │   ├── events.py         ✅
│   │   │   ├── services.py       ✅
│   │   │   ├── exceptions.py     ✅
│   │   │   └── repositories.py   ⏳ (interfaces)
│   │   └── vendas/
│   │
│   ├── application/              # Use Cases
│   │   ├── use_cases/
│   │   │   ├── criar_kit.py
│   │   │   ├── criar_orcamento.py
│   │   │   └── aprovar_orcamento.py
│   │   └── dtos/
│   │
│   └── infrastructure/           # Adapters
│       ├── persistence/
│       │   ├── sqlalchemy/       # FastAPI
│       │   │   ├── models.py
│       │   │   ├── repositories.py
│       │   │   └── session.py
│       │   └── django/           # Django Admin
│       │       └── models.py
│       ├── cache/
│       │   └── redis_cache.py
│       ├── messaging/
│       │   ├── rabbitmq.py
│       │   └── events_publisher.py
│       └── external/
│           ├── whatsapp/
│           └── email/
│
├── shared/                       # Shared Kernel
│   ├── utils.py
│   └── constants.py
│
└── docker/
    ├── Dockerfile.api
    ├── Dockerfile.admin
    ├── Dockerfile.worker
    └── docker-compose.yml
```

---

## 🗄️ BANCO DE DADOS: PostgreSQL

### Por que PostgreSQL?

✅ **ACID completo** - Transações confiáveis  
✅ **JSON/JSONB** - Flexibilidade para eventos  
✅ **Replicação nativa** - Read replicas  
✅ **Particionamento** - Escalabilidade  
✅ **Full-text search** - Busca avançada  
✅ **Extensões** - PostGIS, pg_trgm  
✅ **Maturidade** - Comunidade ativa

### Alternativas Descartadas

❌ **MySQL** - JSON menos eficiente  
❌ **MongoDB** - Sem ACID multi-documento  
❌ **SQLite** - Não escala

---

## 🔄 ESTRATÉGIA DE PERSISTÊNCIA

### Dual Write Pattern

```
┌─────────────┐
│   FastAPI   │ (Async)
└──────┬──────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ SQLAlchemy  │   │   Django    │
│   (Async)   │   │     ORM     │
└──────┬──────┘   └──────┬──────┘
       │                 │
       └────────┬────────┘
                ▼
        ┌───────────────┐
        │  PostgreSQL   │
        │   (Master)    │
        └───────┬───────┘
                │
        ┌───────┴───────┐
        ▼               ▼
    ┌────────┐     ┌────────┐
    │ Replica│     │ Replica│
    │  Read  │     │  Read  │
    └────────┘     └────────┘
```

### Configuração

**FastAPI (SQLAlchemy Async)**
```python
# Escrita: Master
# Leitura: Replicas (round-robin)
```

**Django Admin**
```python
# Apenas Master (operações admin)
```

---

## 📊 REPLICAÇÃO

### Master-Slave (Streaming Replication)

```yaml
postgresql:
  master:
    host: db-master
    port: 5432
    
  replicas:
    - host: db-replica-1
      port: 5432
      lag_max: 100ms
      
    - host: db-replica-2
      port: 5432
      lag_max: 100ms
```

### Estratégia de Leitura

```python
# FastAPI - Read Replicas
@router.get("/orcamentos")
async def listar(db: AsyncSession = Depends(get_read_db)):
    # Usa replica
    pass

# FastAPI - Write Master
@router.post("/orcamentos")
async def criar(db: AsyncSession = Depends(get_write_db)):
    # Usa master
    pass
```

---

## 🔌 INTEGRAÇÃO FastAPI + Django

### Compartilhamento de Schema

```python
# shared/database.py
DATABASE_URL = "postgresql+asyncpg://user:pass@db-master:5432/sunwops"

# FastAPI usa asyncpg
# Django usa psycopg2
```

### Models Sincronizados

**Django** (Source of Truth)
```python
# admin/apps/orcamentos/models.py
class Orcamento(models.Model):
    id = models.UUIDField(primary_key=True)
    cliente_nome = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    # ...
```

**SQLAlchemy** (Espelho)
```python
# infrastructure/persistence/sqlalchemy/models.py
class OrcamentoModel(Base):
    __tablename__ = "orcamentos_orcamento"  # Mesmo nome Django
    id = Column(UUID, primary_key=True)
    cliente_nome = Column(String(200))
    status = Column(String(20))
    # ...
```

### Migrations

```bash
# 1. Django cria migrations
python manage.py makemigrations

# 2. Django aplica no master
python manage.py migrate

# 3. SQLAlchemy reflete automaticamente
# (não precisa de migrations próprias)
```

---

## 🐰 RabbitMQ - Filas

### Exchanges e Queues

```
┌──────────────────────────────────────┐
│         RabbitMQ Topology            │
├──────────────────────────────────────┤
│                                      │
│  Exchange: orcamentos.events         │
│  Type: Topic                         │
│  ├─ orcamento.criado                 │
│  ├─ orcamento.aprovado               │
│  └─ orcamento.enviado                │
│                                      │
│  Queues:                             │
│  ├─ email.queue                      │
│  ├─ whatsapp.queue                   │
│  ├─ pdf.queue                        │
│  └─ analytics.queue                  │
└──────────────────────────────────────┘
```

### Publicação de Eventos

```python
# infrastructure/messaging/events_publisher.py
class EventPublisher:
    async def publish(self, event: DomainEvent):
        await rabbitmq.publish(
            exchange="orcamentos.events",
            routing_key=f"orcamento.{event.__class__.__name__.lower()}",
            body=event.to_json()
        )
```

### Consumers (Workers)

```python
# workers/email_worker.py
@rabbitmq.consumer("email.queue")
async def processar_email(message):
    evento = OrcamentoEnviado.from_json(message.body)
    await email_service.enviar(evento.cliente_contato)
```

---

## 🔴 Redis - Cache

### Estratégias

**1. Cache de Queries**
```python
@cache(ttl=300)  # 5 minutos
async def listar_orcamentos(filtros):
    return await db.query(...)
```

**2. Cache de Agregados**
```python
# Cache do aggregate completo
key = f"orcamento:{id}"
ttl = 3600  # 1 hora
```

**3. Cache de Sessão**
```python
# JWT + Redis
key = f"session:{user_id}"
ttl = 86400  # 24 horas
```

**4. Rate Limiting**
```python
key = f"rate:{ip}:{endpoint}"
ttl = 60  # 1 minuto
```

---

## 🐳 Docker Compose

```yaml
version: '3.8'

services:
  # PostgreSQL Master
  db-master:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: sunwops
      POSTGRES_USER: sunwops
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_master:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  # PostgreSQL Replica 1
  db-replica-1:
    image: postgres:15-alpine
    environment:
      POSTGRES_MASTER_HOST: db-master
    depends_on:
      - db-master
  
  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  # RabbitMQ
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: sunwops
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
  
  # FastAPI
  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.api
    ports:
      - "8000:8000"
    depends_on:
      - db-master
      - redis
      - rabbitmq
    environment:
      DATABASE_URL: postgresql+asyncpg://sunwops:${DB_PASSWORD}@db-master:5432/sunwops
      REDIS_URL: redis://redis:6379
      RABBITMQ_URL: amqp://sunwops:${RABBITMQ_PASSWORD}@rabbitmq:5672
  
  # Django Admin
  admin:
    build:
      context: .
      dockerfile: docker/Dockerfile.admin
    ports:
      - "8001:8000"
    depends_on:
      - db-master
    environment:
      DATABASE_URL: postgresql://sunwops:${DB_PASSWORD}@db-master:5432/sunwops
  
  # Celery Worker
  worker:
    build:
      context: .
      dockerfile: docker/Dockerfile.worker
    depends_on:
      - rabbitmq
      - redis
    environment:
      CELERY_BROKER_URL: amqp://sunwops:${RABBITMQ_PASSWORD}@rabbitmq:5672
      CELERY_RESULT_BACKEND: redis://redis:6379

volumes:
  postgres_master:
  redis_data:
```

---

## 🔄 FLUXO DE DADOS

### Escrita (Command)

```
Cliente → FastAPI → Use Case → Aggregate → Repository → PostgreSQL Master
                                    ↓
                              Domain Event
                                    ↓
                              RabbitMQ → Workers
```

### Leitura (Query)

```
Cliente → FastAPI → Redis Cache?
                         ↓ miss
                    PostgreSQL Replica → Cache
```

---

## 📦 DEPENDÊNCIAS

### FastAPI
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy[asyncio]==2.0.25
asyncpg==0.29.0
pydantic==2.5.3
redis[hiredis]==5.0.1
aio-pika==9.3.1
```

### Django
```txt
django==5.0
psycopg2-binary==2.9.9
celery==5.3.6
```

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ Domain Layer completo
2. ⏳ Repository interfaces
3. ⏳ SQLAlchemy models
4. ⏳ Django models
5. ⏳ FastAPI endpoints
6. ⏳ RabbitMQ setup
7. ⏳ Redis cache
8. ⏳ Docker compose

Quer que eu implemente os **Repository Interfaces** agora?
