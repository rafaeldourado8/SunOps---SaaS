# 🏗️ ARQUITETURA TÉCNICA - SunwOps MAB

## 📊 Stack Escolhida

### Backend
```
FastAPI (Async)  → API REST + WebSockets
Django Admin     → Painel administrativo
PostgreSQL       → Banco principal (ACID)
Redis            → Cache + Sessions
RabbitMQ         → Filas assíncronas
```

### Por que PostgreSQL?

✅ **ACID completo** - Transações seguras para orçamentos  
✅ **JSONB** - Flexibilidade para dados dinâmicos  
✅ **Full-text search** - Busca em produtos/clientes  
✅ **Replicação nativa** - Read replicas fáceis  
✅ **Particionamento** - Escala horizontal  
✅ **Extensões** - PostGIS (futuro: geolocalização)

### Alternativas Descartadas

❌ **MongoDB** - Sem transações ACID robustas  
❌ **MySQL** - JSONB inferior, replicação complexa  
❌ **SQLite** - Não escala para produção

---

## 🗄️ Estratégia de Persistência

### Padrão: Repository + Unit of Work

```python
# Domain (puro Python)
class Orcamento:
    def aprovar(self): ...

# Application (use cases)
class AprovarOrcamento:
    def execute(self, orcamento_id):
        orcamento = self.repo.get(orcamento_id)
        orcamento.aprovar()
        self.uow.commit()

# Infrastructure (SQLAlchemy)
class OrcamentoRepository:
    def get(self, id): ...
    def save(self, orcamento): ...
```

### ORM: SQLAlchemy 2.0 (Async)

```python
# Async queries
async with async_session() as session:
    result = await session.execute(
        select(Orcamento).where(Orcamento.id == id)
    )
    return result.scalar_one()
```

---

## 🔄 Replicação PostgreSQL

### Configuração: 1 Master + 2 Read Replicas

```
┌─────────────┐
│   Master    │ ← Writes (FastAPI)
│ (Primary)   │
└──────┬──────┘
       │ Streaming Replication
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Replica1 │   │ Replica2 │   │ Replica3 │
│ (Read)   │   │ (Read)   │   │ (Backup) │
└──────────┘   └──────────┘   └──────────┘
```

### Load Balancer de Leitura

```python
# Writes → Master
@router.post("/orcamentos")
async def criar(db: AsyncSession = Depends(get_master_db)):
    ...

# Reads → Replicas (round-robin)
@router.get("/orcamentos")
async def listar(db: AsyncSession = Depends(get_replica_db)):
    ...
```

### Configuração Docker Compose

```yaml
services:
  postgres-master:
    image: postgres:15-alpine
    environment:
      POSTGRES_REPLICATION_MODE: master
      POSTGRES_REPLICATION_USER: replicator
    volumes:
      - master-data:/var/lib/postgresql/data
  
  postgres-replica1:
    image: postgres:15-alpine
    environment:
      POSTGRES_REPLICATION_MODE: slave
      POSTGRES_MASTER_HOST: postgres-master
    volumes:
      - replica1-data:/var/lib/postgresql/data
```

---

## 🚀 Arquitetura de Serviços

```
┌─────────────────────────────────────────────────────────┐
│                    NGINX (Reverse Proxy)                │
│                  SSL/TLS + Load Balancer                │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
    ┌────────▼────────┐          ┌────────▼────────┐
    │   FastAPI       │          │  Django Admin   │
    │   (Async API)   │          │  (Sync Panel)   │
    │   Port: 8000    │          │  Port: 8001     │
    └────────┬────────┘          └────────┬────────┘
             │                            │
             └────────────┬───────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐
    │PostgreSQL│    │  Redis   │    │ RabbitMQ │
    │ Master   │    │  Cache   │    │  Queue   │
    └──────────┘    └──────────┘    └────┬─────┘
                                          │
                                    ┌─────▼─────┐
                                    │  Celery   │
                                    │  Workers  │
                                    └───────────┘
```

---

## 📁 Estrutura de Diretórios

```
sunwops/
├── fastapi_app/              # API Assíncrona
│   ├── api/
│   │   ├── v1/
│   │   │   ├── orcamentos.py
│   │   │   ├── kits.py
│   │   │   └── whatsapp.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── domain/           # Entities, VOs, Events
│   │   ├── application/      # Use Cases
│   │   └── infrastructure/   # Repos, DB, Cache
│   ├── config.py
│   └── main.py
│
├── django_app/               # Admin Panel
│   ├── admin_panel/
│   │   ├── models.py         # Django Models
│   │   ├── admin.py          # Admin Config
│   │   └── views.py
│   ├── settings.py
│   └── manage.py
│
├── shared/                   # Código compartilhado
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   └── schemas/
│
├── workers/                  # Celery Tasks
│   ├── tasks/
│   │   ├── email.py
│   │   ├── pdf.py
│   │   └── whatsapp.py
│   └── celery_app.py
│
├── docker/
│   ├── Dockerfile.fastapi
│   ├── Dockerfile.django
│   ├── Dockerfile.worker
│   └── docker-compose.yml
│
└── tests/
```

---

## 🔧 Configuração de Banco

### PostgreSQL Master (docker-compose.yml)

```yaml
postgres-master:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: sunwops
    POSTGRES_USER: sunwops_user
    POSTGRES_PASSWORD: ${DB_PASSWORD}
    POSTGRES_REPLICATION_MODE: master
    POSTGRES_REPLICATION_USER: replicator
    POSTGRES_REPLICATION_PASSWORD: ${REPL_PASSWORD}
  volumes:
    - postgres-master:/var/lib/postgresql/data
    - ./docker/postgres/master.conf:/etc/postgresql/postgresql.conf
  ports:
    - "5432:5432"
  command: postgres -c config_file=/etc/postgresql/postgresql.conf
```

### PostgreSQL Replica (docker-compose.yml)

```yaml
postgres-replica1:
  image: postgres:15-alpine
  environment:
    POSTGRES_REPLICATION_MODE: slave
    POSTGRES_MASTER_HOST: postgres-master
    POSTGRES_MASTER_PORT: 5432
    POSTGRES_REPLICATION_USER: replicator
    POSTGRES_REPLICATION_PASSWORD: ${REPL_PASSWORD}
  volumes:
    - postgres-replica1:/var/lib/postgresql/data
  ports:
    - "5433:5432"
  depends_on:
    - postgres-master
```

### master.conf

```conf
# Replicação
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3
hot_standby = on

# Performance
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

---

## 🔄 Redis Cache Strategy

### Configuração

```yaml
redis:
  image: redis:7-alpine
  command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
  volumes:
    - redis-data:/data
  ports:
    - "6379:6379"
```

### Uso no FastAPI

```python
from redis.asyncio import Redis

# Cache de queries
@cache(ttl=300)  # 5 minutos
async def get_orcamento(id: str):
    return await db.get(Orcamento, id)

# Session store
async def get_user_session(token: str):
    return await redis.get(f"session:{token}")
```

---

## 🐰 RabbitMQ Queues

### Configuração

```yaml
rabbitmq:
  image: rabbitmq:3-management-alpine
  environment:
    RABBITMQ_DEFAULT_USER: sunwops
    RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
  ports:
    - "5672:5672"   # AMQP
    - "15672:15672" # Management UI
  volumes:
    - rabbitmq-data:/var/lib/rabbitmq
```

### Filas Definidas

```python
# Filas por prioridade
QUEUES = {
    "email.high": {"priority": 10},      # Emails urgentes
    "email.normal": {"priority": 5},     # Emails normais
    "pdf.generate": {"priority": 7},     # Geração de PDF
    "whatsapp.send": {"priority": 8},    # WhatsApp
    "monitoring.check": {"priority": 3}, # Monitoramento
}
```

---

## 🔐 Segurança

### Secrets Management

```bash
# .env (não commitar!)
DB_PASSWORD=xxx
REPL_PASSWORD=xxx
RABBITMQ_PASSWORD=xxx
REDIS_PASSWORD=xxx
JWT_SECRET=xxx
```

### Backup Automático

```bash
# Cron diário
0 2 * * * pg_dump -h postgres-master sunwops | gzip > /backups/sunwops_$(date +\%Y\%m\%d).sql.gz
```

---

## 📊 Monitoramento

### Prometheus + Grafana

```yaml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
```

### Métricas Coletadas

- Latência de queries (p50, p95, p99)
- Taxa de cache hit/miss
- Tamanho das filas RabbitMQ
- Lag de replicação PostgreSQL
- CPU/Memória dos containers

---

## 🚀 Deploy

### Produção (AWS/DigitalOcean)

```
RDS PostgreSQL (Multi-AZ)
ElastiCache Redis (Cluster)
Amazon MQ (RabbitMQ)
ECS/Fargate (Containers)
ALB (Load Balancer)
S3 (Backups)
CloudWatch (Logs)
```

### Custos Estimados (Mês)

- RDS db.t3.medium: $70
- ElastiCache t3.small: $30
- Amazon MQ t3.micro: $20
- ECS Fargate: $50
- Total: ~$170/mês

---

**Próximo passo**: Implementar repositories?
