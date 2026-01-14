# Sprint 1 - Setup Multi-Tenancy + Auth + Infraestrutura

## ✅ Implementado

### Multi-tenancy
- ✅ Tenant Model (banco MASTER)
- ✅ Connection Manager (database-per-tenant)
- ✅ Tenant Resolution Middleware
- ✅ Cache Manager (Redis)

### Autenticação
- ✅ User Model com Roles (SuperAdmin, Admin, Vendedor)
- ✅ JWT Token Handler
- ✅ Auth Middleware
- ✅ Auth Dependencies

### Infraestrutura
- ✅ FastAPI App
- ✅ Celery + RabbitMQ
- ✅ Event Bus
- ✅ Docker Compose completo

## 🚀 Como Rodar

### 1. Subir containers
```bash
docker-compose up -d
```

### 2. Aguardar serviços (30-60s)
```bash
docker-compose logs -f
```

### 3. Criar migrations
```bash
docker-compose exec django python manage.py makemigrations
docker-compose exec django python manage.py migrate
```

### 4. Inicializar banco MASTER
```bash
docker-compose exec postgres psql -U postgres -f /scripts/init_master_db.sql
```

### 5. Criar superuser
```bash
docker-compose exec django python manage.py createsuperuser
```

## 🔗 Acessar Serviços

- **Django Admin**: http://localhost:8000/admin
- **FastAPI Docs**: http://localhost:8001/docs
- **RabbitMQ Management**: http://localhost:15672 (user: rabbitmq, pass: rabbitmq_dev_password)

## 🧪 Testar Multi-Tenancy

### 1. Login via FastAPI
```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Criar Cliente (com tenant header)
```bash
curl -X POST http://localhost:8001/api/v1/clientes \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Slug: solar-abc" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "nome": "João Silva",
    "tipo_documento": "CPF",
    "numero_documento": "12345678901",
    "email": "joao@email.com",
    "telefone": "11999999999"
  }'
```

## 📊 Arquitetura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   FastAPI   │────▶│   Django    │
│             │     │  (Port 8001)│     │  (Port 8000)│
└─────────────┘     └─────────────┘     └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │    Redis    │     │  PostgreSQL │
                    │  (Port 6379)│     │  (Port 5432)│
                    └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  RabbitMQ   │
                    │  (Port 5672)│
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Celery    │
                    │   Worker    │
                    └─────────────┘
```

## 🔐 Roles

- **SUPERADMIN**: Acesso total, gerencia tenants
- **ADMIN**: Gerencia tenant específico
- **VENDEDOR**: Acesso limitado (CRUD clientes/orçamentos)

## 📝 Próximos Passos

- [ ] Testar multi-tenancy com 2 tenants
- [ ] Implementar Sprint 2 (Fornecedores + APIs completas)
- [ ] Adicionar testes de integração
